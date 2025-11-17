# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dola is a static HTML/CSS event aggregator application for Prishtina, Kosovo. It displays local events, venues, and activities in a hybrid model showing both time-specific events (with dates) and permanent venues (always available).

## Running the Application

Simply open `index.html` in any web browser. No build process, dependencies, or server required.

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

## Event Ordering System

All events in `MANUAL_EVENTS` array have an `order` property that controls display order:

- **Lower order numbers appear first** (e.g., `order: 1` appears before `order: 10`)
- **Live events**: Use order numbers 1-20 (sorted by date, soonest first)
- **Permanent venues**: Use order numbers 21+ (newest venues first)
- Events without an `order` property default to 999 (appear last)

The `renderDynamicEvents()` function automatically sorts by the `order` property before rendering.

### To Reorder Events:

Simply change the `order` number in the event object. For example, to move Brezovica to the top of permanent venues:

```javascript
{
    title: "Brezovica Ski Resort",
    // ... other properties
    order: 21  // Change this number to reorder
}
```

## Adding New Events

1. Add new event object to `MANUAL_EVENTS` array in `index.html`
2. Include all required properties:
   - `title`, `titleEn` (Albanian and English titles)
   - `description`, `descriptionEn`
   - `date`, `time`, `location`
   - `image` (Unsplash or event image URL)
   - `category` (`bars`, `museum`, `outdoor`, `restaurant`, or `concert`)
   - `url` (event website or Google search)
   - `source` (event source name)
   - `isLive` (`true` for time-specific events, `false` for permanent venues)
   - `order` (number determining display position)
3. Assign appropriate `order` number:
   - For live events: Use 1-20 range, ordered by date
   - For new venues: Use 21-30 range for newest venues
   - For older venues: Use 31+ range

## CSS Architecture

- Gradient theme: Purple (`#667eea` to `#764ba2`)
- Live event badge: Pink gradient with pulse animation
- Venue badge: Green gradient, no animation
- Responsive breakpoints: 768px, 480px
- All event cards use CSS Grid layout (auto-fill, minmax(350px, 1fr))
