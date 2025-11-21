#!/usr/bin/env python3
"""
Event Scraper for Dola
Scrapes events from various public sources and updates index.html
Supports: Facebook Graph API, Eventbrite, RSS feeds
"""

import re
import json
import os
import random
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

# User-Agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Diverse image pools for each category (multiple images to avoid repetition)
IMAGE_POOLS = {
    'concert': [
        'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400',  # Concert crowd
        'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400',  # Live music
        'https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=400',  # Music festival
        'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400',  # Stage performance
        'https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400',  # DJ/electronic
    ],
    'bars': [
        'https://images.unsplash.com/photo-1566417713940-fe7c737a9ef2?w=400',  # Cocktail bar
        'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=400',  # Night bar
        'https://images.unsplash.com/photo-1543007630-9710e4a00a20?w=400',  # Bar interior
        'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=400',  # Drinks
        'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400',  # Nightlife
    ],
    'museum': [
        'https://images.unsplash.com/photo-1518998053901-5348d3961a04?w=400',  # Art gallery
        'https://images.unsplash.com/photo-1564399579883-451a5d44ec08?w=400',  # Museum interior
        'https://images.unsplash.com/photo-1577083552431-6e5fd01988ec?w=400',  # Exhibition
        'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=400',  # Theater/culture
        'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400',  # Cinema
    ],
    'restaurant': [
        'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',  # Restaurant interior
        'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400',  # Fine dining
        'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400',  # Food spread
        'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400',  # Cafe atmosphere
        'https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=400',  # Modern restaurant
    ],
    'outdoor': [
        'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400',  # Outdoor event
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',  # Mountains
        'https://images.unsplash.com/photo-1501555088652-021faa106b9b?w=400',  # Hiking
        'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400',  # Mountain landscape
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',  # Nature activity
        'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400',  # Ski resort
        'https://images.unsplash.com/photo-1483921020237-2ff51e8e4b22?w=400',  # Adventure sports
    ]
}

# Keywords to detect event category from title/description
CATEGORY_KEYWORDS = {
    'concert': ['concert', 'music', 'festival', 'band', 'jazz', 'rock', 'dj', 'performance', 'show', 'stage', 'koncert', 'muzik', 'festival'],
    'bars': ['bar', 'club', 'nightlife', 'party', 'drinks', 'cocktail', 'lounge', 'pub', 'nightclub', 'club', 'ballë'],
    'museum': ['museum', 'gallery', 'art', 'exhibition', 'theater', 'theatre', 'cinema', 'film', 'movie', 'culture', 'cultural', 'muzeu', 'galeri', 'teatr', 'kino'],
    'restaurant': ['restaurant', 'food', 'dining', 'cafe', 'coffee', 'brunch', 'dinner', 'lunch', 'restorant', 'ushqim'],
    'outdoor': ['outdoor', 'hiking', 'mountain', 'ski', 'nature', 'adventure', 'trail', 'park', 'sports', 'malet', 'natyra']
}

# Facebook scraping removed per user request


def detect_category(title, description):
    """
    Intelligently detect event category from title and description
    Returns the best matching category, defaulting to 'outdoor'
    """
    text = (title + ' ' + description).lower()

    # Score each category based on keyword matches
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        scores[category] = score

    # Return category with highest score, or 'outdoor' if no matches
    best_category = max(scores.items(), key=lambda x: x[1])
    return best_category[0] if best_category[1] > 0 else 'outdoor'


def get_random_image(category):
    """
    Get a random image from the category's image pool
    Returns a diverse image to avoid repetition
    """
    if category in IMAGE_POOLS:
        return random.choice(IMAGE_POOLS[category])
    # Fallback to outdoor images if category not found
    return random.choice(IMAGE_POOLS['outdoor'])


