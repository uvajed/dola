# Dola - Kosovo Event Discovery Platform

Discover live events, bars, restaurants, museums, and activities across Kosovo - Prishtina, Peja, Prizren & more!

🌐 **Live Site:** [dola.kosovo](https://uvajed.github.io/dola/) *(update with your actual URL)*

## Features

- 🎉 **Live Events & Permanent Venues** - Time-specific events and always-open locations
- 🌍 **Bilingual** - Full support for Albanian (SQ) and English (EN)
- 🔍 **Smart Search** - Search by city, event name, location, or category
- 🏷️ **Category Filtering** - Bars & Nightlife, Museums & Culture, Outdoor, Restaurants, Concerts
- 🤖 **Auto-Update** - GitHub Actions automatically scrapes and updates events daily
- 📱 **Responsive Design** - Works perfectly on mobile, tablet, and desktop

## Auto-Update System

Events are automatically updated every 24 hours via GitHub Actions:

1. Scraper runs daily at 6:00 AM UTC
2. Fetches new events from configured sources
3. Updates `index.html` automatically
4. Commits and pushes changes
5. GitHub Pages deploys the updated site

**Configure:** See `scripts/README.md` for customization options

## Local Development

Simply open `index.html` in your browser - no build process required!

```bash
open index.html
```

## Project Structure

```
Dola/
├── index.html              # Main page (events included here)
├── styles.css              # All styling
├── dola.jpg                # Social media preview image
├── CLAUDE.md               # Project guidelines for AI assistants
├── .github/
│   └── workflows/
│       └── update-events.yml   # GitHub Actions workflow
└── scripts/
    ├── scrape-events.py    # Event scraper
    └── README.md           # Scraper documentation
```

## Adding Events Manually

### Static HTML Events

Add events directly in `index.html` under the `<!-- TIME-SPECIFIC EVENTS -->` section:

```html
<article class="event-card event-card-live" data-category="concert" onclick="window.open('URL', '_blank')">
    <div class="event-badge">🎉 LIVE EVENT</div>
    <div class="event-image" style="background-image: url('IMAGE_URL');"></div>
    <div class="event-content">
        <div class="event-header">
            <span class="event-category concert">Concerts & Shows</span>
            <span class="event-time">Nov 20, 8:00 PM</span>
        </div>
        <h2 class="event-title" data-lang-en="Event Title" data-lang-sq="Titulli i Eventit">Titulli i Eventit</h2>
        <p class="event-description" data-lang-en="Description..." data-lang-sq="Përshkrimi...">Përshkrimi...</p>
        <div class="event-footer">
            <span class="event-location">📍 Location</span>
            <span class="event-source">Source: Example</span>
        </div>
        <button class="maps-btn" onclick="event.stopPropagation(); window.open('MAPS_URL', '_blank')">📍 View on Maps</button>
    </div>
</article>
```

### Dynamic JavaScript Events

Add events to the `MANUAL_EVENTS` array in `index.html`:

```javascript
const MANUAL_EVENTS = [
    {
        title: "Titulli në Shqip",
        titleEn: "Title in English",
        description: "Përshkrimi në shqip...",
        descriptionEn: "Description in English...",
        date: "Nov 20",
        time: "8:00 PM",
        location: "Prishtina",
        image: "https://images.unsplash.com/...",
        category: "concert", // bars, museum, outdoor, restaurant, concert
        url: "https://example.com",
        source: "Source Name",
        isLive: true
    }
];
```

## Categories

- `bars` - Bars & Nightlife
- `museum` - Museums & Culture
- `outdoor` - Outdoor Activities
- `restaurant` - Restaurants
- `concert` - Concerts & Shows

## Deployment

### GitHub Pages

1. Push your code to GitHub
2. Go to Settings → Pages
3. Select branch: `main` (or `master`)
4. Click Save
5. Your site will be live at `https://yourusername.github.io/dola/`

### Custom Domain (Optional)

1. Add a `CNAME` file with your domain: `events.yourdomain.com`
2. Configure DNS at your domain provider
3. Enable HTTPS in GitHub Pages settings

## Technologies

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - No frameworks, pure JS
- **GitHub Actions** - Automated event updates
- **Python** - Event scraping (BeautifulSoup, Requests)

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is open source and available for anyone to use and modify.

## Contact

For issues or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for Kosovo**
