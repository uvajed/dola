# Automatic Facebook Event Scraping Guide

## Overview

This guide shows you how to automatically scrape Facebook events daily using GitHub Actions.

## Prerequisites

- GitHub account (you have this ✅)
- Facebook Developer account (free)
- 15 minutes of setup time

---

## PART 1: Facebook App Setup (10 minutes)

### Step 1: Create Facebook Developer Account

1. Go to https://developers.facebook.com/
2. Click **"Get Started"**
3. Log in with your Facebook account
4. Complete the registration (verify email if needed)

### Step 2: Create Facebook App

1. Go to https://developers.facebook.com/apps/
2. Click **"Create App"**
3. Choose app type: **"Business"**
4. Fill in details:
   - **App Name**: "Dola Events"
   - **Contact Email**: Your email
   - Click **"Create App"**

### Step 3: Complete App Configuration

1. In your app dashboard, go to **Settings** → **Basic**

2. Fill in **required fields**:
   ```
   Privacy Policy URL: https://www.termsfeed.com/live/your-privacy-policy-url
   (You can generate one free at: https://www.termsfeed.com/privacy-policy-generator/)
   
   Category: Events
   
   App Icon: Upload any icon (can use your dola.jpg)
   ```

3. **Add Platform**:
   - Scroll down to "Add Platform"
   - Click **"Website"**
   - Site URL: `https://uvajed.github.io/dola/`
   - Save Changes

