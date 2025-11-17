# Dola - Auto-Scraping Deployment Guide

This guide will help you deploy Dola with automatic event scraping enabled.

## Quick Overview

Your Dola repository is already configured with:
- ✅ GitHub Actions workflow (`.github/workflows/update-events.yml`)
- ✅ Python event scraper (`scripts/scrape-events.py`)
- ✅ Facebook API integration in `index.html`
- ✅ Auto-refresh every 60 minutes on the website

## 🚀 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `dola` (or any name you prefer)
3. Make it **Public** (required for GitHub Pages free hosting)
4. Click **"Create repository"**

### Step 2: Push Your Code to GitHub

```bash
cd /Users/elvis/Documents/Claude\ Code/Personal/Dola

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Dola event aggregator with auto-scraping"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/dola.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select: **Deploy from a branch**
4. Branch: **main**, Folder: **/ (root)**
5. Click **Save**
6. Your site will be live at: `https://YOUR_USERNAME.github.io/dola/`

### Step 4: Configure Auto-Scraping (Optional but Recommended)

#### Option A: Use Facebook Graph API (Recommended)

1. **Create Facebook App:**
   - Go to https://developers.facebook.com/apps/
   - Click "Create App" → Choose "Business" type
   - App Name: "Dola Events Aggregator"

2. **Get Access Token:**
   - Go to Graph API Explorer: https://developers.facebook.com/tools/explorer/
   - Select your app
   - Click "Get Token" → "Get Page Access Token"
   - Select Kosovo event pages you want to scrape
   - Copy the token (long string)

3. **Add Secrets to GitHub:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add these secrets:
     - Name: `FB_APP_ID`, Value: Your Facebook App ID
     - Name: `FB_PAGE_TOKEN`, Value: Your Page Access Token

4. **Update `index.html` with your App ID:**
   - Find line 692-698 in `index.html`
   - Replace `appId: '1234567890'` with your actual App ID
   - Replace `pageAccessToken: 'YOUR_PAGE_ACCESS_TOKEN'` (this will use GitHub secrets in Actions)
   - Add Kosovo event page IDs to the `pages` array

#### Option B: Use Manual Events (Easiest)

Simply add events manually to the `MANUAL_EVENTS` array in `index.html` (lines 769-857). The scraper will preserve these and merge them with any scraped events.

### Step 5: Test Auto-Scraping

1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **"Update Events Daily"** workflow
4. Click **"Run workflow"** button (manual trigger)
5. Watch it run - it will scrape and update events automatically

### Step 6: Verify Deployment

1. Visit your GitHub Pages URL: `https://YOUR_USERNAME.github.io/dola/`
2. Check that events are displaying
3. Test language toggle (🇬🇧 EN / 🇦🇱 SQ)
4. Test category filtering
5. Test search functionality

## 📅 How Auto-Scraping Works

### Daily Updates
- GitHub Actions runs **every day at 6:00 AM UTC**
- Scraper fetches new events from configured sources
- New events are added to `MANUAL_EVENTS` in `index.html`
- Changes are committed and pushed automatically
- GitHub Pages redeploys the updated site

### Client-Side Refresh
- Website automatically reloads **every 60 minutes**
- Facebook API calls fetch fresh events from configured pages
- Events are cached in browser localStorage
- See countdown timer in bottom-right corner

## 🔧 Customization

### Change Scraping Schedule

Edit `.github/workflows/update-events.yml`:

```yaml
schedule:
  # Every 6 hours
  - cron: '0 */6 * * *'

  # Every Monday at 9 AM UTC
  - cron: '0 9 * * 1'

  # Twice daily (6 AM and 6 PM UTC)
  - cron: '0 6,18 * * *'
```

### Add More Event Sources

Edit `scripts/scrape-events.py` and add scraping logic:

