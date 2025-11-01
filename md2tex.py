import re
import sys
import os

# Remove emoji/sticker characters by Unicode ranges (flags, emoticons, pictographs, dingbats, etc.)
EMOJI_RE = re.compile('[\U0001F1E6-\U0001F1FF'  # Flags
                      '\U0001F300-\U0001F5FF'   # Misc Symbols & Pictographs
                      '\U0001F600-\U0001F64F'   # Emoticons
                      '\U0001F680-\U0001F6FF'   # Transport & Map
                      '\U0001F700-\U0001F77F'   # Alchemical Symbols
                      '\U0001F780-\U0001F7FF'   # Geometric Shapes Extended
                      '\U0001F800-\U0001F8FF'   # Supplemental Arrows-C
                      '\U0001F900-\U0001F9FF'   # Supplemental Symbols & Pictographs
                      '\U0001FA00-\U0001FA6F'   # Symbols & Pictographs (part)
                      '\U0001FA70-\U0001FAFF'   # Symbols & Pictographs Extended-A
                      '\U00002600-\U000026FF'   # Misc Symbols
                      '\U00002700-\U000027BF'   # Dingbats
                      '\U0001F3FB-\U0001F3FF'   # Skin tone modifiers
                      '\U0000200D'               # Zero Width Joiner
                      '\U0000FE0F]')             # Variation Selector-16

def _strip_emojis(text: str) -> str:
    return EMOJI_RE.sub('', text)

def escape_latex(text):
    if not text:
        return ''
    text = str(text)
    # Remove all emoji/sticker characters early
    text = _strip_emojis(text)
    
    text = text.replace('\\', ' BACKSLASHTEMP ')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace(' BACKSLASHTEMP ', '\\textbackslash{}')
    
    unicode_map = {
        '—': '---', '–': '--',
        'α': r'$\alpha$', 'β': r'$\beta$', 'γ': r'$\gamma$', 
        'δ': r'$\delta$', 'ε': r'$\varepsilon$', 'ζ': r'$\zeta$',
        'η': r'$\eta$', 'θ': r'$\theta$', 'λ': r'$\lambda$',
        'μ': r'$\mu$', 'π': r'$\pi$', 'σ': r'$\sigma$',
        'τ': r'$\tau$', 'φ': r'$\varphi$', 'ω': r'$\omega$',
        'Γ': r'$\Gamma$', 'Δ': r'$\Delta$', 'Θ': r'$\Theta$',
        'Λ': r'$\Lambda$', 'Ξ': r'$\Xi$', 'Π': r'$\Pi$',
        'Σ': r'$\Sigma$', 'Φ': r'$\Phi$', 'Ψ': r'$\Psi$',
        'Ω': r'$\Omega$', 'ν': r'$\nu$',
        '±': r'$\pm$', '∓': r'$\mp$', '×': r'$\times$', 
        '÷': r'$\div$', '√': r'$\sqrt{}$', '∞': r'$\infty$', 
        '≈': r'$\approx$', '≠': r'$\neq$', '≤': r'$\leq$', 
        '≥': r'$\geq$', '≡': r'$\equiv$', '∝': r'$\propto$',
        '∫': r'$\int$', '∑': r'$\sum$', '∏': r'$\prod$',
        '∂': r'$\partial$', '∇': r'$\nabla$', '∮': r'$\oint$',
        '∛': r'$\sqrt[3]{}$', '∜': r'$\sqrt[4]{}$', '∆': r'$\Delta$',
        '→': r'$\rightarrow$', '←': r'$\leftarrow$',
        '↑': r'$\uparrow$', '↓': r'$\downarrow$',
        '↔': r'$\leftrightarrow$', '⇒': r'$\Rightarrow$',
        '⇐': r'$\Leftarrow$', '⇔': r'$\Leftrightarrow$',
        '∩': r'$\cap$', '∪': r'$\cup$',
        '⊂': r'$\subset$', '⊃': r'$\supset$',
        '⊆': r'$\subseteq$', '⊇': r'$\supseteq$',
        '∈': r'$\in$', '∉': r'$\notin$',
        '°': r'$^\circ$', '∙': r'$\cdot$', '⋅': r'$\cdot$',
        '©': r'\textcopyright{}', '®': r'\textregistered{}',
        '™': r'\texttrademark{}',
        '€': r'\texteuro{}', '£': r'\pounds{}', 
        '¥': r'\textyen{}', '¢': r'\textcent{}',
        '§': r'\S{}', '¶': r'\P{}',
        '†': r'\dag{}', '‡': r'\ddag{}',
        '•': r'\textbullet{}', '‰': r'\textperthousand{}',
        '′': r'$\prime$', '″': r'$\prime\prime$', 
        '‴': r'$\prime\prime\prime$',
        '⁰': r'$^0$', '¹': r'$^1$', '²': r'$^2$', '³': r'$^3$',
        '⁴': r'$^4$', '⁵': r'$^5$', '⁶': r'$^6$', '⁷': r'$^7$',
        '⁸': r'$^8$', '⁹': r'$^9$', '⁻': r'$^-$',
    }
    
    for char, replacement in unicode_map.items():
        text = text.replace(char, replacement)
    
    return text