4. **Copy your App ID** (you'll need this later)
   - It's shown at the top of the Settings page
   - Example: `532619825283746`

### Step 4: Switch App to Live Mode

1. At the top of your app dashboard, you'll see **"App Mode: Development"**
2. Click the toggle to switch to **"Live"**
3. May require identity verification (follow prompts)
4. Once approved, app is live!

---

## PART 2: Get Access Tokens (5 minutes)

### Option A: User Access Token (Easiest, expires in 60 days)

1. Go to https://developers.facebook.com/tools/explorer/

2. Select your app from the dropdown

3. Click **"Get Token"** → **"Get User Access Token"**

4. Select permissions:
   - `pages_read_engagement`
   - `pages_show_list`
   - Click **"Generate Access Token"**

5. **Copy the token** (long string starting with `EAAA...`)

6. **Extend the token** (make it last 60 days):
   - Go to https://developers.facebook.com/tools/accesstoken/
   - Find your token
   - Click **"Debug"**
   - Click **"Extend Access Token"**
   - Copy the new extended token

### Option B: Page Access Token (Advanced, better for production)

1. Go to https://developers.facebook.com/tools/explorer/

2. Select your app

3. Click **"Get Token"** → **"Get Page Access Token"**

4. Select the Facebook Pages you want to scrape events from

5. Copy the page token

---

## PART 3: Add Tokens to GitHub Secrets

### Add Secrets (CRITICAL - Never commit these!)

1. Go to your repository: https://github.com/uvajed/dola

2. Click **Settings** → **Secrets and variables** → **Actions**

3. Click **"New repository secret"**

4. Add **First Secret**:
   ```
   Name: FB_APP_ID
   Value: [Your App ID from Step 3.4]
   ```
   Click **"Add secret"**

5. Add **Second Secret**:
   ```
   Name: FB_PAGE_TOKEN
   Value: [Your Access Token from Part 2]
   ```
   Click **"Add secret"**

---

## PART 4: Configure Your Scraper

### Update the Scraper Code

I'll update your `scripts/scrape-events.py` to use Facebook Graph API with the tokens from GitHub Secrets.

The scraper will:
- Use tokens from environment variables (GitHub Secrets)
- Fetch events from Facebook pages you specify
- Parse event details (name, date, location, description)
- Add them to your website automatically
- Run daily at 6 AM UTC

### Find Facebook Page IDs

To scrape events from Kosovo venues:

1. **Find the Facebook page** (e.g., "ZONE Club Prishtina")
2. **Get the Page ID**:
   - Method 1: Look at the URL
     - `https://www.facebook.com/zoneclubpr` → Page ID is `zoneclubpr`
   
   - Method 2: Use Graph API Explorer
     - Go to https://developers.facebook.com/tools/explorer/
     - Enter: `https://www.facebook.com/zoneclubpr`
     - Click Submit → You'll see the page ID

3. **Add to your list** (I'll show you where)

---

## PART 5: How It Works

### Daily Automatic Updates:

```
Every day at 6:00 AM UTC:
  ↓
GitHub Actions starts
  ↓
Loads FB_APP_ID and FB_PAGE_TOKEN from secrets
  ↓
Runs scrape-events.py
  ↓
Scraper calls Facebook Graph API
  ↓
Gets latest events from your specified pages
  ↓
Adds events to MANUAL_EVENTS in index.html
  ↓
Commits changes to GitHub
  ↓
GitHub Pages auto-deploys
  ↓
Your site shows fresh events! ✅
```

### What Gets Scraped:

- Event name/title
- Start date and time
- Event description
- Location/venue
- Cover photo
- Facebook event link

---

## PART 6: Testing

### Manual Test (GitHub Actions)

1. Go to https://github.com/uvajed/dola/actions

2. Click **"Update Events Daily"**

3. Click **"Run workflow"** dropdown

4. Click green **"Run workflow"** button

5. Watch it run (takes ~30 seconds)

6. Check the logs for:
   - "🔍 Scraping Facebook events..."
   - "✅ Found X events"
   - "✅ Added X new events to index.html"

### Local Test (Optional)

```bash
# Set environment variables
export FB_APP_ID="your_app_id"
export FB_PAGE_TOKEN="your_token"

# Run scraper
python3 scripts/scrape-events.py
```

---

## Token Renewal

### Access Token Expiration:

- **User tokens**: Expire after 60 days
- **Page tokens**: Can be long-lived (doesn't expire)

### When token expires:

1. Go to https://developers.facebook.com/tools/explorer/
2. Get new token (same process as Part 2)
3. Update GitHub Secret `FB_PAGE_TOKEN`
4. Done!

### Set Calendar Reminder:

- Set reminder for 55 days from now
- Renew token before it expires
- Takes 2 minutes

---

## Troubleshooting

### "Invalid OAuth access token"
- Token expired → Get new one
- Wrong token in secrets → Check and update

### "No events found"
- Page has no upcoming events
- Wrong page ID → Verify in Graph API Explorer
- Permissions issue → Ensure `pages_read_engagement` is granted

### "Rate limit exceeded"
- Too many requests → Scraper already has delays built in
- Try again in 1 hour

### Events not appearing on site
- Check GitHub Actions logs
- Verify commit was successful
- GitHub Pages takes 1-2 min to deploy

---

## Best Practices

### ✅ Do:
- Renew tokens before expiration
- Add 3-5 popular Kosovo event pages
- Monitor GitHub Actions for errors
- Respect Facebook's rate limits

### ❌ Don't:
- Never commit tokens to code
- Don't scrape too frequently (daily is good)
- Don't share your access tokens
- Don't scrape private events

---

## Kosovo Event Pages to Scrape

Add these page IDs to your scraper:

```python
FACEBOOK_PAGES = [
    'kinoarmata',        # Kino ARMATA
    'zoneclubpr',        # ZONE Club
    'vendum.ks',         # Vendum
    'pristina.events',   # Prishtina Events (if exists)
    'visitkosovo',       # Visit Kosovo
    # Add more as you find them
]
```

---

## Summary

1. ✅ Create Facebook App
2. ✅ Get Access Token
3. ✅ Add to GitHub Secrets
4. ✅ Configure page IDs
5. ✅ Test manually
6. ✅ Runs automatically daily at 6 AM UTC

**Setup time**: 15 minutes  
**Maintenance**: Renew token every 60 days (2 min)  
**Result**: Fresh Facebook events on your site daily! 🎉

---

Need help with any step? Let me know!
