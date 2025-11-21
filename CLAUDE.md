# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dola is a static HTML/CSS event aggregator application for Prishtina, Kosovo. It displays local events, venues, and activities in a hybrid model showing both time-specific events (with dates) and permanent venues (always available).

## Running the Application

Simply open `index.html` in any web browser. No build process, dependencies, or server required.

## ⚠️ CRITICAL RULES

### Event Title Preservation

**NEVER change event titles from their original name. EVER.**

- ✅ **Titles**: Always keep in original language (Albanian, English, or whatever language the event organizer used)
- ✅ **Descriptions**: CAN be translated between Albanian and English
- ❌ **DO NOT** translate event titles
- ❌ **DO NOT** modify event titles in any way
- ❌ **DO NOT** add language switching attributes (`data-lang-sq`, `data-lang-en`) to title elements

**Examples:**
- Event title: "Sunny Hill Festival 2025" → Keep as "Sunny Hill Festival 2025" (never translate to "Festivali Sunny Hill 2025")
- Event title: "Koncert i Dafina Zeqiri" → Keep as "Koncert i Dafina Zeqiri" (never translate to "Dafina Zeqiri Concert")
- Description: "Koncert në Prishtinë" → CAN be translated to "Concert in Prishtina"

This rule applies to:
- Manual events in `MANUAL_EVENTS` array
- Scraped events from `scripts/scrape-events.py`
- User-submitted events
- All event rendering functions in JavaScript

## Architecture

### Two-Type Content Model

The application uses a **hybrid content system**:

1. **TIME-SPECIFIC EVENTS** (🎉 LIVE EVENT badge)
   - Events with specific dates and times
   - Displayed first in the feed
   - Have pink/red gradient badge with pulsing animation
   - Pink border around card (`.event-card-live`)
   - Examples: NYE parties, football matches, Christmas market

2. **PERMANENT VENUES** (📍 VENUE badge)
   - Restaurants, museums, bars always open
   - Displayed after live events
   - Have green/blue gradient badge (`.venue-badge`)
   - Standard card styling

### Event Card Structure

Each event card (`.event-card`) must include:
- `data-category` attribute: `bars`, `museum`, `outdoor`, `restaurant`, or `concert`
- `.event-badge` with either default (live event) or `.venue-badge` class
- `.event-image` with background-image style
- `.event-content` containing:
  - `.event-header` with category tag and time
  - `.event-title`
  - `.event-description`
  - `.event-footer` with location and source
  - `.maps-btn` button

### Click Behavior

- **Card click**: Opens Google search for the event/venue (for reviews/info)
- **Maps button click**: Opens Google Maps with location
- Maps button uses `event.stopPropagation()` to prevent card click

### Category Filtering

JavaScript in `index.html` filters cards by `data-category` attribute when category buttons are clicked. The mapping:
- "Bars & Nightlife" → `bars`
- "Museums & Culture" → `museum`
- "Outdoor Activities" → `outdoor`
- "Restaurants" → `restaurant`
- "Concerts & Shows" → `concert`

### Auto-Refresh System

Page automatically reloads every 60 minutes (`REFRESH_INTERVAL = 60 * 60 * 1000`). A countdown timer displays in the bottom-right corner showing:
- Last update time
- Minutes until next refresh

For production, replace `location.reload()` with API calls to event sources (Facebook Graph API, Eventbrite API, etc.).

## Automatic Event Ordering System

Events are automatically sorted without manual order numbers:

- **Live events**: Automatically sorted by date (soonest first)
  - Events with specific dates like "Nov 19" or "Dec 31" appear first
  - Events with vague dates like "Coming Soon" or "This Weekend" appear last
  - Sorting happens automatically based on the `date` field

- **Permanent venues**: Displayed in the order they appear in the array
  - First venue in the array = first venue displayed
  - To move a venue to the top, move it to the top of the PERMANENT VENUES section in the code

The `renderDynamicEvents()` function automatically:
1. Filters to only show events with actual dates
2. **Removes past events** - Events with dates that have already passed are automatically hidden
   - For date ranges (e.g., "Nov 22-27"), uses the END date
   - For single dates (e.g., "Nov 19"), checks that specific date
   - Permanent venues (e.g., "Open Daily", "Check Schedule") are never filtered out
3. Sorts remaining events by date (soonest first)
4. Displays events in chronological order

**Note**: Past events are only hidden from display, not deleted from the code. This prevents the list from showing outdated events while preserving the event data.

### To Reorder Venues:

Simply cut and paste the venue object to a new position in the `MANUAL_EVENTS` array. For example, to make Rugova Canyon appear first:

1. Cut the Rugova Canyon event object
2. Paste it right after the `// PERMANENT VENUES` comment
3. It will now appear first among venues!

## Adding New Events

**IMPORTANT**: Events must be added to the `MANUAL_EVENTS` JavaScript array, **NOT** as static HTML in the feed. Static HTML events will not be properly sorted or displayed.

### How to Add Events:

1. **Locate the `MANUAL_EVENTS` array** in `index.html` (search for `const MANUAL_EVENTS`)

2. **Add new event object** with all required properties:
   ```javascript
   {
       title: "Event Name in Albanian",
       titleEn: "Event Name in English",
       description: "Albanian description",
       descriptionEn: "English description",
       date: "Nov 25",  // or "Nov 25-30" for multi-day
       time: "7:00 PM",  // Optional, can be empty string ""
       location: "Venue Name, City",
       image: "https://images.unsplash.com/...",
       category: "concert",  // bars, museum, outdoor, restaurant, or concert
       url: "https://event-website.com",
       source: "Event Organizer Name",
       isLive: true  // true for time-specific events, false for permanent venues
   }
   ```

3. **Placement**:
   - For live events: Add anywhere in UPCOMING EVENTS section (auto-sorted by date)
   - For new venues: Add in PERMANENT VENUES section (order matters!)

### Examples:

**Live Event (Concert):**
```javascript
{
    title: "Festivali i Xhazit të Prishtinës 2025",
    titleEn: "Prishtina Jazz Festival 2025",
    description: "Festivali ndërkombëtar vjetor i xhazit...",
    descriptionEn: "Annual international jazz festival...",
    date: "Nov 14-19",
    time: "",
    location: "ODA Theatre, Prishtinë",
    image: "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=400",
    category: "concert",
    url: "https://www.instagram.com/prishtinajazzfest/",
    source: "prishtinajazzfest",
    isLive: true
}
```

**Permanent Venue (Restaurant):**
```javascript
{
    title: "Pishat Restaurant",
    titleEn: "Pishat Restaurant",
    description: "Një nga restoratet më të njohura në Prishtinë...",
    descriptionEn: "One of the most popular restaurants in Pristina...",
    date: "Check Schedule",
    time: "Open Daily",
    location: "Prishtina",
    image: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400",
    category: "restaurant",
    url: "https://www.google.com/search?q=Pishat+Restaurant+Prishtina",
    source: "Local Reviews",
    isLive: false
}
```

## User Features

### Favorites System

Users can save events they're interested in:
- Click the heart icon on any event card to save/unsave
- Saved events are stored in `localStorage` (client-side only)
- Click "Saved Events" button to filter and view only saved events
- Heart icon changes color when event is saved (red vs. outline)
- Saved count shown in "Saved Events" button

**Technical Details:**
- `localStorage.getItem('dolaFavorites')` - Array of saved event IDs
- Each event card has a unique ID generated from title + location
- Heart icons update dynamically when toggled

### User-Submitted Events

Users can add their own events via the "Add Event" button:
- Green floating button in bottom-left corner
- Opens modal form with bilingual fields (Albanian/English)
- Image suggestions based on selected category
- Events stored in `localStorage` (client-side only)
- User events display with orange "USER EVENT" badge
- Can be deleted by clicking X button on the card

**Technical Details:**
- `localStorage.getItem('userSubmittedEvents')` - Array of user events
- User events loaded before other events on page load
- Same structure as MANUAL_EVENTS but stored in localStorage

### Bilingual Support

All UI elements support Albanian (Shqip) and English:
- Language toggle button in header (🇦🇱 SQ / 🇬🇧 EN)
- Uses `data-lang-sq` and `data-lang-en` attributes
- Event titles and descriptions switch dynamically
- Current language stored in `localStorage`

### Page View Counter

Displays page view count in the footer:
- Stored in `localStorage.getItem('dolaPageViews')` (per-browser tracking)
- Increments on each page load
- Starts at 0 for new visitors
- Uses version system (`dolaCounterVersion`) to force resets
- Change `COUNTER_VERSION` constant in `updatePageViewCounter()` to reset all counters globally
- Displays with animated purple highlight on update

**Technical Details:**
- Located in footer: `<span id="page-view-counter">`
- Version check prevents old high counts from persisting after resets
- Format: `👁️ Page Views: 123`

## CSS Architecture

