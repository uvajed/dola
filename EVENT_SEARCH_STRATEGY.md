# Kosovo Event Search Strategy

## Kosovo Cities to Search

### Major Cities:
1. **Prishtina** (Pristina) - Capital, largest city
2. **Prizren** - Cultural capital, many festivals
3. **Peja** (Peć) - Western Kosovo, outdoor events
4. **Gjakova** (Đakovica) - Historic city
5. **Ferizaj** (Uroševac) - Central Kosovo
6. **Gjilan** (Gnjilane) - Eastern Kosovo
7. **Mitrovica** - Northern Kosovo

### Search Terms by City:

**Prishtina:**
- "Prishtina events"
- "Pristina events"  
- "Prishtinë ngjarje"
- "Events in Prishtina Kosovo"

**Prizren:**
- "Prizren events"
- "Prizren festival"
- "DokuFest Prizren"
- "Prizren ngjarje"

**Peja:**
- "Peja events"
- "Peja outdoor"
- "Rugova events"
- "Peja hiking"

## Better Event Sources

### 1. Eventbrite (Works!)
```
https://www.eventbrite.com/d/kosovo--pristina/events/
https://www.eventbrite.com/d/kosovo--prizren/events/
https://www.eventbrite.com/d/kosovo/events/
```

### 2. Facebook Events (Needs API)
**Major Kosovo Pages:**
- Kino ARMATA (@kinoarmata)
- ZONE Club (@zoneclubpr)
- Vendum (@vendum.ks)
- Dokufest (@dokufest)
- Prishtina Insight (@prishtinainsight)
- Visit Kosovo (@visitkosovo)
- Kosovo 2.0 (@kosovo2point0)

### 3. Instagram (Manual/API)
**Event Organizers:**
- @kosovophilharmonic
- @luluscoffeeandwine
- @vendum.ks
- @zoneclubpr
- @dokufest
- @pristina.events (if exists)

### 4. Local Event Sites
```
https://evendo.com/kosovo
https://www.allaboutalbania.com/kosovo-events/
https://www.timeout.com/pristina
```

### 5. Tourism Boards
```
https://www.visitkosova.org/en/events/
https://www.kosovo-online.com/events
```

### 6. Universities & Cultural Centers
- University of Prishtina events
- Prishtina National Theatre
- National Gallery of Kosovo
- Ethnographic Museum events

### 7. DokuFest (Major Festival)
```
https://dokufest.com/
Annual documentary & short film festival in Prizren
Huge cultural event (August)
```

### 8. Music Venues
- Kino ARMATA (Cinema & events)
- ODA Theatre
- National Theatre
- Germia Park events
- SHPIJA e Vjetër

## Search Strategy by Category

### Concerts & Music:
- Search: "Kosovo concerts", "Prishtina live music", "Prizren festival"
- Sources: Facebook events, venue websites, Bandsintown alternatives
- Keywords: "koncert", "muzikë live", "festival"

### Cultural Events:
- DokuFest (Prizren)
- MOISIU Festival (Prishtina)
- Prishtina Jazz Festival
- Search: "Kosovo cultural events", "festival kulturor"

### Nightlife:
- ZONE Club, Duplex Club, Venom Nightclub
- Search: "Prishtina nightlife", "Kosovo nightclubs"
- Keywords: "jetë nate", "natë"

### Outdoor & Sports:
- Rugova Canyon events
- Sharr Mountains hiking
- Football matches (Stadiumi Fadil Vokrri)
- Search: "Kosovo outdoor", "hiking Kosovo", "sport events"

### Food & Drink:
- Restaurant events
- Wine tastings
- Food festivals
- Search: "Kosovo food festival", "Prishtina restaurants"

## Automated Search Approach

### Multi-Source Scraper:

1. **Eventbrite Kosovo** (Easy, no API needed)
   - Search all Kosovo cities
   - Filter by date
   - Extract structured data

2. **Google Search API** (If available)
   - "events in Prishtina Kosovo [this month]"
   - "things to do Kosovo [this weekend]"
   - "Kosovo concerts [date]"

3. **Social Media Aggregation**
   - Facebook Graph API (when setup complete)
   - Instagram hashtags: #kosovevents #prishtinaevents #prizrenevents
   - Twitter/X: @visitkosovo posts

4. **RSS Feeds**
   - Kosovo news sites event sections
   - Tourism board RSS
   - Cultural organization feeds

5. **Structured Data Scraping**
   - Schema.org markup from event sites
   - iCal/Calendar feeds
   - JSON-LD event data

## Implementation Plan

### Phase 1: Eventbrite Multi-City
```python
KOSOVO_CITIES = ['pristina', 'prizren', 'peja', 'gjakova', 'gjilan', 'ferizaj']

for city in KOSOVO_CITIES:
    url = f"https://www.eventbrite.com/d/kosovo--{city}/events/"
    scrape_eventbrite(url, city)
```

### Phase 2: Facebook Pages
```python
KOSOVO_FB_PAGES = [
    'kinoarmata', 'zoneclubpr', 'vendum.ks',
    'dokufest', 'visitkosovo', 'prishtinainsight'
]
```

### Phase 3: Tourism Boards
```python
scrape_visitkosova()
scrape_local_news_events()
```

### Phase 4: Smart Search
- Google Custom Search API for "Kosovo events"
- Aggregate results from multiple sources
- Deduplicate events
- Rank by relevance

## Search Keywords (Albanian)

- "ngjarje" - events
- "festival" - festival
- "koncert" - concert
- "shfaqje" - show/performance
- "muzikë live" - live music
- "ekspozitë" - exhibition
- "teatër" - theatre
- "spo rt" - sports
- "ushqim" - food
- "artë" - art

## Expected Results

By implementing this multi-city, multi-source approach:
- **50-100 events** across Kosovo cities
- **Weekly updates** from multiple sources
- **Better coverage** beyond just Prishtina
- **Diverse categories** (culture, music, food, sports, outdoor)

## Next Steps

1. Implement Eventbrite multi-city scraper
2. Add Visit Kosovo scraper
3. Set up Facebook API for major venues
4. Create event deduplication logic
5. Add city filters to frontend

---

This strategy provides comprehensive event coverage across all of Kosovo!
