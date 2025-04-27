import json
import os
import requests

# Standard headers for API requests to avoid 304
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://svgl.app',
    'Referer': 'https://svgl.app/',
}

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


class SVGLSearchExtension(Extension):
    def __init__(self):
        super(SVGLSearchExtension, self).__init__()
        # Subscribe to keyword query events
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        query = query.strip()
        items = []

        if len(query) == 0:
            # No search term entered yet; show a hint
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Type a logo name to search...',
                description='e.g. svg firefox',
                on_enter=DoNothingAction()
            ))
            return RenderResultListAction(items)

        # Build the API URL
        api_url = f"https://api.svgl.app/?search={query}"

        try:
            # Fetch data from API
            response = requests.get(api_url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            results = response.json()
        except Exception as e:
            # Handle errors (network issue or JSON parse error)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Error searching for SVGs',
                description=f'Error: {str(e)}',
                on_enter=DoNothingAction()
            ))
            return RenderResultListAction(items)

        if not results:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='No matching SVG logos found',
                description='Try a different search term.',
                on_enter=DoNothingAction()
            ))
            return RenderResultListAction(items)

        # Create a temp directory for SVG files
        temp_dir = "/tmp/ulauncher_svgl_search"
        os.makedirs(temp_dir, exist_ok=True)

        # Process results (limit to first 10 for performance)
        for entry in results[:10]:
            # Get the SVG URL
            route = entry.get("route", "")
            if isinstance(route, dict):
                svg_url = route.get("light") or route.get("dark") or next(iter(route.values()))
            else:
                svg_url = route

            # Skip if no valid URL
            if not svg_url:
                continue

            # Get name and description
            name = entry.get("title", "Unknown")
            desc = entry.get("category", "")
            if isinstance(desc, list):
                desc = ", ".join(desc)
            if desc:
                desc = f"Category: {desc}"
            else:
                # If no category, use the brand URL domain
                url = entry.get("url", "")
                desc = f"Source: {url}" if url else ""

            # Download SVG content
            svg_data = None
            if svg_url.startswith(('http://', 'https://')):
                try:
                    svg_response = requests.get(svg_url, headers=HEADERS, timeout=5)
                    svg_response.raise_for_status()
                    svg_data = svg_response.content
                except:
                    svg_data = None

            if svg_data:
                # Save to a temp file
                temp_path = f"{temp_dir}/svg_{name.lower().replace(' ', '_')}.svg"
                with open(temp_path, "wb") as f:
                    f.write(svg_data)
                icon_path = temp_path
                svg_text = svg_data.decode('utf-8')
            else:
                # Fallback to extension icon if image fetch failed
                icon_path = "images/icon.png"
                svg_text = ""

            # Add result item
            items.append(ExtensionResultItem(
                icon=icon_path,
                name=name,
                description=desc,
                on_enter=CopyToClipboardAction(svg_text)
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    SVGLSearchExtension().run()
