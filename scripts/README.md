# Event Scraper for Dola

This folder contains the automated event scraping system that runs daily via GitHub Actions.

## How It Works

1. **GitHub Actions** runs every day at 6:00 AM UTC
2. **scrape-events.py** fetches new events from configured sources
3. New events are added to the `MANUAL_EVENTS` array in `index.html`
4. Changes are automatically committed and pushed to GitHub
5. GitHub Pages deploys the updated site

## Customizing the Scraper

### Adding Event Sources

Edit `scrape-events.py` and add your scraping logic in the `scrape_events()` function:

```python
def scrape_events():
    events = []

    # Example: Scrape from a website
    try:
        response = requests.get('https://example.com/events')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse events from the page
        for event_element in soup.find_all('div', class_='event'):
            event = {
                'title': event_element.find('h2').text,
                'titleEn': event_element.find('h2').text,
                'description': event_element.find('p').text,
                'descriptionEn': event_element.find('p').text,
                'date': 'Nov 20',
                'time': '7:00 PM',
                'location': 'Prishtina',
                'image': 'https://images.unsplash.com/...',
                'category': 'concert',
                'url': 'https://example.com/event/1',
                'source': 'Example Source',
                'isLive': True
            }
            events.append(event)
    except Exception as e:
        print(f"Error scraping: {e}")

    return events
```

### Using Facebook Graph API

To scrape Facebook events properly, you need API credentials:

1. Create a Facebook App at https://developers.facebook.com
2. Get your App ID and Page Access Token
3. Add them as GitHub Secrets:
   - Go to your repo Settings → Secrets → Actions
   - Add `FB_APP_ID` and `FB_PAGE_TOKEN`
4. Update the scraper to use these credentials

### Manual Testing

Run the scraper locally:

```bash
cd /path/to/Dola
python3 scripts/scrape-events.py
```

### Adjusting Schedule

Edit `.github/workflows/update-events.yml`:

```yaml
schedule:
  # Run every 12 hours
  - cron: '0 */12 * * *'

  # Run every Monday at 9 AM
  - cron: '0 9 * * 1'
```

## Event Structure

Each event must have these fields:

- `title` (Albanian)
- `titleEn` (English)
- `description` (Albanian)
- `descriptionEn` (English)
- `date` (e.g., "Nov 20")
- `time` (e.g., "7:00 PM")
- `location` (e.g., "Prishtina")
- `image` (URL)
- `category` (`bars`, `museum`, `outdoor`, `restaurant`, `concert`)
- `url` (link to event)
- `source` (source name)
- `isLive` (true for time-specific events, false for venues)

## Troubleshooting

- **Actions not running?** Check the Actions tab in your GitHub repo
- **Scraper failing?** Check the workflow logs for errors
- **Events not updating?** Make sure the scraper found new events
