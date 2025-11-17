# Auto-Scraper Setup Guide

This guide explains how to configure automatic event scraping from multiple sources.

## 🎯 What Gets Scraped

The daily auto-scraper fetches events from:
- ✅ **Eventbrite** (disabled - was inaccurate)
- ⚠️ **Facebook** (requires API setup)
- ⚠️ **Google Search** (requires API setup)
- ❌ **Instagram** (not supported - against ToS)

## 📅 When It Runs

- **Automatically**: Every day at 6:00 AM UTC
- **Manually**: Go to GitHub → Actions → "Update Events Daily" → Run workflow

## 🔧 Configuration

### Option 1: Facebook Events (Recommended)

**What you need:**
1. Facebook App ID
2. Page Access Token (hardest part!)

**Setup:**
1. Go to: https://developers.facebook.com/apps
2. Create a new app (choose "Business" type)
3. Get your App ID from the dashboard
4. **To get Page Access Token:**
   - You must be an admin of the Facebook page (Kino ARMATA, etc.)
   - Go to Graph API Explorer: https://developers.facebook.com/tools/explorer
   - Generate a Page Access Token
   - OR: Ask the page owner to authorize your app

**Add to GitHub:**
1. Go to: Your repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add:
   - Name: `FB_APP_ID` → Value: Your App ID
   - Name: `FB_PAGE_TOKEN` → Value: Your Page Access Token

**Scraped pages:**
- kinoarmata (Kino ARMATA)
- zoneclubpr (ZONE Club)
- vendum.ks (Vendum)

---

### Option 2: Google Custom Search (Easier)

**What you need:**
1. Google API Key (FREE - 100 searches/day)
2. Custom Search Engine ID

**Setup:**

**Step 1: Get API Key**
1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable "Custom Search API"
4. Go to: Credentials → Create Credentials → API Key
5. Copy your API key

**Step 2: Create Search Engine**
1. Go to: https://programmablesearchengine.google.com/
2. Click "Add" to create new search engine
3. **Sites to search:** Leave blank or add `*.com/*` (searches entire web)
4. **Search settings:**
   - Enable "Search the entire web"
   - Name it "Kosovo Events Search"
5. Click "Create"
6. Copy your **Search Engine ID** (starts with a long string of letters)

**Add to GitHub:**
1. Go to: Your repo → Settings → Secrets and variables → Actions
2. Add:
   - Name: `GOOGLE_API_KEY` → Value: Your Google API Key
   - Name: `GOOGLE_SEARCH_ENGINE_ID` → Value: Your Search Engine ID

**Search queries used:**
- "events in Prishtina Kosovo this week"
- "concerts Kosovo November 2025"
- "Prizren events"
- "Kosovo nightlife events"

**Limitations:**
- FREE tier: 100 searches/day
- May find event listings, news articles, not always direct event pages
- Results quality varies

---

### Option 3: Instagram (NOT SUPPORTED)

**Why it doesn't work:**
- Instagram has NO public events API
- Web scraping Instagram is:
  - Against their Terms of Service
  - Actively blocked by their bot detection
  - Unreliable and breaks frequently

**Alternative:**
- Manually check Instagram for events
- Add them to `MANUAL_EVENTS` in index.html
- Much more reliable than trying to scrape

---

## 🧪 Testing the Scraper

**Test locally:**
```bash
cd scripts
python3 scrape-events.py
```

**Test on GitHub:**
1. Go to: Actions tab in your repo
2. Click "Update Events Daily"
3. Click "Run workflow"
4. Wait 1-2 minutes
5. Check the logs to see what was found

---

## 📊 What Happens

When the scraper runs:

1. ✅ Fetches events from configured sources
2. 🔄 Updates `MANUAL_EVENTS` array in `index.html`
3. 💾 Auto-commits with message: "🤖 Auto-update events - [timestamp]"
4. 🚀 GitHub Pages deploys updated site (1-2 min)

---

## ⚠️ Important Notes

**Event Quality:**
- Facebook: ⭐⭐⭐⭐⭐ Best quality (real event data)
- Google Search: ⭐⭐⭐ Medium (may include news articles)
- Instagram: ⭐ Not supported

**API Limits:**
- Google: 100 searches/day (FREE tier)
- Facebook: No hard limit, but rate limited

**Privacy:**
- All API keys stored in GitHub Secrets (encrypted)
- Never commit API keys to code!

---

## 🎯 Recommended Setup

**For best results:**

1. ✅ **Set up Facebook API** (if you can get Page Access Token)
2. ✅ **Set up Google Search** (easy, free, backup source)
3. ❌ **Skip Instagram** (manually add events instead)
4. ✅ **Keep manual curation** (still add important events to MANUAL_EVENTS)

The auto-scraper is a **supplement**, not a replacement for manual curation!

---

## 🆘 Troubleshooting

**No events found:**
- Check GitHub Actions logs for errors
- Verify API keys are correct in Secrets
- Try running script locally to debug

**Facebook fails:**
- Page Access Token expired? (they expire!)
- App not approved by Facebook?
- Page privacy settings blocking API?

**Google returns junk:**
- Refine search queries in `scrape-events.py`
- Add better filtering logic
- Reduce search result limit

---

Need help? Check the GitHub Actions logs for detailed error messages.