- Gradient theme: Purple (`#667eea` to `#764ba2`)
- Live event badge: Soft pink gradient with gentle pulse animation
- Venue badge: Soft green gradient, no animation
- User event badge: Orange gradient
- Responsive breakpoints: 768px, 480px
- All event cards use CSS Grid layout (auto-fill, minmax(350px, 1fr))
- Softer colors and animations (updated from harsh original design)

## Automated Event Scraping System

The application includes a GitHub Actions workflow that automatically scrapes and updates events daily.

### Architecture

**GitHub Actions Workflow** (`.github/workflows/update-events.yml`):
- Runs daily at 6:00 AM UTC (configurable with cron syntax)
- Can be manually triggered via "workflow_dispatch"
- Requires Python 3.11 and dependencies (beautifulsoup4, requests, lxml)
- Commits and pushes changes automatically using GitHub Actions Bot

**Python Scraper** (`scripts/scrape-events.py`):
- **Google Custom Search API**: Primary source for Kosovo events (requires `GOOGLE_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID` GitHub Secrets)
- **Eventbrite**: Scrapes multiple Kosovo cities (Pristina, Prizren, Peja, Gjakova, Gjilan, Ferizaj, Mitrovica)
- **Intelligent Category Detection**: Uses keyword matching to auto-categorize events
- **Date Extraction**: Parses various date formats (ISO, month names, date ranges)
- **Image Pool System**: Assigns diverse category-appropriate images from Unsplash pools
- **Duplicate Prevention**: Filters out duplicate events by title matching

### Key Features

1. **Relaxed Date Requirement**: Accepts events with and without specific dates
   - Events WITH dates (e.g., "Nov 22") are sorted chronologically and shown first
   - Events WITHOUT dates get "Coming Soon" and are shown at the end
   - This increases discovery from ~2 events/day to 50-60+ events/day
2. **Smart Updates**: Appends new events to existing `MANUAL_EVENTS` array in `index.html`
3. **API Rate Limiting**: Respects Google's free tier with 33 queries × 2 results = 66 API calls/day (under 100 limit)
4. **Multi-City Coverage**: Searches all major Kosovo cities automatically
5. **Category Intelligence**: Auto-detects event type from title/description keywords
6. **Targeted Queries**: 33 optimized searches including venue-specific (Zone Club, Kino ARMATA), Albanian language queries, and festival searches

### Testing Locally

```bash
python3 scripts/scrape-events.py
```

### Required GitHub Secrets

Add these to Settings → Secrets and variables → Actions:
- `GOOGLE_API_KEY` - Get from https://developers.google.com/custom-search/v1/overview
- `GOOGLE_SEARCH_ENGINE_ID` - Create at https://programmablesearchengine.google.com/

### Customization

**Change scraping schedule** in `.github/workflows/update-events.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 6,18 * * *'  # Twice daily (6 AM and 6 PM)
```

**Add event sources** in `scripts/scrape-events.py`:
- Implement new scraping functions (e.g., `scrape_facebook_events()`)
- Add to `scrape_events()` main function
- Follow existing event structure (see Event Structure below)

### Event Structure

Each scraped event must include:
```python
{
    'title': 'Albanian title',
    'titleEn': 'English title',
    'description': 'Albanian description',
    'descriptionEn': 'English description',
    'date': 'Nov 25' or 'Nov 25-30',
    'time': '7:00 PM',
    'location': 'Prishtina, Kosovo',
    'image': 'https://images.unsplash.com/...',
    'category': 'bars|museum|outdoor|restaurant|concert',
    'url': 'https://event-source.com',
    'source': 'Source Name',
    'isLive': True  # False for permanent venues
}
```

## Development Workflow

### Adding Events Manually vs. Automated Scraping

- **Manual events** in `MANUAL_EVENTS` array are preserved by the scraper
- **Scraped events** are appended to the array automatically
- Both types are rendered together by `renderDynamicEvents()` function
- The scraper never removes manually-added events

### Deployment

1. **GitHub Pages** (recommended):
   - Push to GitHub repository
   - Enable in Settings → Pages → Source: main branch
   - Site deploys to `https://username.github.io/dola/`

2. **Auto-Updates**:
   - GitHub Actions runs scraper daily
   - New events are committed automatically
   - GitHub Pages re-deploys with updated content

### Troubleshooting Scraper

- **No events found**: Check GitHub Actions logs in Actions tab
- **Scraper failing**: Verify secrets are configured correctly
- **Rate limiting**: Reduce number of search queries in `scrape-events.py`
- **Invalid syntax**: Run `node -e "..."` command to validate JavaScript syntax
- **Events not showing**: Clear browser cache and localStorage
