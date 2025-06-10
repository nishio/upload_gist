# gist-uploader

A lightweight Python library and CLI tool for uploading files to GitHub Gist.

## Features

- 📁 Upload files or stdin content to GitHub Gist
- 🔒 Create private (secret) or public gists
- ✏️ Update existing gists
- 🎨 JSON formatting support (pretty-print or minify)
- 🐍 Use as Python library or CLI tool
- ⚡ Minimal dependencies (only `requests`)

## Installation

### From PyPI (recommended)

```bash
pip install gist-uploader
```

### From source

```bash
git clone https://github.com/nishio/upload_gist.git
cd upload_gist
pip install -e .
```

## Setup

You need a GitHub Personal Access Token with `gist` scope:

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token with `gist` scope
3. Set it as environment variable:

```bash
export GIST_TOKEN="your_token_here"
# or
export GITHUB_TOKEN="your_token_here"
```

## Usage

### CLI Examples

```bash
# Upload a file as private gist
python -m gist_uploader path/to/report.md

# Upload from stdin as public gist
echo "Hello, World!" | python -m gist_uploader -f hello.txt --public

# Update existing gist
python -m gist_uploader summary.txt --gist-id abc123def456

# Pretty-print JSON with indentation
cat data.json | python -m gist_uploader -f data.json --indent 2

# Minify JSON
cat data.json | python -m gist_uploader -f data.json --raw-json
```

### Library Usage

```python
from gist_uploader import upload_to_gist

# Create a private gist
result = upload_to_gist(
    content="Hello, World!",
    filename="hello.txt",
    public=False
)
print(f"Gist URL: {result['html_url']}")

# Update existing gist
result = upload_to_gist(
    content="Updated content",
    filename="hello.txt",
    gist_id="abc123def456"
)
```

### Environment Variables

- `GIST_TOKEN` or `GITHUB_TOKEN`: GitHub personal access token
- `GIST_ID`: Default gist ID for updates (optional)

### CLI Options

```
usage: python -m gist_uploader [-h] [-f FILENAME] [-d DESCRIPTION] [--public]
                               [--gist-id GIST_ID] [--token TOKEN]
                               [--indent N | --raw-json]
                               [path]

positional arguments:
  path                  Path of the file to upload. If omitted, read from STDIN.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Filename stored in the gist (defaults to basename or stdin.txt).
  -d DESCRIPTION, --description DESCRIPTION
                        Gist description. Uses a timestamp if omitted.
  --public              Create a *public* gist.
  --gist-id GIST_ID     Update an existing gist instead of creating new.
  --token TOKEN         GitHub token (overrides environment variable).
  --indent N            Pretty‑print JSON with indentation N (detects JSON).
  --raw-json            Treat input as *raw* JSON and upload minified.
```

## GitHub Actions Integration

```yaml
name: Upload Report to Gist

on:
  workflow_dispatch:

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install gist-uploader
      run: pip install gist-uploader
    
    - name: Upload to Gist
      env:
        GIST_TOKEN: ${{ secrets.GIST_TOKEN }}  # PAT with gist scope
      run: |
        python -m gist_uploader report.json --public
```

**Note**: GitHub Actions' default `GITHUB_TOKEN` doesn't have `gist` scope. Create a separate Personal Access Token with `gist` scope and add it as `GIST_TOKEN` secret.

## Development

```bash
# Clone and setup
git clone https://github.com/nishio/upload_gist.git
cd upload_gist

# Install in development mode
pip install -e .

# Run tests
pip install pytest
pytest

# Build package
pip install build
python -m build
```

## License

MIT License
