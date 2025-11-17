# Files to Push to GitHub

## ✅ PUSH THESE (Essential Files)

### Website Files:
- `index.html` - Your main website
- `styles.css` - All the styling
- `dola.jpg` - Social media preview image

### Auto-Scraping System:
- `.github/workflows/update-events.yml` - GitHub Actions workflow
- `scripts/scrape-events.py` - Event scraper
- `scripts/README.md` - Scraper documentation

### Configuration:
- `.gitignore` - Prevents bad files from being committed

### Documentation:
- `README.md` - Project overview (if you have one)
- `CLAUDE.md` - Project instructions
- `DEPLOYMENT_GUIDE.md` - How to deploy
- `FACEBOOK_INTEGRATION.md` - Facebook API setup
- `SCRAPING_GUIDE.md` - How scraping works

## ❌ DO NOT PUSH THESE

- `.DS_Store` - macOS system file (already in .gitignore)
- `.env` files - Would contain API keys (already in .gitignore)
- `__pycache__/` - Python cache (already in .gitignore)
- Any files with API keys or passwords!

---

The `.gitignore` file I created automatically prevents bad files from being pushed.