def process_inline(text):
    if not text:
        return ''
    # Protect double-dollar text to render literally (e.g., $$block$$)
    dd_tokens = []
    def _protect_dd(m):
        dd_tokens.append(m.group(1))
        return f"DDTOKEN{len(dd_tokens)-1}"
    text = re.sub(r"\$\$([^$]+)\$\$", _protect_dd, text)

    parts = []
    current = 0
    
    while current < len(text):
        dollar_match = re.search(r'\$([^\$]+)\$', text[current:])
        
        if dollar_match:
            before_match = text[current:current + dollar_match.start()]
            before_match = _process_formats(before_match)
            parts.append(before_match)
            parts.append('$' + dollar_match.group(1) + '$')
            current = current + dollar_match.end()
        else:
            remaining = text[current:]
            remaining = _process_formats(remaining)
            parts.append(remaining)
            break
    
    out = ''.join(parts)
    # Restore protected $$...$$ as literal text with escaped dollars
    for i, val in enumerate(dd_tokens):
        out = out.replace(f"DDTOKEN{i}", f"\\$\\${escape_latex(val)}\\$\\$")
    return out

def _process_formats(text):
    result = []
    pos = 0
    
    for match in re.finditer(r'`([^`]+)`|\*\*([^\*]+)\*\*|\[([^\]]+)\]\(([^\)]+)\)', text):
        result.append(escape_latex(text[pos:match.start()]))
        
        if match.group(1):  # code
            code = _strip_emojis(match.group(1))
            code = code.replace('\\', 'BACKSLASHTEMP')
            code = code.replace('{', '\\{')
            code = code.replace('}', '\\}')
            code = code.replace('BACKSLASHTEMP', '\\textbackslash{}')
            code = code.replace('_', '\\_')
            code = code.replace('^', '\\textasciicircum{}')
            code = code.replace('#', '\\#')
            code = code.replace('&', '\\&')
            code = code.replace('%', '\\%')
            code = code.replace('$', '\\$')
            result.append('\\texttt{' + code + '}')
        elif match.group(2):  # bold
            result.append('\\textbf{' + escape_latex(match.group(2)) + '}')
        elif match.group(3):  # link
            result.append('\\href{' + match.group(4) + '}{' + escape_latex(match.group(3)) + '}')
        
        pos = match.end()
    
    result.append(escape_latex(text[pos:]))
    return ''.join(result)

def _clean_heading_text(text: str) -> str:
    # Remove leading emojis/symbols then a leading numeric prefix like '1.' or '2) '
    t = text.strip()
    # Strip leading non-alnum symbols (common emojis or bullets) with following spaces
    t = re.sub(r'^[^\w\d]+\s*', '', t)
    # Strip leading numbering patterns like '1. ', '2) '
    t = re.sub(r'^\d+[\.)]\s+', '', t)
    return t

def process_table_cell(cell):
    if not cell:
        return ''
    
    parts = []
    current_pos = 0
    
    for match in re.finditer(r'\$([^\$]+)\$|`([^`]+)`|\*\*([^\*]+)\*\*', cell):
        before = cell[current_pos:match.start()]
        parts.append(escape_latex(before))
        
        if match.group(1):
            parts.append('$' + match.group(1) + '$')
        elif match.group(2):
            code = _strip_emojis(match.group(2))
            code = code.replace('\\', 'BACKSLASHTEMP')
            code = code.replace('{', '\\{')
            code = code.replace('}', '\\}')
            code = code.replace('BACKSLASHTEMP', '\\textbackslash{}')
            code = code.replace('_', '\\_')
            code = code.replace('^', '\\textasciicircum{}')
            code = code.replace('#', '\\#')
            code = code.replace('&', '\\&')
            code = code.replace('%', '\\%')
            code = code.replace('$', '\\$')
            parts.append('\\texttt{' + code + '}')
        elif match.group(3):
            parts.append('\\textbf{' + escape_latex(match.group(3)) + '}')
        
        current_pos = match.end()
    
    parts.append(escape_latex(cell[current_pos:]))
    
    return ''.join(parts)