def extract_date_from_text(text):
    """
    Extract event date from text using regex patterns
    Returns (date_string, has_specific_date) tuple
    """
    import re
    from datetime import datetime

    text_lower = text.lower()
    current_year = datetime.now().year
    current_month_num = datetime.now().month

    # Month name mapping
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    # Pattern 1: "November 22, 2025" or "Nov 22, 2025"
    match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2}),?\s+(\d{4})', text_lower)
    if match:
        month_name, day, year = match.groups()
        month_num = months.get(month_name)
        if month_num and int(year) >= current_year:
            # Check if date is in the past
            event_date = datetime(int(year), month_num, int(day))
            if event_date.date() >= datetime.now().date():
                return (f"{month_name.capitalize()} {day}", True)

    # Pattern 2: "22 November 2025" or "22 Nov 2025"
    match = re.search(r'(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{4})', text_lower)
    if match:
        day, month_name, year = match.groups()
        month_num = months.get(month_name)
        if month_num and int(year) >= current_year:
            event_date = datetime(int(year), month_num, int(day))
            if event_date.date() >= datetime.now().date():
                return (f"{month_name.capitalize()} {day}", True)

    # Pattern 3: "November 22-24" (date range)
    match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})\s*-\s*(\d{1,2})', text_lower)
    if match:
        month_name, start_day, end_day = match.groups()
        month_num = months.get(month_name)
        if month_num and month_num >= current_month_num:
            return (f"{month_name.capitalize()} {start_day}-{end_day}", True)

    # Pattern 4: "2025-11-22" (ISO format)
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
    if match:
        year, month, day = match.groups()
        if int(year) >= current_year:
            event_date = datetime(int(year), int(month), int(day))
            if event_date.date() >= datetime.now().date():
                month_name = list(months.keys())[int(month) - 1]
                return (f"{month_name.capitalize()} {int(day)}", True)

    # No specific date found
    return ('Coming Soon', False)


# Facebook scraping function removed per user request


