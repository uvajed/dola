# Event Scraping Guide

## Current Sources

Your scraper (`scripts/scrape-events.py`) currently scrapes from:

1. **Eventbrite Kosovo** - Public event listings from Prishtina

## Adding More Kosovo Event Sources

### Easy Sources to Add:

1. **Visit Kosovo Official**
   - URL: https://www.visitkosova.org/en/events/
   - Public events calendar
   - No API needed

2. **Kosovo Events Pages**
   - https://www.facebook.com/pg/kinoarmata/events (requires Facebook API)
   - https://www.bandsintown.com/c/pristina-kosovo
   - Local venue websites

3. **RSS Feeds** (Best Option!)
   - Many venues publish RSS feeds
   - Look for `/feed`, `/rss`, or `/.rss` at end of URLs
   - Example: `https://venue-website.com/events/feed`

### How to Add a New Source

Edit `scripts/scrape-events.py` and add a function:

```python
def scrape_new_source():
    """
    Scrape from your new source
    """
    events = []
    
    try:
        print("🔍 Scraping New Source...")
        url = "https://example-kosovo-events.com/events"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find event elements (inspect website to find correct selectors)
            event_elements = soup.find_all('div', class_='event-item')
            
            for elem in event_elements:
                title = elem.find('h2').get_text(strip=True)
                date = elem.find('span', class_='date').get_text(strip=True)
                location = elem.find('span', class_='location').get_text(strip=True)
                
                event = {
                    'title': title,
                    'titleEn': title,
                    'description': 'Event in Kosovo',
                    'descriptionEn': 'Event in Kosovo',
                    'date': date,
                    'time': 'TBA',
                    'location': location,
                    'image': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400',
                    'category': 'concert',
                    'url': url,
                    'source': 'New Source Name',
                    'isLive': True
                }
                events.append(event)
                print(f"  ✅ Found: {title}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return events
```

Then add it to the main `scrape_events()` function:

```python
def scrape_events():
    all_events = []
    
    # Existing sources
    eventbrite_events = scrape_eventbrite()
    all_events.extend(eventbrite_events)
    
    # Your new source
    new_events = scrape_new_source()
    all_events.extend(new_events)
    
    return all_events
```

## Finding Good Sources

### Look For:

1. **Public event calendars** (no login required)
2. **RSS/Atom feeds** (easiest to parse)
3. **Structured HTML** (consistent formatting)
4. **Kosovo-specific** event sites

### Avoid:

1. **Sites requiring login** (complicated, unreliable)
2. **Sites with CAPTCHAs** (will block scraper)
3. **Google** (actively blocks scrapers, ToS violation)
4. **JavaScript-heavy sites** (need browser automation)

## Kosovo Event Sources to Consider

### Websites:
- Visit Kosovo: https://www.visitkosova.org/
- Pristina Insight: Events section
- Local venue websites (ZONE Club, Kino ARMATA, etc.)
- University event boards

### Social Media (with API):
- Facebook Events (requires Graph API - see FACEBOOK_INTEGRATION.md)
- Instagram event posts (requires API)

### Event Platforms:
- Eventbrite Kosovo (✅ already implemented)
- Meetup.com Kosovo groups
- AllEvents Kosovo

## Testing Your Scraper Locally

```bash
# Install dependencies
pip3 install beautifulsoup4 requests lxml

# Run scraper
python3 scripts/scrape-events.py

# Check if events were found
# Look for "✅ Found X total new events"
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'bs4'"
- Install: `pip3 install beautifulsoup4`

### "No events found"
- Check if website structure changed
- Verify CSS selectors are correct
- Test URL in browser first

### "Timeout errors"
- Website might be blocking requests
- Add delays between requests
- Check your internet connection

### "403 Forbidden"
- Website is blocking your User-Agent
- Try different User-Agent string
- Some sites require cookies/sessions

## Legal & Ethical Scraping

### ✅ Good Practices:
- Scrape only public data
- Respect robots.txt
- Add delays between requests (be polite)
- Cache results to reduce requests
- Provide proper attribution

### ❌ Don't:
- Scrape private/login-only data
- Overwhelm servers with requests
- Scrape sites that explicitly forbid it
- Violate Terms of Service

## Why Not Use Google?

**People often ask: "Can I just scrape Google search results?"**

**Answer: NO - here's why:**

1. **Actively Blocked**: Google uses CAPTCHAs, rate limits, IP bans
2. **ToS Violation**: Against Google's Terms of Service
3. **Unreliable**: Frequently breaks due to anti-scraping measures
4. **Low Quality**: Search results != structured event data
5. **Legal Risk**: Could get legal threats from Google

**Better approach:** Scrape the same sources Google indexes (event websites directly)

## GitHub Actions Deployment

When you push to GitHub, the scraper runs automatically:

1. **No local installation needed** - GitHub provides fresh Python environment
2. **Dependencies auto-installed** - See `.github/workflows/update-events.yml`
3. **Runs daily at 6 AM UTC** - Fully automated
4. **Commits results** - Updates your site automatically

## Need Help?

- Check existing scraper: `scripts/scrape-events.py`
- Read deployment guide: `DEPLOYMENT_GUIDE.md`
- Test locally before deploying
- Check GitHub Actions logs if scraper fails

---

**Remember: Your site works great even without scraping!** The scraper is just a bonus to auto-update events. You already have 20+ hardcoded events that will always display.
