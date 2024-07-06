
# Code to PDF Converter

This project converts code files to PDF with syntax highlighting. It supports multiple file types and uses `wkhtmltopdf` for PDF conversion.

## Prerequisites

- Python 3.x
- `wkhtmltopdf` (The script will attempt to download and install it if not found)

## Setup

1. Clone the repository or download the project folder.
2. Navigate to the project directory.
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Ensure the `config.json` file is correctly configured with the path to `wkhtmltopdf` and the desired file types.

## Running the Converter

Run the converter script:

```sh
python converter.py
```

You will be prompted to enter the project directory, output directory, and the path to the configuration file.

## Configuration

The `config.json` file should look like this:

```json
{
    "pdfkit_path": "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
    "file_types": {
        "java": "Java/Kotlin Class",
        "kt": "Kotlin Class",
        "xml": "XML [Extensible Markup Language]",
        "py": "Python Script",
        "js": "JavaScript File",
        "html": "HTML File",
        "css": "CSS File",
        "json": "JSON [JavaScript Object Notation]",
        "md": "Markdown Document",
        "sh": "Shell Script",
        "bat": "Batch Script",
        "rb": "Ruby Script",
        "php": "PHP Script",
        "pl": "Perl Script",
        "c": "C Source File",
        "cpp": "C++ Source File",
        "cs": "C# Source File",
        "go": "Go Source File",
        "rs": "Rust Source File",
        "swift": "Swift Source File",
        "ts": "TypeScript File",
        "r": "R Script",
        "m": "MATLAB Script",
        "sql": "SQL File",
        "yml": "YAML File",
        "tex": "LaTeX Document"
    }
}
```

## Troubleshooting

- Ensure `wkhtmltopdf` is correctly installed.
- Ensure the paths provided are correctly formatted.
- Check the log file in the output directory for any errors.

## Developer

- Itamar Itzhaki - [GitHub](https://github.com/CMOSfail)