def scrape_eventbrite():
    """
    Scrape events from Eventbrite - ALL Kosovo cities!
    Public data, no API key needed
    """
    all_events = []

    # Major Kosovo cities to search
    KOSOVO_CITIES = [
        ('pristina', 'Prishtina'),
        ('prizren', 'Prizren'),
        ('peja', 'Peja'),
        ('gjakova', 'Gjakova'),
        ('gjilan', 'Gjilan'),
        ('ferizaj', 'Ferizaj'),
        ('mitrovica', 'Mitrovica'),
        ('kosovo', 'Kosovo')  # General Kosovo events
    ]

    for city_slug, city_name in KOSOVO_CITIES:
        try:
            print(f"🔍 Searching Eventbrite: {city_name}...")
            url = f"https://www.eventbrite.com/d/kosovo--{city_slug}/events/"
            response = requests.get(url, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Eventbrite uses structured data - look for event cards
                event_items = soup.find_all('div', class_='discover-search-desktop-card')[:3]  # Get first 3 per city

                for item in event_items:
                    try:
                        # Extract event details
                        title_elem = item.find('h2') or item.find('h3')
                        title = title_elem.get_text(strip=True) if title_elem else None

                        if title:
                            # Avoid duplicates
                            if not any(e['title'] == title for e in all_events):
                                # IMPORTANT: Keep original title - NEVER translate event titles!
                                # Only descriptions can be translated, titles stay in original language
                                event = {
                                    'title': title,  # Original title (NEVER translate)
                                    'titleEn': title,  # Keep same as original
                                    'description': f'Event in {city_name}, Kosovo. Check Eventbrite for full details.',
                                    'descriptionEn': f'Event in {city_name}, Kosovo. Check Eventbrite for full details.',
                                    'date': 'Coming Soon',
                                    'time': 'TBA',
                                    'location': f'{city_name}, Kosovo',
                                    'image': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400',
                                    'category': 'outdoor',
                                    'url': url,
                                    'source': f'Eventbrite ({city_name})',
                                    'isLive': True
                                }
                                all_events.append(event)
                                print(f"  ✅ {city_name}: {title[:50]}...")
                    except Exception as e:
                        print(f"  ⚠️ Error parsing event: {e}")
                        continue
            else:
                print(f"  ℹ️  No events found for {city_name}")

            # Be polite - small delay between requests
            import time
            time.sleep(0.5)

        except Exception as e:
            print(f"  ❌ Error with {city_name}: {e}")

    return all_events


def scrape_google_events():
    """
    Search Google for Kosovo events using Custom Search API
    Requires GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID in environment

    To set up:
    1. Get API key: https://developers.google.com/custom-search/v1/overview
    2. Create Search Engine: https://programmablesearchengine.google.com/
    3. Add to GitHub Secrets: GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    """
    events = []

    api_key = os.environ.get('GOOGLE_API_KEY', '')
    search_engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID', '')

    if not api_key or not search_engine_id:
        print("⚠️  Google Custom Search not configured")
        print("   Add GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID to GitHub Secrets")
        return events

    print("🔍 Searching Google for Kosovo events...")

    # Comprehensive search queries - organized by type
    from datetime import datetime
    current_month = datetime.now().strftime("%B %Y")
    current_year = datetime.now().year

    search_queries = [
        # TIME-SPECIFIC EVENT SEARCHES
        f"Kosovo events {current_month}",
        f"Prishtina events December {current_year}",
        "Kosovo nightlife this weekend",
        "concerts Prishtina tonight",
        f"Prizren festival {current_year}",

        # VENUE-SPECIFIC (Most likely to have events)
        "Zone Club Prishtina events",
        "Kino Armata Prishtina schedule",
        "ODA Theatre Prishtina program",
        "Duplex Club Prishtina",
        "Dit' e Nat' Prishtina events",
        "Hamam Jazz Bar Prishtina",
        "Termokiss Prishtina events",

        # EVENT TYPE + LOCATION
        f"live music Prishtina {current_month}",
        "DJ night Prishtina",
        f"art exhibition Pristina {current_year}",
        "film screening Kosovo",
        "food festival Prizren",
        f"Christmas market Prishtina {current_year}",

        # SOCIAL MEDIA & EVENT PLATFORMS
        "facebook events Prishtina Kosovo",
        "eventbrite Kosovo",
        f"Kosovo nightlife {current_month}",

        # ALBANIAN LANGUAGE (More Local Results)
        f"koncert Prishtinë {current_year}",
        "ngjarje Prishtinë sonte",
        f"festa Kosovë Nëntor {current_year}",
        "muzikë live Prishtinë",
        "ekspozitë Prishtinë",

        # SPECIFIC EVENT ORGANIZERS
        f"Sunny Hill Festival {current_year}",
        f"DokuFest {current_year} dates",
        f"Prishtina Film Festival {current_year}",
        f"Anibar Festival {current_year}",
        "Kosovo Wine Festival"
    ]

    # Limit queries to stay within Google's free tier (100 searches/day)
    # With 33 queries × 2 results = 66 API calls (well under 100/day limit)
    MAX_QUERIES = 33  # Increased from 16 for better coverage
    search_queries = search_queries[:MAX_QUERIES]

    print(f"   Running {len(search_queries)} searches (max {MAX_QUERIES*2} results)")

    for query in search_queries:
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': search_engine_id,
                'q': query,
                'num': 2  # Get 2 results per query (stay under free tier limit)
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if 'items' in data:
                    for item in data['items']:
                        title = item.get('title', 'Event in Kosovo')
                        snippet = item.get('snippet', 'Check Google for details')
                        link = item.get('link', 'https://google.com')

                        # Extract date from title and snippet
                        date_str, has_specific_date = extract_date_from_text(title + ' ' + snippet)

                        # Add all events (with and without specific dates)
                        # Events without dates will appear at the end of the list
                        if not any(e['title'] == title for e in events):
                            # Intelligently detect category and select diverse image
                            category = detect_category(title, snippet)
                            image = get_random_image(category)

                            # IMPORTANT: Keep original title - NEVER translate event titles!
                            # Only descriptions can be translated, titles stay in original language
                            event = {
                                'title': title[:100],  # Original title (NEVER translate)
                                'titleEn': title[:100],  # Keep same as original
                                'description': snippet[:200],
                                'descriptionEn': snippet[:200],
                                'date': date_str,  # Will be "Coming Soon" if no date found
                                'time': 'Check Website',
                                'location': 'Kosovo',
                                'image': image,
                                'category': category,
                                'url': link,
                                'source': 'Google Search',
                                'isLive': True
                            }
                            events.append(event)
                            if has_specific_date:
                                print(f"  ✅ Found: {title[:50]}... [{category}] on {date_str}")
                            else:
                                print(f"  ✅ Added (no date): {title[:50]}... [{category}]")
            else:
                print(f"  ❌ Error: {response.status_code}")

            import time
            time.sleep(0.5)  # Respect API rate limits

        except Exception as e:
            print(f"  ⚠️ Error searching Google: {e}")

    return events


def scrape_instagram_hashtags():
    """
    Search Instagram hashtags for Kosovo events

    WARNING: Instagram actively blocks scraping and has no public API.
    This method is:
    - Against Instagram's Terms of Service
    - Unreliable (Instagram blocks bots)
    - May not work at all

    Better alternatives:
    1. Manually check Instagram and add events to MANUAL_EVENTS
    2. Partner with venues to get event info directly
    3. Use Facebook Graph API (same company, better API support)
    """
    events = []

    print("⚠️  Instagram scraping is unreliable and against ToS")
    print("   Recommended: Manually add Instagram events to MANUAL_EVENTS")

    # Instagram doesn't provide a public API for this
    # Web scraping Instagram is blocked and against ToS
    # We'll skip this to avoid issues

    return events


def scrape_public_calendar_feeds():
    """
    Example: Scrape from public calendar feeds or RSS feeds
    Many venues publish RSS feeds of their events
    """
    events = []

    # Example RSS feeds (replace with actual Kosovo venue feeds)
    rss_feeds = [
        # 'https://example-venue.com/events/feed',
        # Add RSS feed URLs here
    ]

    for feed_url in rss_feeds:
        try:
            print(f"🔍 Checking RSS feed: {feed_url}")
            response = requests.get(feed_url, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                # Parse RSS feed with BeautifulSoup
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')[:5]

                for item in items:
                    title = item.find('title').get_text(strip=True) if item.find('title') else None
                    if title:
                        # IMPORTANT: Keep original title - NEVER translate event titles!
                        event = {
                            'title': title,  # Original title (NEVER translate)
                            'titleEn': title,  # Keep same as original
                            'description': 'Event from RSS feed',
                            'descriptionEn': 'Event from RSS feed',
                            'date': 'TBA',
                            'time': 'TBA',
                            'location': 'Kosovo',
                            'image': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400',
                            'category': 'concert',
                            'url': feed_url,
                            'source': 'RSS Feed',
                            'isLive': True
                        }
                        events.append(event)
        except Exception as e:
            print(f"⚠️ Error with feed {feed_url}: {e}")

    return events


def scrape_events():
    """
    Main scraper - combines all sources
    Returns list of event dictionaries
    """
    all_events = []

    print("🎉 Starting Event Scraper")
    print("=" * 50)

    # Scrape from Google Custom Search (if configured)
    google_events = scrape_google_events()
    all_events.extend(google_events)

    # Instagram scraping (not recommended - see function for details)
    instagram_events = scrape_instagram_hashtags()
    all_events.extend(instagram_events)

    print("=" * 50)
    print(f"✅ Found {len(all_events)} total new events")
    print(f"   - Google Search: {len(google_events)} events")
    print(f"   - Instagram: {len(instagram_events)} events")

    return all_events


def update_html_file(events):
    """
    Update index.html with new events
    """
    if not events:
        print("ℹ️  No new events to add")
        return

    print("📝 Updating index.html...")

    # Read current HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find the MANUAL_EVENTS array in the JavaScript
    pattern = r'const MANUAL_EVENTS = \[(.*?)\];'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        print("❌ Could not find MANUAL_EVENTS array")
        return

    # Parse existing events
    existing_events_str = match.group(1)

    # Helper function to escape quotes and special characters
    def escape_js_string(s):
        if not s:
            return ""
        # Replace double quotes with single quotes to avoid breaking strings
        s = s.replace('"', "'")
        # Remove newlines and carriage returns
        s = s.replace('\n', ' ').replace('\r', ' ')
        # Remove multiple spaces
        s = re.sub(r'\s+', ' ', s)
        return s.strip()

    # Generate new events JavaScript
    new_events_js = []
    for event in events:
        event_js = f"""
            {{
                title: "{escape_js_string(event['title'])}",
                titleEn: "{escape_js_string(event['titleEn'])}",
                description: "{escape_js_string(event['description'])}",
                descriptionEn: "{escape_js_string(event['descriptionEn'])}",
                date: "{escape_js_string(event['date'])}",
                time: "{escape_js_string(event['time'])}",
                location: "{escape_js_string(event['location'])}",
                image: "{event['image']}",
                category: "{event['category']}",
                url: "{event['url']}",
                source: "{escape_js_string(event['source'])}",
                isLive: {str(event['isLive']).lower()}
            }}"""
        new_events_js.append(event_js)

    # Combine existing and new events
    combined_events = existing_events_str.strip() + ',\n' + ',\n'.join(new_events_js)

    # Update HTML content
    updated_html = re.sub(
        pattern,
        f'const MANUAL_EVENTS = [{combined_events}\n        ];',
        html_content,
        flags=re.DOTALL
    )

    # Write updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"✅ Added {len(events)} new events to index.html")


def main():
    """Main function"""
    print("🎉 Dola Event Scraper Started")
    print("=" * 50)

    # Scrape events
    events = scrape_events()

    # Update HTML file
    update_html_file(events)

    print("=" * 50)
    print("✨ Done!")


if __name__ == '__main__':
    main()
