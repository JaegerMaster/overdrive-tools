# overdrive_tools/core/chapter_extractor.py

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
        path = os.path.join(self.directory, file)
        audio = MP3(path)
        m = id3.ID3(path)
        
        data = m.get("TXXX:OverDrive MediaMarkers")
        if not data:
            console.print(f"[yellow]Can't find TXXX data point for {file}[/yellow]")
            return total + audio.info.length, []

        info = data.text[0]
        file_chapters = re.findall(
            r"<Name>\s*([^>]+?)\s*</Name><Time>\s*([\d:.]+)\s*</Time>",
            info,
            re.MULTILINE
        )
        
        chapters = []
        for chapter in file_chapters:
            name, length = chapter
            # Clean up chapter name
            name = re.sub(r'^"(.+)"$', r"\1", name)
            name = re.sub(r"^\*(.+)\*$", r"\1", name)
            name = re.sub(r"\s*\([^)]*\)$", "", name)  # Remove sub-chapter markers
            name = re.sub(r"\s+\(?continued\)?$", "", name)
            name = re.sub(r"\s+-\s*$", "", name)
            name = re.sub(r"^Dis[kc]\s+\d+\W*$", "", name)
            name = name.strip()

            # Convert timestamp to seconds
            t_parts = list(length.split(":"))
            t_parts.reverse()
            seconds = total + float(t_parts[0])
            if len(t_parts) > 1:
                seconds += int(t_parts[1]) * 60
            if len(t_parts) > 2:
                seconds += int(t_parts[2]) * 60 * 60

            chapters.append([name, seconds])

        return total + audio.info.length, chapters

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

            # Process each MP3 file
            for file in sorted(mp3_files):
                total, chapters = self._load_mp3(total, file)
                for chapter in chapters:
                    if chapter[0] in all_chapters:
                        continue
                    all_chapters[chapter[0]] = chapter[1]

            if not all_chapters:
                console.print("[yellow]No chapters found in MP3 files[/yellow]")
                return False

            # Write chapters to file
            chapters_file = os.path.join(self.directory, "chapters.txt")
            with open(chapters_file, "w") as f:
                for name, length in all_chapters.items():
                    chapter_line = f"{self._timestr(length)} {name}"
                    f.write(chapter_line + "\n")

            console.print(f"[green]Successfully extracted {len(all_chapters)} chapters to {chapters_file}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error extracting chapters: {str(e)}[/red]")
            return False
