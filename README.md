# uLauncher SVGL Search

A simple [uLauncher](https://ulauncher.io/) extension to search SVG logos from the [SVGL API](https://svgl.app/) and copy the raw SVG code to your clipboard.

---

## Features

- Triggered by a keyword (default: `svg`)
- Live search of SVG logos by name using the SVGL REST API
- Preview thumbnails of SVGs in results
- Copy full SVG XML markup to clipboard with one keystroke

---

## Installation
**Open the extension GUI**
    - Open uLauncher Preferences → Extensions
    - Click Add Extension. Paste https://github.com/Shine1i/ulauncher-svgl
    - Find **uLauncher SVGL Search** and click “Start” if it’s stopped
     

---

## Usage

1. Press your uLauncher hotkey (e.g. `Ctrl + Space`).
2. Type:
   ```
   svg <search term>
   ```
3. Browse the results with ↑/↓. Each result shows:
    - A small SVG thumbnail
    - The logo name (and optional category)
4. Press **Enter** on your choice to copy the SVG code to the clipboard.
5. Paste anywhere you need your SVG (editors, HTML, Markdown, etc.).

---

## Configuration

You can customize the trigger keyword:

1. Open **Preferences → Extensions → uLauncher SVGL Search**.
2. Edit the **SVG Logo Search** keyword (default: `svg`).
3. Restart uLauncher to apply changes.

---

## Development

- **Entry point**: `main.py`
- **Keyword event**: listens for `KeywordQueryEvent`
- **API calls**: uses the SVGL REST API (`https://api.svgl.app?search=<term>`)
- **Dependencies**:
    - Python 3 standard library (`requests`, `json`, `os`)
    - uLauncher’s built-in extension API

---

## References & Sources

- **uLauncher Extension Docs**  
  https://docs.ulauncher.io/en/stable/
- **uLauncher Sample Extensions**
    - Emoji extension example for keyword events & copy actions
- **SVGL API Documentation**  
  https://svgl.app/api
- **SVGL Website**  
  https://svgl.app/

---

