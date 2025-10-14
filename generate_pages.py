#!/usr/bin/env python3
"""
Script to generate GitHub Pages for the GPU kernels repository.
Creates an index page and individual pages for each day's work.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


def parse_readme() -> Dict[int, str]:
    """Parse README.md and extract descriptions for each day."""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("README.md not found!")
        return {}
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract day sections using regex
    day_descriptions = {}
    
    # Pattern to match day sections (handles both ## Day X and # Day X)
    pattern = r'(?:^|\n)(#{1,2})\s+Day\s+(\d+)(?:\s*:\s*|\s*\n)(.*?)(?=(?:\n#{1,2}\s+Day\s+\d+|\Z))'
    
    matches = re.finditer(pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        day_num = int(match.group(2))
        description = match.group(3).strip()
        day_descriptions[day_num] = description
    
    return day_descriptions


def get_day_files(day_num: int) -> List[Tuple[str, str]]:
    """Get all code files in a day directory."""
    day_dir = Path(f"day {day_num:02d}")
    
    if not day_dir.exists():
        return []
    
    code_files = []
    code_extensions = {'.cu', '.cpp', '.c', '.h', '.cuh', '.py', '.md'}
    
    for file_path in day_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in code_extensions:
            rel_path = file_path.relative_to(day_dir)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                code_files.append((str(rel_path), content))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return code_files


def get_language(filename: str) -> str:
    """Get Prism.js language identifier from filename."""
    ext_map = {
        '.cu': 'cuda',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.cuh': 'cuda',
        '.py': 'python',
        '.md': 'markdown'
    }
    ext = Path(filename).suffix
    return ext_map.get(ext, 'clike')


def generate_day_page(day_num: int, description: str, files: List[Tuple[str, str]]) -> str:
    """Generate HTML content for a single day page."""
    
    files_html = ""
    if files:
        for filename, content in files:
            lang = get_language(filename)
            escaped_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            files_html += f'''
    <div class="file-section">
        <h3>{filename}</h3>
        <pre><code class="language-{lang}">{escaped_content}</code></pre>
    </div>
'''
    else:
        files_html = '<p class="no-files">No code files found for this day.</p>'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {day_num} - GPU Kernels Learning Journey</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .nav {{
            background: white;
            padding: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .nav-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .nav a {{
            color: #667eea;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        
        .nav a:hover {{
            background: #667eea;
            color: white;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .description {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }}
        
        .description h2 {{
            color: #667eea;
            margin-bottom: 1rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }}
        
        .description pre {{
            background: #f5f5f5;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
        }}
        
        .file-section {{
            background: white;
            margin-bottom: 2rem;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .file-section h3 {{
            background: #667eea;
            color: white;
            padding: 1rem;
            margin: 0;
        }}
        
        .file-section pre {{
            margin: 0;
            border-radius: 0;
        }}
        
        .file-section code {{
            display: block;
            padding: 1.5rem;
            max-height: 600px;
            overflow: auto;
        }}
        
        .no-files {{
            text-align: center;
            padding: 3rem;
            color: #999;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .nav-content {{
                flex-direction: column;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Day {day_num}</h1>
        <div class="subtitle">GPU Kernels Learning Journey</div>
    </div>
    
    <nav class="nav">
        <div class="nav-content">
            <a href="index.html">← Back to Index</a>
            <div>
                {f'<a href="day-{day_num-1}.html">← Day {day_num-1}</a>' if day_num > 1 else ''}
                {f'<a href="day-{day_num+1}.html">Day {day_num+1} →</a>' if day_num < 100 else ''}
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="description">
            <h2>Description</h2>
            <div class="desc-content">
{description if description else '<p>No description available for this day.</p>'}
            </div>
        </div>
        
        <h2 style="margin-bottom: 1rem; color: #667eea;">Code Files</h2>
{files_html}
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markdown.min.js"></script>
</body>
</html>'''
    
    return html


def generate_index_page(day_descriptions: Dict[int, str]) -> str:
    """Generate the main index page."""
    
    # Generate day cards
    day_cards = ""
    for day_num in range(1, 101):
        desc = day_descriptions.get(day_num, "")
        # Get first line or first sentence as preview
        preview = ""
        if desc:
            lines = desc.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    preview = line[:150] + ('...' if len(line) > 150 else '')
                    break
        
        if not preview:
            preview = "Click to view details"
        
        day_cards += f'''
        <div class="day-card">
            <div class="day-number">Day {day_num}</div>
            <div class="day-preview">{preview}</div>
            <a href="day-{day_num}.html" class="day-link">View Details →</a>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPU Kernels - 100 Days Learning Journey</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 1rem;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }}
        
        .hero p {{
            font-size: 1.3rem;
            opacity: 0.95;
            max-width: 800px;
            margin: 0 auto 2rem;
        }}
        
        .hero .links {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .hero .links a {{
            color: white;
            text-decoration: none;
            padding: 0.8rem 1.5rem;
            border: 2px solid white;
            border-radius: 5px;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .hero .links a:hover {{
            background: white;
            color: #667eea;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 1rem;
        }}
        
        .section-title {{
            text-align: center;
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 3rem;
            font-weight: 700;
        }}
        
        .day-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }}
        
        .day-card {{
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
        }}
        
        .day-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
        }}
        
        .day-number {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .day-preview {{
            color: #666;
            flex-grow: 1;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        
        .day-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            display: inline-block;
        }}
        
        .day-link:hover {{
            color: #764ba2;
            transform: translateX(5px);
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem 1rem;
            margin-top: 4rem;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .hero p {{
                font-size: 1.1rem;
            }}
            
            .section-title {{
                font-size: 2rem;
            }}
            
            .day-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>🚀 GPU Kernels Learning Journey</h1>
        <p>A 100-day journey of learning GPU programming and parallel computing with CUDA, HIP, and more</p>
        <div class="links">
            <a href="https://github.com/douyixuan/gpu-kernels" target="_blank">GitHub Repository</a>
            <a href="https://hamdi.bearblog.dev/" target="_blank">Blog</a>
        </div>
    </div>
    
    <div class="container">
        <h2 class="section-title">100 Days of GPU Programming</h2>
        <div class="day-grid">
{day_cards}
        </div>
    </div>
    
    <div class="footer">
        <p>Created as part of the 100 Days GPU Programming Challenge</p>
        <p>Mentor: <a href="https://github.com/hkproj/" target="_blank">hkproj</a> | 
           Challenge Partner: <a href="https://github.com/1y33/100Days" target="_blank">1y33</a></p>
    </div>
</body>
</html>'''
    
    return html


def main():
    """Main function to generate all pages."""
    print("Parsing README.md...")
    day_descriptions = parse_readme()
    print(f"Found descriptions for {len(day_descriptions)} days")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Generate index page
    print("Generating index page...")
    index_html = generate_index_page(day_descriptions)
    with open(docs_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✓ Generated index.html")
    
    # Generate individual day pages
    print("\nGenerating day pages...")
    for day_num in range(1, 101):
        description = day_descriptions.get(day_num, "")
        files = get_day_files(day_num)
        
        day_html = generate_day_page(day_num, description, files)
        
        with open(docs_dir / f"day-{day_num}.html", 'w', encoding='utf-8') as f:
            f.write(day_html)
        
        print(f"✓ Generated day-{day_num}.html ({len(files)} files)")
    
    print(f"\n✅ Successfully generated all pages in {docs_dir}/")


if __name__ == "__main__":
    main()
