import time
from pathlib import Path

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
        filename (str): Path to the HTML file
        
    Returns:
        None
    """
    print(f"Enhancing HTML file with search functionality: {filename}")
    start_time = time.time()
    
    # Define the paths to our static files
    base_dir = Path(__file__).parent
    css_path = base_dir / "static" / "css" / "search.css"
    html_path = base_dir / "static" / "search.html"
    js_path = base_dir / "static" / "js" / "search.js"
    
    # Read the generated HTML
    with open(filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Get components for search functionality
    search_css = f"<style>\n{read_file(css_path)}\n</style>"
    search_html = read_file(html_path)
    search_js = f"<script type=\"text/javascript\">\n{read_file(js_path)}\n</script>"
    
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
