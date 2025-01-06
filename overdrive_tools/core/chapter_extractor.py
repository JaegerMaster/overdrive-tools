import os
import re
from typing import Dict, List, Tuple
import mutagen.id3 as id3
from mutagen.mp3 import MP3
from collections import OrderedDict
from rich.console import Console
from . import utils

console = Console()

class ChapterExtractor:
    def __init__(self, directory: str):
        """Initialize chapter extractor with directory path."""
        self.directory = os.path.abspath(directory)
        
    def _timestr(self, secs: float) -> str:
        """Convert seconds to HH:MM:SS.mmm format."""
        return utils.format_timestamp(secs)
        
    def _load_mp3(self, total: float, file: str) -> Tuple[float, List[List[str]]]:
        """Load and extract chapter information from MP3 file."""
        try:
            path = os.path.join(self.directory, file)
            audio = MP3(path)
            m = id3.ID3(path)
            data = m.get("TXXX:OverDrive MediaMarkers")
            
            if not data:
                console.print(f"[yellow]Can't find TXXX data point for {file}[/yellow]")
                return total + audio.info.length, []
                
            info = data.text[0]
            console.print(f"[blue]Processing chapters from {file}[/blue]")
            console.print(f"[dim]Raw chapter data: {info[:200]}...[/dim]")  # Debug output
            
            file_chapters = re.findall(
                r"<Name>\s*([^>]+?)\s*</Name><Time>\s*([\d:.]+)\s*</Time>",
                info,
                re.MULTILINE
            )
            
            if not file_chapters:
                console.print(f"[yellow]No chapters found in {file} using regular expression[/yellow]")
                return total + audio.info.length, []
            
            chapters = []
            for i, chapter in enumerate(file_chapters):
                try:
                    if len(chapter) != 2:
                        console.print(f"[yellow]Invalid chapter format in {file}, chapter {i+1}: {chapter}[/yellow]")
                        continue
                        
                    name, length = chapter
                    console.print(f"[dim]Processing chapter: {name} at {length}[/dim]")  # Debug output
                    
                    # Clean up chapter name
                    name = re.sub(r'^"(.+)"$', r"\1", name)
                    name = re.sub(r"^\*(.+)\*$", r"\1", name)
                    name = re.sub(r"\s*\([^)]*\)$", "", name)  # Remove sub-chapter markers
                    name = re.sub(r"\s*-?\s*Chapter\s+\d+\s+(?i)Continued\)?$", "", name)  # Remove "Chapter X Continued"
                    name = re.sub(r"\s+\(?continued\)?$", "", name)  # Keep existing continued check
                    name = re.sub(r"\s+-\s*$", "", name)
                    name = re.sub(r"^Dis[kc]\s+\d+\W*$", "", name)
                    name = name.strip()
                    
                    if not name:
                        console.print(f"[yellow]Empty chapter name after cleaning in {file}, chapter {i+1}[/yellow]")
                        continue
                    
                    # Convert timestamp to seconds with error handling
                    t_parts = list(length.split(":"))
                    if not t_parts:
                        console.print(f"[red]Invalid timestamp format in {file}, chapter {i+1}: {length}[/red]")
                        continue
                    
                    t_parts.reverse()
                    try:
                        seconds = total + float(t_parts[0])  # seconds
                        if len(t_parts) > 1:
                            seconds += int(t_parts[1]) * 60  # minutes
                        if len(t_parts) > 2:
                            seconds += int(t_parts[2]) * 60 * 60  # hours
                        chapters.append([name, seconds])
                        console.print(f"[dim]Successfully processed chapter: {name} at {self._timestr(seconds)}[/dim]")
                    except (ValueError, IndexError) as e:
                        console.print(f"[red]Error parsing timestamp {length} in {file}, chapter {i+1}: {str(e)}[/red]")
                        continue
                        
                except Exception as e:
                    console.print(f"[red]Error processing chapter in {file}, chapter {i+1}: {str(e)}[/red]")
                    continue
            
            if not chapters:
                console.print(f"[yellow]No valid chapters extracted from {file}[/yellow]")
            else:
                console.print(f"[green]Successfully extracted {len(chapters)} chapters from {file}[/green]")
            
            return total + audio.info.length, chapters
            
        except Exception as e:
            console.print(f"[red]Error processing file {file}: {str(e)}[/red]")
            return total, []
    
    def extract_chapters(self) -> bool:
        """Extract chapters from all MP3 files in directory."""
        try:
            total = 0
            all_chapters = OrderedDict()
            
            # Get all MP3 files and sort them
            mp3_files = [f for f in os.listdir(self.directory) if f.endswith('.mp3')]
            if not mp3_files:
                console.print("[red]No MP3 files found in directory[/red]")
                return False
            
            console.print(f"[blue]Found {len(mp3_files)} MP3 files[/blue]")
            
            # Process each MP3 file
            for file in sorted(mp3_files):
                try:
                    total, chapters = self._load_mp3(total, file)
                    for chapter in chapters:
                        if not chapter[0]:  # Skip empty chapter names
                            continue
                        if chapter[0] in all_chapters:
                            console.print(f"[yellow]Duplicate chapter name found: {chapter[0]}[/yellow]")
                            continue
                        all_chapters[chapter[0]] = chapter[1]
                except Exception as e:
                    console.print(f"[red]Error processing {file}: {str(e)}[/red]")
                    continue
            
            if not all_chapters:
                console.print("[yellow]No chapters found in MP3 files[/yellow]")
                return False
            
            # Write chapters to file
            chapters_file = os.path.join(self.directory, "chapters.txt")
            try:
                with open(chapters_file, "w", encoding='utf-8') as f:
                    for name, length in all_chapters.items():
                        chapter_line = f"{self._timestr(length)} {name}"
                        f.write(chapter_line + "\n")
                
                console.print(f"[green]Successfully extracted {len(all_chapters)} chapters to {chapters_file}[/green]")
                return True
                
            except Exception as e:
                console.print(f"[red]Error writing chapters file: {str(e)}[/red]")
                return False
            
        except Exception as e:
            console.print(f"[red]Error extracting chapters: {str(e)}[/red]")
            return False
