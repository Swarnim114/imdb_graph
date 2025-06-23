import time
from pathlib import Path
import os

# Import from the package
from imdb_graph.utils.constants import PROJECT_ROOT

# Path to static resources
STATIC_DIR = Path(__file__).parent.parent / "static"
CSS_FILE = STATIC_DIR / "css" / "search.css"
JS_FILE = STATIC_DIR / "js" / "search.js"

def read_file(path):
    """Read the contents of a file.
    
    Args:
        path (str): Path to the file
        
    Returns:
        str: File contents
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def enhance_html_with_search(filename):
    """Enhance the HTML file with search functionality.
    
    Args:
        filename (str or Path): Path to the HTML file
        
    Returns:
        None
    """
    # Convert to string if it's a Path object
    if not isinstance(filename, str):
        filename = str(filename)
        
    print(f"Enhancing HTML file with search functionality: {filename}")
    start_time = time.time()
    
    # Define search HTML
    search_html = """
<div id="searchContainer">
  <div style="width: 100%; margin-bottom: 10px;">
    <h3 style="margin: 0 0 8px 0; color: white; font-size: 18px; font-weight: 500;">Movie Explorer</h3>
    <div class="searchDescription">Search the graph by movie title</div>
  </div>
  <div style="display: flex; width: 100%; gap: 10px;">
    <input type="text" id="searchInput" placeholder="Search for a movie...">
    <button id="searchBtn">Search</button>
  </div>
</div>
<div id="searchResults"></div>
    """
    
    # Read the generated HTML
    with open(filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Get components for search functionality
    search_css = f"<style>\n{read_file(CSS_FILE)}\n</style>"
    search_js = f"<script type=\"text/javascript\">\n{read_file(JS_FILE)}\n</script>"
    
    # Inject our search HTML into the body
    enhanced_html = html_content.replace('<body>', f'<body>\n{search_html}')
    # Inject our CSS into the head
    enhanced_html = enhanced_html.replace('</head>', f'{search_css}\n</head>')
    # Inject our JS at the end of the body
    enhanced_html = enhanced_html.replace('</body>', f'{search_js}\n</body>')
    
    # Write the modified HTML back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"HTML file enhanced in {time.time() - start_time:.2f} seconds")
