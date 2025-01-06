# OverDrive Tools

A Python package for downloading and processing OverDrive audiobooks with proper chapter support.

## Features

- Download audiobooks from ODM files
- Extract chapters from OverDrive MP3 files
- Process audiobooks into properly chaptered files
- Return borrowed books
- Import processed files to media library (supports beets)

## Requirements

- Python 3.8 or higher
- ffmpeg (for audio processing)
- beets (optional, for library management)

## Installation

1. Make sure you have the requirements installed:
   ```bash
   # On Ubuntu/Debian
   sudo apt install ffmpeg

   # On macOS with Homebrew
   brew install ffmpeg

   # Optional: Install beets
   pip install beets
   ```

2. Install the package:
   ```bash
   pip install .
   ```

## Usage

### Basic Usage

1. Download and process in one step:
   ```bash
   overdrive-tools download -p -i beets book.odm
   ```

2. Or use the separate steps for better chapter handling:
   ```bash
   # First download
   overdrive-tools download book.odm

   # Then extract chapters and process
   overdrive-tools extract -p -i beets "Author - Book Title"
   ```

### Available Commands

- `download`: Download audiobooks from ODM files
  ```bash
  overdrive-tools download [-p] [-c] [-i beets] book.odm
  ```

- `extract`: Extract chapters from OverDrive MP3 files
  ```bash
  overdrive-tools extract [-p] [-c] [-i beets] "Author - Book Title"
  ```

- `process`: Process downloaded audiobooks
  ```bash
  overdrive-tools process [-c] [-i beets] "Author - Book Title"
  ```

- `return`: Return borrowed audiobooks
  ```bash
  overdrive-tools return book.odm
  ```

### Command Options

- `-p, --process`: Process chapters after downloading/extracting
- `-c, --cleanup`: Clean up original files after processing
- `-i, --import-to`: Import to media library after processing (currently supports 'beets')
- `-o, --output-format`: Custom output directory format (default: @AUTHOR - @TITLE)

## Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/overdrive-tools.git
   cd overdrive-tools
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Acknowledgments and Credits

This project builds upon and integrates work from several excellent projects:

- [overdrive](https://github.com/chbrown/overdrive) by [chbrown](https://github.com/chbrown) - Original inspiration and base code for ODM file processing and downloading
- [audiobook_chapters](https://github.com/choc96208/audiobook_chapters) by [choc96208](https://github.com/choc96208) - Chapter extraction methodology from OverDrive MP3 files

These projects provided essential insights and methodologies for handling OverDrive audiobooks and chapter extraction.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
