#!/usr/bin/env python3
"""
Convert Markdown files to HTML with consistent styling
"""

import os
import re
from pathlib import Path

def escape_html(text):
    """Escape HTML special characters"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def convert_md_to_html(md_content, title, breadcrumb_path=""):
    """Convert markdown content to HTML"""

    # Split into lines for processing
    lines = md_content.split('\n')
    html_lines = []
    in_code_block = False
    code_language = ''
    in_list = False
    in_ordered_list = False
    in_blockquote = False
    in_table = False
    table_headers = []

    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                code_language = line.strip()[3:].strip()
                html_lines.append('<pre><code>')
                in_code_block = True
            else:
                html_lines.append('</code></pre>')
                in_code_block = False
            continue

        if in_code_block:
            html_lines.append(escape_html(line))
            continue

        # Handle tables
        if '|' in line and not in_code_block:
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                # Parse headers
                headers = [h.strip() for h in line.split('|')[1:-1]]
                html_lines.append('<thead><tr>')
                for header in headers:
                    html_lines.append(f'<th>{header}</th>')
                html_lines.append('</tr></thead><tbody>')
                table_headers = headers
                continue
            elif line.strip().startswith('|---') or line.strip().startswith('|-'):
                # Skip separator line
                continue
            else:
                # Table row
                cells = [c.strip() for c in line.split('|')[1:-1]]
                html_lines.append('<tr>')
                for cell in cells:
                    html_lines.append(f'<td>{process_inline_md(cell)}</td>')
                html_lines.append('</tr>')
                continue
        elif in_table and '|' not in line:
            html_lines.append('</tbody></table>')
            in_table = False

        # Handle headers
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            # Create ID from text for linking
            link_id = text.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
            html_lines.append(f'<h{level} id="{link_id}">{process_inline_md(text)}</h{level}>')
            continue

        # Handle blockquotes
        if line.strip().startswith('>'):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            text = line.strip()[1:].strip()
            html_lines.append(f'<p>{process_inline_md(text)}</p>')
            continue
        elif in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False

        # Handle lists
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = line.strip()[2:].strip()
            html_lines.append(f'<li>{process_inline_md(text)}</li>')
            continue
        elif in_list and not line.strip().startswith('-') and not line.strip().startswith('*'):
            html_lines.append('</ul>')
            in_list = False

        # Handle ordered lists
        if re.match(r'^\d+\.\s', line.strip()):
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
            text = re.sub(r'^\d+\.\s', '', line.strip())
            html_lines.append(f'<li>{process_inline_md(text)}</li>')
            continue
        elif in_ordered_list and not re.match(r'^\d+\.\s', line.strip()):
            html_lines.append('</ol>')
            in_ordered_list = False

        # Handle horizontal rules
        if line.strip() in ['---', '***', '___']:
            html_lines.append('<hr>')
            continue

        # Handle empty lines
        if not line.strip():
            html_lines.append('')
            continue

        # Regular paragraphs
        html_lines.append(f'<p>{process_inline_md(line)}</p>')

    # Close any open tags
    if in_code_block:
        html_lines.append('</code></pre>')
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    if in_blockquote:
        html_lines.append('</blockquote>')
    if in_table:
        html_lines.append('</tbody></table>')

    html_body = '\n'.join(html_lines)

    # Create full HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Coding Challenges</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav-bar">
        <div class="nav-content">
            <a href="../index.html" class="nav-brand">
                🚀 AI Coding Challenges
            </a>
            <ul class="nav-links">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../quick-start.html">Quick Start</a></li>
                <li><a href="../ai-modes-guide.html">AI Modes</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">Home</a>
            {breadcrumb_path}
        </div>

        <div class="content-wrapper">
            {html_body}
        </div>

        <div class="footer">
            <p><a href="../index.html">← Back to Documentation Hub</a></p>
            <p>AI-Augmented Coding Challenge Framework | Version: 1.0</p>
        </div>
    </div>
</body>
</html>"""

    return html_template

def process_inline_md(text):
    """Process inline markdown formatting"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    # Checkboxes
    text = text.replace('- [ ]', '☐')
    text = text.replace('- [x]', '☑')
    text = text.replace('- [X]', '☑')

    # Emoji shortcuts (common ones)
    emoji_map = {
        ':check_mark:': '✅',
        ':x:': '❌',
        ':warning:': '⚠️',
        ':information_source:': 'ℹ️',
        ':rocket:': '🚀',
        ':book:': '📖',
        ':hammer_and_wrench:': '🛠️',
    }
    for shortcode, emoji in emoji_map.items():
        text = text.replace(shortcode, emoji)

    return text

def main():
    """Main conversion function"""
    base_dir = Path(__file__).parent

    # Define files to convert (md_path, html_path, title, breadcrumb)
    conversions = [
        ('QUICK-START.md', 'quick-start.html', 'Quick Start Guide', ''),
        ('PROBLEM-STATEMENT.md', 'problem-statement.html', 'Problem Statement', ''),
        ('challenges/challenge-1-legacy-modernization/README.md',
         'challenges/challenge-1.html', 'Challenge 1: Legacy Modernization',
         '<span>→</span> <a href="../challenges/">Challenges</a> <span>→</span> Challenge 1'),
        ('challenges/challenge-2-distributed-systems/README.md',
         'challenges/challenge-2.html', 'Challenge 2: Distributed Systems',
         '<span>→</span> <a href="../challenges/">Challenges</a> <span>→</span> Challenge 2'),
        ('challenges/challenge-3-security-performance/README.md',
         'challenges/challenge-3.html', 'Challenge 3: Security & Performance',
         '<span>→</span> <a href="../challenges/">Challenges</a> <span>→</span> Challenge 3'),
        ('evaluation/scoring-guide.md', 'evaluation/scoring-guide.html',
         'Scoring & Evaluation Guide',
         '<span>→</span> <a href="../evaluation/">Evaluation</a> <span>→</span> Scoring Guide'),
        ('research/ai-coding-effectiveness.md', 'research/ai-effectiveness.html',
         'AI Coding Effectiveness Research',
         '<span>→</span> <a href="../research/">Research</a> <span>→</span> AI Effectiveness'),
        ('templates/submission-template.md', 'templates/submission-template.html',
         'Submission Template',
         '<span>→</span> <a href="../templates/">Templates</a> <span>→</span> Submission'),
        ('templates/ai-usage-log-template.md', 'templates/ai-usage-log.html',
         'AI Usage Log Template',
         '<span>→</span> <a href="../templates/">Templates</a> <span>→</span> AI Usage Log'),
    ]

    for md_path, html_path, title, breadcrumb in conversions:
        md_file = base_dir / md_path
        html_file = base_dir / html_path

        if not md_file.exists():
            print(f"⚠️  Skipping {md_path} (not found)")
            continue

        print(f"Converting {md_path} → {html_path}")

        # Read markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert to HTML
        html_content = convert_md_to_html(md_content, title, breadcrumb)

        # Ensure output directory exists
        html_file.parent.mkdir(parents=True, exist_ok=True)

        # Write HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Created {html_path}")

    print("\n🎉 Conversion complete!")

if __name__ == '__main__':
    main()
