# md2tex

A small, no-frills Markdown → LaTeX/PDF converter written in Python. One command takes a `.md` file and produces `.tex` and `.pdf` with sensible defaults.

## Highlights

- One-step pipeline: `.md → .tex → .pdf` (runs a LaTeX engine for you)
- Cross‑platform engine detection: `pdflatex`, `xelatex`, or `lualatex`
- Unicode‑safe behavior:
  - Preserves raw Unicode exactly inside fenced code blocks (```/~~~)
  - Uses a Unicode‑capable engine automatically when needed
- Emoji/sticker removal by Unicode ranges (no per‑emoji lists)
- Inline formatting: `**bold**`, `[links](url)`, and `` `inline code` ``
- Math: inline `$...$`, display `$$...$$`, and bracketed display blocks using lines with `[` and `]`
- Tables: GitHub‑style pipe tables scaled to page width
- Lists: ordered/unordered, nested by indentation (2 spaces per level)
- Headings: `#` → `\section`, `##` → `\subsection`, `###` → `\subsubsection`, `####` → `\paragraph`
  - Leading numeric prefixes like `1. Title` are stripped from heading text
  - Subsubsections numbered as `1, 2, 3` (no `0.0.1`)
- Horizontal rules: `---`, `***`, or `___`
- Newlines: a single newline in Markdown becomes a visible line break in LaTeX (`\newline`)
- Cleanup: removes LaTeX aux files after a successful build (keeps only `.md`, `.tex`, `.pdf`, `.py`)

## Requirements

- Python 3.8+
- A LaTeX distribution:
  - Windows: MiKTeX or TeX Live
  - Linux/macOS: TeX Live

The script auto‑detects engines via PATH and known install locations and prefers `xelatex`/`lualatex` when it detects non‑ASCII inside fenced code blocks, otherwise `pdflatex`.

## Usage

- Windows (PowerShell):

```powershell
python md2tex.py your_file.md
```

- Linux/macOS:

```bash
python3 md2tex.py your_file.md
```

Outputs:
- `your_file.tex` — generated LaTeX
- `your_file.pdf` — compiled PDF (if a LaTeX engine is installed)

## Markdown support details

- Paragraphs/newlines
  - Single newline → `\\newline` (forced line break)
  - Blank line → paragraph break
- Code
  - Fenced code blocks (```/~~~) are emitted as `verbatim` with Unicode preserved
  - Inline code uses `\texttt{...}` with safe escaping
- Math
  - Inline: `$...$`
  - Display: `$$...$$` or bracketed block between lines `[` and `]`
  - Literal `$$...$$` text is preserved (escaped) in regular paragraphs
- Tables
  - Pipe tables with a header and a separator line are supported and auto‑scaled to `\textwidth`
- Lists
  - `-`, `*` unordered; `1.` ordered
  - Nesting by 2‑space indentation per level
- Headings
  - `#`, `##`, `###`, `####` → LaTeX sectioning commands
  - Leading numbering like `1. Title` in source is removed from the title text
- Emojis/stickers
  - Removed globally by Unicode ranges (flags, pictographs, emoticons, dingbats, skin tones, VS‑16/ZWJ)

## Troubleshooting

- “No LaTeX engine found”
  - Install MiKTeX (Windows) or TeX Live (Linux/macOS) and ensure binaries are on PATH
- “PDF compilation failed”
  - Check the generated `.tex` next to your `.md`
  - Make sure packages like `amsmath`, `hyperref`, `adjustbox` are available in your LaTeX install
- “Unicode in code block breaks with pdflatex”
  - The script prefers `xelatex`/`lualatex` when it detects non‑ASCII in code fences; install one of them if missing

## Known limitations (by design)

- Images, blockquotes, and task lists are not implemented (kept intentionally simple)
- This is not a full Markdown parser; it covers the most common patterns used in notes/technical docs

## Credits

- Author: SDNT8810

## License

MIT License — see `LICENSE` file.