def md_to_latex(md_text, engine: str = 'pdflatex', system_name: str = None):
    lines = md_text.split('\n')
    result = []
    in_code_block = False
    ul_level = 0  # number of open itemize levels
    ol_level = 0  # number of open enumerate levels
    in_math_block = False
    in_bracket_math = False
    code_block_content = []
    math_block_content = []
    bracket_math_content = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('$$') and not in_code_block and not in_bracket_math:
            if in_math_block:
                result.append('\\[')
                result.extend(math_block_content)
                result.append('\\]')
                math_block_content = []
                in_math_block = False
            else:
                in_math_block = True
            i += 1
            continue
        
        if in_math_block:
            math_block_content.append(line)
            i += 1
            continue

        # Support bracketed display math using lines with '[' ... ']'
        if line.strip() == '[' and not in_code_block and not in_math_block:
            in_bracket_math = True
            i += 1
            continue
        if in_bracket_math:
            if line.strip() == ']':
                result.append('\\[')
                result.extend(bracket_math_content)
                result.append('\\]')
                bracket_math_content = []
                in_bracket_math = False
            else:
                bracket_math_content.append(line)
            i += 1
            continue
        
        if line.startswith('```') or line.startswith('~~~'):
            if in_code_block:
                result.append('\\begin{verbatim}')
                for code_line in code_block_content:
                    # Preserve code exactly as written (including Unicode)
                    if len(code_line) > 80:
                        for j in range(0, len(code_line), 75):
                            result.append(code_line[j:j+75])
                    else:
                        result.append(code_line)
                result.append('\\end{verbatim}')
                code_block_content = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        # Helpers to close all open list environments
        def _close_all_lists():
            nonlocal ul_level, ol_level
            while ul_level > 0:
                result.append('\\end{itemize}')
                ul_level -= 1
            while ol_level > 0:
                result.append('\\end{enumerate}')
                ol_level -= 1

        # Horizontal rules (---, ***, ___) -> full-width rule
        if line.strip() in ('---', '***', '___'):
            _close_all_lists()
            result.append('\\noindent\\rule{\\linewidth}{0.4pt}')
            i += 1
            continue

        if '|' in line and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|', lines[i + 1]):
            _close_all_lists()
            
            headers = [h.strip() for h in line.split('|') if h.strip()]
            num_cols = len(headers)
            
            if num_cols == 1:
                col_width = 0.85
            elif num_cols == 2:
                col_width = 0.42
            elif num_cols == 3:
                col_width = 0.28
            elif num_cols == 4:
                col_width = 0.20
            else:
                col_width = 0.85 / num_cols
            
            result.append('\\begin{adjustbox}{max width=\\textwidth}')
            col_spec = '|' + f'p{{{col_width}\\textwidth}}|' * num_cols
            result.append('\\begin{tabular}{' + col_spec + '}')
            result.append('\\hline')
            result.append(' & '.join(escape_latex(h) for h in headers) + ' \\\\')
            result.append('\\hline')
            i += 2
            
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                cells = [c.strip() for c in lines[i].split('|') if c.strip() or lines[i].startswith('|')]
                cells = [c for c in cells if c.strip()]
                
                if len(cells) != num_cols:
                    break
                
                processed_cells = [process_table_cell(cell) for cell in cells]
                result.append(' & '.join(processed_cells) + ' \\\\')
                result.append('\\hline')
                i += 1
            
            result.append('\\end{tabular}')
            result.append('\\end{adjustbox}')
            result.append('')
            continue
        # Nested unordered list items (supports indentation in multiples of 2 spaces)
        m_ul = re.match(r'^(\s*)([-\*])\s+(.*)$', line)
        if m_ul:
            indent = m_ul.group(1)
            content = m_ul.group(3)
            level = len(indent) // 2
            desired = level + 1
            while ul_level < desired:
                while ol_level > 0:
                    result.append('\\end{enumerate}')
                    ol_level -= 1
                result.append('\\begin{itemize}')
                ul_level += 1
            while ul_level > desired:
                result.append('\\end{itemize}')
                ul_level -= 1
            result.append('\\item ' + process_inline(content))
            i += 1
            continue

        # Nested ordered list items
        m_ol = re.match(r'^(\s*)\d+\.\s+(.*)$', line)
        if m_ol:
            indent = m_ol.group(1)
            content = m_ol.group(2)
            level = len(indent) // 2
            desired = level + 1
            while ul_level > 0:
                result.append('\\end{itemize}')
                ul_level -= 1
            while ol_level < desired:
                result.append('\\begin{enumerate}')
                ol_level += 1
            while ol_level > desired:
                result.append('\\end{enumerate}')
                ol_level -= 1
            result.append('\\item ' + process_inline(content))
            i += 1
            continue

        # Headings and paragraphs
        if line.startswith('#### '):
            _close_all_lists()
            heading_text = _clean_heading_text(line[5:])
            result.append('\\paragraph{' + process_inline(heading_text) + '}')
        elif line.startswith('### '):
            _close_all_lists()
            heading_text = _clean_heading_text(line[4:])
            result.append('\\subsubsection{' + process_inline(heading_text) + '}')
        elif line.startswith('## '):
            _close_all_lists()
            heading_text = _clean_heading_text(line[3:])
            result.append('\\subsection{' + process_inline(heading_text) + '}')
        elif line.startswith('# '):
            _close_all_lists()
            heading_text = _clean_heading_text(line[2:])
            result.append('\\section{' + process_inline(heading_text) + '}')
        elif line.strip() == '':
            _close_all_lists()
            result.append('')
        else:
            _close_all_lists()
            processed = process_inline(line)
            # Force a LaTeX line break for every non-block plain-text line.
            # Use \newline for robustness across contexts instead of \\
            if not processed.rstrip().endswith('\\') and not processed.rstrip().endswith('\\newline'):
                processed += ' \\newline'
            result.append(processed)
        
        i += 1
        
    # Close any remaining lists at EOF
        while ul_level > 0:
            result.append('\\end{itemize}')
            ul_level -= 1
        while ol_level > 0:
            result.append('\\end{enumerate}')
            ol_level -= 1
    
    text = '\n'.join(result)
    
    # Engine-specific preamble
    engine_preamble = ''
    if engine in ('xelatex', 'lualatex'):
        # Use fontspec for Unicode; try to set a monospaced font if available
        engine_preamble += "\\usepackage{fontspec}\n"
        engine_preamble += "\\newcommand{\\TrySetMono}[1]{\\IfFontExistsTF{#1}{\\setmonofont{#1}}{}}\n"
        # Try common fonts in order without failing if missing
        engine_preamble += "\\TrySetMono{Consolas}\n\\TrySetMono{DejaVu Sans Mono}\n\\TrySetMono{Fira Code}\n\\TrySetMono{Courier New}\n"
    else:
        # For pdfLaTeX, ensure UTF-8 input handling for non-ASCII outside verbatim
        engine_preamble += "\\usepackage[utf8]{inputenc}\n"

    latex_doc = f"""\\documentclass{{article}}
\\usepackage[margin=0.6in]{{geometry}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{textcomp}}
\\usepackage[official]{{eurosym}}
\\usepackage{{hyperref}}
\\usepackage{{longtable}}
\\usepackage{{array}}
\\usepackage{{adjustbox}}
\\usepackage{{enumitem}}
\\setlength{{\\parindent}}{{0pt}}
\\setlist[itemize]{{leftmargin=2em}}
\\setlist[enumerate]{{leftmargin=2.5em}}
% Number subsubsections as 1, 2, 3 (no parent prefixes like 0.0.1)
\\setcounter{{secnumdepth}}{{3}}
\\renewcommand\\thesubsubsection{{\\arabic{{subsubsection}}}}
{engine_preamble}
\\begin{{document}}

{text}

\\end{{document}}"""
    
    return latex_doc

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Detect if code blocks contain non-ASCII (to decide LaTeX engine)
        def _has_non_ascii_in_code(md: str) -> bool:
            in_code = False
            for ln in md.splitlines():
                if ln.startswith('```') or ln.startswith('~~~'):
                    in_code = not in_code
                    continue
                if in_code and any(ord(ch) > 127 for ch in ln):
                    return True
            return False

        needs_unicode_engine = _has_non_ascii_in_code(md_content)
        output_file = input_file.replace('.md', '.tex')
        
        import subprocess
        import shutil
        import platform
        
        # Determine LaTeX engine (prefer xelatex/lualatex when Unicode in code blocks)
        engine_name = None
        engine_path = None

        candidates = []
        if needs_unicode_engine:
            candidates = ['xelatex', 'lualatex', 'pdflatex']
        else:
            candidates = ['pdflatex', 'xelatex', 'lualatex']

        for eng in candidates:
            p = shutil.which(eng)
            if p:
                engine_name = eng
                engine_path = p
                break

        # Fallback search in common locations if not found via PATH
        if not engine_path:
            system = platform.system()
            common_paths_map = {
                'Windows': {
                    'pdflatex': [
                        rf'C:\\Users\\{os.environ.get("USERNAME", "user")}\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe',
                        r'C:\\Program Files\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe',
                        r'C:\\texlive\\2024\\bin\\win32\\pdflatex.exe',
                        r'C:\\texlive\\2024\\bin\\windows\\pdflatex.exe',
                    ],
                    'xelatex': [
                        rf'C:\\Users\\{os.environ.get("USERNAME", "user")}\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\xelatex.exe',
                        r'C:\\Program Files\\MiKTeX\\miktex\\bin\\x64\\xelatex.exe',
                        r'C:\\texlive\\2024\\bin\\win32\\xelatex.exe',
                        r'C:\\texlive\\2024\\bin\\windows\\xelatex.exe',
                    ],
                    'lualatex': [
                        rf'C:\\Users\\{os.environ.get("USERNAME", "user")}\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\lualatex.exe',
                        r'C:\\Program Files\\MiKTeX\\miktex\\bin\\x64\\lualatex.exe',
                        r'C:\\texlive\\2024\\bin\\win32\\lualatex.exe',
                        r'C:\\texlive\\2024\\bin\\windows\\lualatex.exe',
                    ],
                },
                'Linux': {
                    'pdflatex': [
                        '/usr/bin/pdflatex', '/usr/local/bin/pdflatex',
                        '/usr/local/texlive/2024/bin/x86_64-linux/pdflatex',
                        '/opt/texlive/2024/bin/x86_64-linux/pdflatex',
                    ],
                    'xelatex': [
                        '/usr/bin/xelatex', '/usr/local/bin/xelatex',
                        '/usr/local/texlive/2024/bin/x86_64-linux/xelatex',
                        '/opt/texlive/2024/bin/x86_64-linux/xelatex',
                    ],
                    'lualatex': [
                        '/usr/bin/lualatex', '/usr/local/bin/lualatex',
                        '/usr/local/texlive/2024/bin/x86_64-linux/lualatex',
                        '/opt/texlive/2024/bin/x86_64-linux/lualatex',
                    ],
                },
                'Darwin': {  # macOS
                    'pdflatex': ['/Library/TeX/texbin/pdflatex'],
                    'xelatex': ['/Library/TeX/texbin/xelatex'],
                    'lualatex': ['/Library/TeX/texbin/lualatex'],
                },
            }
            for eng in candidates:
                for path in common_paths_map.get(system, {}).get(eng, []):
                    if os.path.exists(path):
                        engine_name = eng
                        engine_path = path
                        break
                if engine_path:
                    break

        # Generate LaTeX with engine-specific preamble
        latex_output = md_to_latex(md_content, engine=engine_name or 'pdflatex', system_name=platform.system())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_output)
        
        print(f'Converted {input_file} to {output_file}')

        if engine_path:
            print(f'Compiling PDF using: {engine_path}')
            try:
                result = subprocess.run(
                    [engine_path, '-interaction=nonstopmode', output_file],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    cwd=os.path.dirname(os.path.abspath(output_file)) or '.'
                )
                
                pdf_file = output_file.replace('.tex', '.pdf')
                if os.path.exists(pdf_file):
                    print(f'✓ PDF created: {pdf_file}')
                    # Cleanup only the auxiliary files for this document
                    def _cleanup_aux_files(tex_path: str):
                        base, _ = os.path.splitext(tex_path)
                        aux_exts = [
                            '.aux', '.log', '.out', '.toc', '.synctex.gz',
                            '.fls', '.fdb_latexmk', '.nav', '.snm', '.vrb',
                            '.bbl', '.blg', '.lof', '.lot', '.lol',
                            '.idx', '.ilg', '.ind', '.glg', '.glo', '.gls',
                            '.ist', '.acn', '.acr', '.alg', '.bcf', '.run.xml',
                            '.xdy', '.thm'
                        ]
                        for ext in aux_exts:
                            candidate = base + ext
                            try:
                                if os.path.exists(candidate):
                                    os.remove(candidate)
                            except Exception:
                                # Silently ignore cleanup issues
                                pass
                    _cleanup_aux_files(output_file)
                else:
                    print('✗ PDF compilation failed')
                    if 'error' in result.stdout.lower() or 'error' in result.stderr.lower():
                        print('Errors found in compilation output')
            except Exception as e:
                print(f'✗ Error running LaTeX engine: {e}')
        else:
            print('✗ No LaTeX engine found (pdflatex/xelatex/lualatex). Please install MiKTeX or TeX Live.')
            print('  Download MiKTeX: https://miktex.org/download')
    else:
        print('Usage: python md2tex.py <markdown_file>')
