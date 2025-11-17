#!/usr/bin/env python3
"""
Event Scraper for Dola
Scrapes events from various public sources and updates index.html
Supports: Facebook Graph API, Eventbrite, RSS feeds
"""

import re
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

# User-Agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Facebook Configuration (from GitHub Secrets)
FB_APP_ID = os.environ.get('FB_APP_ID', '')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN', '')

# Kosovo Facebook Pages to scrape events from
FACEBOOK_PAGES = [
    'kinoarmata',        # Kino ARMATA
    'zoneclubpr',        # ZONE Club
    'vendum.ks',         # Vendum
    # Add more Kosovo event pages here
]

def scrape_facebook_events():
    """
    Scrape events from Facebook pages using Graph API
    Requires FB_APP_ID and FB_PAGE_TOKEN environment variables
    """
    events = []

    if not FB_PAGE_TOKEN or not FB_APP_ID:
        print("⚠️  Facebook API not configured (FB_APP_ID or FB_PAGE_TOKEN missing)")
        print("   Add tokens to GitHub Secrets to enable Facebook scraping")
        print("   See FACEBOOK_AUTO_SCRAPING.md for setup instructions")
        return events

    print("🔍 Scraping Facebook events...")

    for page_id in FACEBOOK_PAGES:
        try:
            # Facebook Graph API endpoint
            url = f"https://graph.facebook.com/v18.0/{page_id}/events"
            params = {
                'access_token': FB_PAGE_TOKEN,
                'fields': 'name,description,start_time,end_time,place,cover',
                'time_filter': 'upcoming',
                'limit': 10
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and len(data['data']) > 0:
                    for fb_event in data['data']:
                        try:
                            # Parse event date
                            start_time = datetime.fromisoformat(fb_event['start_time'].replace('Z', '+00:00'))
                            event_date = start_time.strftime('%b %d')
                            event_time = start_time.strftime('%I:%M %p')

                            # Get location
                            location = 'Kosovo'
                            if 'place' in fb_event and 'name' in fb_event['place']:
                                location = fb_event['place']['name']

                            # Get cover image
                            image = 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400'
                            if 'cover' in fb_event and 'source' in fb_event['cover']:
                                image = fb_event['cover']['source']

                            # Get description (truncate if too long)
                            description = fb_event.get('description', 'Event in Kosovo')[:200]
                            if len(fb_event.get('description', '')) > 200:
                                description += '...'

                            event = {
                                'title': fb_event['name'],
                                'titleEn': fb_event['name'],
                                'description': description,
                                'descriptionEn': description,
                                'date': event_date,
                                'time': event_time,
                                'location': location,
                                'image': image,
                                'category': 'concert',  # Default category
                                'url': f"https://facebook.com/events/{fb_event['id']}",
                                'source': f'Facebook ({page_id})',
                                'isLive': True
                            }
                            events.append(event)
                            print(f"  ✅ Found: {fb_event['name'][:50]}... ({event_date})")

                        except Exception as e:
                            print(f"  ⚠️ Error parsing event: {e}")
                            continue
                else:
                    print(f"  ℹ️  No upcoming events for {page_id}")

            elif response.status_code == 400:
                print(f"  ❌ Invalid token or page ID: {page_id}")
            else:
                print(f"  ❌ Error fetching from {page_id}: {response.status_code}")

        except Exception as e:
            print(f"  ❌ Error with page {page_id}: {e}")

    return events


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
                                event = {
                                    'title': title,
                                    'titleEn': title,
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
                        event = {
                            'title': title,
                            'titleEn': title,
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

    # Scrape from Facebook (if configured)
    facebook_events = scrape_facebook_events()
    all_events.extend(facebook_events)

    # Scrape from Eventbrite
    eventbrite_events = scrape_eventbrite()
    all_events.extend(eventbrite_events)

    # Add more sources here
    # rss_events = scrape_public_calendar_feeds()
    # all_events.extend(rss_events)

    print("=" * 50)
    print(f"✅ Found {len(all_events)} total new events")
    print(f"   - Facebook: {len(facebook_events)} events")
    print(f"   - Eventbrite: {len(eventbrite_events)} events")

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

    # Generate new events JavaScript
    new_events_js = []
    for event in events:
        event_js = f"""
            {{
                title: "{event['title']}",
                titleEn: "{event['titleEn']}",
                description: "{event['description']}",
                descriptionEn: "{event['descriptionEn']}",
                date: "{event['date']}",
                time: "{event['time']}",
                location: "{event['location']}",
                image: "{event['image']}",
                category: "{event['category']}",
                url: "{event['url']}",
                source: "{event['source']}",
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