```python
def scrape_events():
    events = []

    # Example: Scrape from Eventbrite
    try:
        response = requests.get('https://www.eventbrite.com/d/kosovo--pristina/events/')
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse events...
    except Exception as e:
        print(f"Error: {e}")

    return events
```

### Update Facebook Pages List

In `index.html` (line 695-698), add more Kosovo event pages:

```javascript
pages: [
    'kinoarmata',           // Kino Armata
    'zoneclubpr',           // ZONE Club
    'pristina.events',      // Pristina Events
    'visitkosovo',          // Visit Kosovo
    // Add more page IDs here
]
```

## 🔍 Finding Kosovo Event Pages

Search Facebook for:
- "Kosovo Events"
- "Prishtina Events"
- "Prizren Events"
- "ZONE Club Prishtina"
- "Kino ARMATA"
- Specific venue pages

To get Page ID from Facebook URL:
- URL: `https://www.facebook.com/kinoarmata`
- Page ID: `kinoarmata` (the part after facebook.com/)

## ⚠️ Important Notes

### Security
- **NEVER commit API keys/tokens to GitHub**
- Always use GitHub Secrets for sensitive data
- The `.gitignore` file is configured to exclude `.env` files

### Rate Limits
- Facebook Graph API has rate limits
- Don't scrape too frequently (daily is reasonable)
- Cache events to reduce API calls

### Content Accuracy
- Events are automatically scraped and may have errors
- The disclaimer notice warns users about this
- Regularly review scraped content for accuracy

## 🐛 Troubleshooting

### Facebook Error: "Feature Unavailable" or "Login Currently Unavailable"

This is a common issue with new Facebook apps. To fix:

1. **Complete App Configuration:**
   - Go to App Dashboard → Settings → Basic
   - Fill in all required fields:
     - Privacy Policy URL (use https://www.termsfeed.com/privacy-policy-generator/)
     - Category: Choose "Events" or "Entertainment"
     - App Icon: Upload any image
   - Add Platform → Website → Enter your GitHub Pages URL
   - Save changes

2. **Switch to Live Mode:**
   - Toggle "In Development" → "Live Mode" at top of dashboard
   - This may require identity verification for first app

3. **Alternative: Deploy Without Facebook API First**
   - Your site works perfectly without Facebook API
   - Just deploy to GitHub Pages and use manual events
   - Add Facebook API later when ready
   - All features still work (search, filters, language toggle)

### GitHub Actions Not Running
- Check the Actions tab for error logs
- Verify secrets are configured correctly
- Make sure workflow file is in `.github/workflows/`

### No Events Showing
- Check if scraper is returning events (see Actions logs)
- Your site has many hardcoded events in index.html - these should always show
- Check browser console for JavaScript errors

### Changes Not Appearing on Site
- GitHub Pages can take 1-2 minutes to deploy
- Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check that workflow successfully committed changes

### Scraper Failing
- Check Actions logs for specific errors
- Verify dependencies are installed (beautifulsoup4, requests)
- Test scraper locally: `python scripts/scrape-events.py`
- The scraper is optional - site works without it

## 📱 Sharing on Social Media

Update meta tags in `index.html` (lines 9-24) with your GitHub Pages URL:

```html
<meta property="og:url" content="https://YOUR_USERNAME.github.io/dola/">
<meta property="og:image" content="https://YOUR_USERNAME.github.io/dola/dola.jpg">
```

## 🎉 Next Steps

1. ✅ Deploy to GitHub Pages
2. ✅ Test auto-scraping workflow
3. ✅ Share your site on social media
4. 📊 Monitor GitHub Actions for daily updates
5. 🔄 Add more event sources over time
6. 🌟 Customize the design and content

## Need Help?

- Check `FACEBOOK_INTEGRATION.md` for Facebook API setup
- Review `scripts/README.md` for scraper customization
- See `CLAUDE.md` for project architecture details

---

**Your Dola site is now ready for deployment with automatic event updates! 🚀**
