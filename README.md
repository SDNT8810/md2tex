# md2tex

A small, no-frills Markdown → LaTeX/PDF converter written in Python. One command takes a `.md` file and produces `.tex` and `.pdf` with sensible defaults.

## Highlights

- One-step pipeline: `.md → .tex → .pdf` (runs a LaTeX engine for you)
- Cross‑platform engine detection: `pdflatex`, `xelatex`, or `lualatex` (Windows/Linux/macOS)
- Engine‑flexible LaTeX preamble (via `iftex`) so the same `.tex` compiles on Overleaf and locally with pdfLaTeX/LaTeX or XeLaTeX/LuaLaTeX
- Unicode‑safe behavior:
  - Preserves raw Unicode exactly inside fenced code blocks (```/~~~)
  - Uses a Unicode‑capable engine automatically when needed
- Emoji/sticker removal by Unicode ranges (no per‑emoji lists)
- Inline formatting: `**bold**`, `[links](url)`, and `` `inline code` ``
- Math: inline `$...$`, display `$$...$$`, and bracketed display blocks using lines with `[` and `]`
- Auto‑wraps common math used in text (e.g., `\alpha`, `\int`, `\vec{x}`, `x_1`, `x^2`) into `$...$`
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

The script auto‑detects engines via PATH and known install locations and prefers `xelatex`/`lualatex` when it detects non‑ASCII inside fenced code blocks; otherwise it uses `pdflatex`.
The generated `.tex` includes an engine‑aware preamble: pdfTeX uses `inputenc` + `T1` + `lmodern`, while Xe/LuaLaTeX use `fontspec`.

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
  - Auto‑math wrapping: if you accidentally use math commands in text (e.g., `\alpha`, `\int`, `x_1`, `x^2`, `\vec{x}`), they are wrapped into `$...$` automatically
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
- “fontspec only works with Xe/LuaLaTeX”
  - The output `.tex` avoids loading `fontspec` on pdfLaTeX/LaTeX via `iftex`. If you manually edit the preamble, keep `fontspec` under the Xe/Lua branch only.
- “Unicode in code block breaks with pdflatex”
  - The script prefers `xelatex`/`lualatex` when it detects non‑ASCII in code fences; install one of them if missing
- Overleaf notes
  - You can compile the same `.tex` with pdfLaTeX, XeLaTeX, or LuaLaTeX. If you hit Unicode issues, switch the Overleaf compiler to XeLaTeX or LuaLaTeX.

## Known limitations (by design)

- Images, blockquotes, and task lists are not implemented (kept intentionally simple)
- This is not a full Markdown parser; it covers the most common patterns used in notes/technical docs

## Credits

- Author: SDNT8810

## License

MIT License — see `LICENSE` file.
