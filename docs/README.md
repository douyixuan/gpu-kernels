# GPU Kernels GitHub Pages

This directory contains the generated static HTML files for the GitHub Pages site showcasing the 100 Days GPU Kernels Learning Journey.

## Viewing the Site

Once GitHub Pages is enabled, the site will be available at:
`https://douyixuan.github.io/gpu-kernels/`

## Regenerating the Pages

If you update the README.md or add new code files to day directories, you can regenerate all pages by running:

```bash
python3 generate_pages.py
```

The script will:
1. Parse `README.md` to extract day descriptions
2. Scan all `day XX` directories for code files
3. Generate `docs/index.html` with an overview of all 100 days
4. Generate individual `docs/day-X.html` pages for each day

## Enabling GitHub Pages

To enable GitHub Pages for this repository:

1. Go to the repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Select branch: `main` (or your default branch)
5. Select folder: `/docs`
6. Click "Save"

GitHub will automatically deploy the site within a few minutes.

## Site Features

- **Responsive Design**: Mobile-friendly layout
- **Modern UI**: Clean gradient headers and card-based design
- **Syntax Highlighting**: Code files displayed with Prism.js syntax highlighting
- **Easy Navigation**: Links between days and back to the index
- **Automatic Generation**: Script handles all 100 days automatically

## Files

- `index.html` - Main landing page with all 100 days
- `day-1.html` through `day-100.html` - Individual day pages
- `_config.yml` - Jekyll configuration (minimal)
- `.nojekyll` - Tells GitHub Pages to skip Jekyll processing
