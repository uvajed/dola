#!/usr/bin/env python3
"""
Event Scraper for Dola
Scrapes events from various public sources and updates index.html
NO GOOGLE SCRAPING - Uses direct source websites instead
"""

import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

# User-Agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_eventbrite():
    """
    Scrape events from Eventbrite Kosovo
    Public data, no API key needed
    """
    events = []

    try:
        print("🔍 Scraping Eventbrite Kosovo...")
        url = "https://www.eventbrite.com/d/kosovo--pristina/events/"
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Eventbrite uses structured data - look for event cards
            event_items = soup.find_all('div', class_='discover-search-desktop-card')[:5]  # Get first 5

            for item in event_items:
                try:
                    # Extract event details
                    title_elem = item.find('h2') or item.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else None

                    if title:
                        event = {
                            'title': title,
                            'titleEn': title,
                            'description': 'Event in Kosovo. Check Eventbrite for full details.',
                            'descriptionEn': 'Event in Kosovo. Check Eventbrite for full details.',
                            'date': 'Coming Soon',
                            'time': 'TBA',
                            'location': 'Prishtina, Kosovo',
                            'image': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400',
                            'category': 'outdoor',
                            'url': 'https://www.eventbrite.com/d/kosovo--pristina/events/',
                            'source': 'Eventbrite',
                            'isLive': True
                        }
                        events.append(event)
                        print(f"  ✅ Found: {title}")
                except Exception as e:
                    print(f"  ⚠️ Error parsing event: {e}")
                    continue

    except Exception as e:
        print(f"❌ Error scraping Eventbrite: {e}")

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

    # Scrape from various sources
    eventbrite_events = scrape_eventbrite()
    all_events.extend(eventbrite_events)

    # Add more sources here
    # rss_events = scrape_public_calendar_feeds()
    # all_events.extend(rss_events)

    print("=" * 50)
    print(f"✅ Found {len(all_events)} total new events")

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
