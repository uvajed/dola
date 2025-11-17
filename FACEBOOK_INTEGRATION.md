# Facebook Integration Guide for Dola

## ✅ AUTOMATIC EVENT FETCHING NOW ENABLED!

Your Dola site now includes **automatic event fetching** from Facebook! The system is built-in and ready to use once you configure it.

### What's Included:
- ✅ Facebook Graph API integration
- ✅ Automatic event updates every hour
- ✅ Dynamic event rendering
- ✅ Event caching in browser
- ✅ Easy manual event additions

---

## SETUP: Enable Facebook Events (5 Minutes)

### Step 1: Create Facebook App

1. Go to: https://developers.facebook.com/apps/
2. Click **"Create App"**
3. Choose **"Business"** type
4. App Name: **"Dola Events Aggregator"**
5. Click "Create App"

### Step 2: Get Your App ID

1. In your app dashboard, you'll see your **App ID**
2. Copy this number (example: `532619825283746`)

### Step 3: Get Page Access Token

1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown
3. Click "Get Token" → "Get Page Access Token"
4. Select the Kosovo event pages you want to fetch from
5. Copy the **Page Access Token** (long string)

### Step 4: Configure Dola

Open `index.html` and update lines 666-672:

```javascript
const FB_CONFIG = {
    appId: '532619825283746', // Your App ID here
    pageAccessToken: 'YOUR_ACTUAL_TOKEN_HERE', // Your Page Access Token
    pages: [
        'zoneclub',           // ZONE Club Prishtina page
        'kosovoevents',       // Add other Kosovo event pages
        'pristina.events',    // Add as many as you want!
    ]
};
```

### Step 5: Find Kosovo Event Pages

Search Facebook for pages that post Kosovo events:
- "Kosovo Events"
- "Prishtina Events"
- "ZONE Club" (nightlife)
- "Visit Kosovo"
- Venue/club pages

Get their Page IDs and add to the `pages` array.

---

## BONUS: Add Manual Events (Super Easy!)

Don't want to wait for API setup? Add events manually in `index.html` (lines 743-756):

```javascript
const MANUAL_EVENTS = [
    {
        title: "Summer Music Festival 2025",
        description: "The biggest music festival in Kosovo!",
        date: "July 15",
        time: "8:00 PM",
        location: "Germia Park, Prishtina",
        image: "https://images.unsplash.com/photo-event.jpg",
        category: "concert",
        url: "https://google.com/search?q=summer+music+festival+kosovo",
        isLive: true
    },
    // Add more events here!
];
```

The site will combine Facebook events + manual events automatically!

---

## Option 1: Share Your Page on Facebook (EASIEST)

### Step 1: Host Your Website
You need to host your page online first. Free options:
- **GitHub Pages** (Free, easiest)
- **Netlify** (Free)
- **Vercel** (Free)

#### Quick GitHub Pages Setup:
1. Create a GitHub account
2. Create a new repository called "dola"
3. Upload your `index.html` and `styles.css`
4. Go to Settings → Pages → Enable GitHub Pages
5. Your site will be at: `https://yourusername.github.io/dola/`

### Step 2: Update Meta Tags
Replace `https://yourdomain.com` in the meta tags with your actual URL.

### Step 3: Test Facebook Sharing
Go to https://developers.facebook.com/tools/debug/ and enter your URL to see how it looks when shared.

---

## Option 2: Create a Facebook Page for Dola

1. Go to https://www.facebook.com/pages/create
2. Choose "Community or Public Figure"
3. Name it "Dola - Kosovo Events"
4. Add description: "Discover events, bars, restaurants, and activities across Kosovo"
5. Add your website link once hosted
6. Post events from your website to the Facebook page

---

## Option 3: Pull Real Events from Facebook (ADVANCED)

To fetch real Facebook Events into your app:

### Step 1: Create Facebook App
1. Go to https://developers.facebook.com/
2. Create a Developer Account
3. Click "My Apps" → "Create App"
4. Choose "Business" type
5. Name: "Dola Events Aggregator"

### Step 2: Get Access Token
1. In your app dashboard, go to Tools → Graph API Explorer
2. Select your app
3. Add permissions: `pages_read_engagement`, `pages_show_list`
4. Generate Access Token

### Step 3: Add JavaScript to Fetch Events

Add this to your HTML before the closing `</body>` tag:

```javascript
// Facebook SDK Integration
window.fbAsyncInit = function() {
    FB.init({
        appId      : 'YOUR_APP_ID',
        xfbml      : true,
        version    : 'v18.0'
    });
};

// Load Facebook SDK
(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Fetch Facebook Events
async function fetchFacebookEvents() {
    const accessToken = 'YOUR_ACCESS_TOKEN';
    const pageId = 'FACEBOOK_PAGE_ID'; // Page that posts Kosovo events

    try {
        const response = await fetch(
            `https://graph.facebook.com/v18.0/${pageId}/events?access_token=${accessToken}`
        );
        const data = await response.json();

        // Process and display events
        displayFacebookEvents(data.data);
    } catch (error) {
        console.error('Error fetching Facebook events:', error);
    }
}

function displayFacebookEvents(events) {
    const newsFeed = document.querySelector('.news-feed');

    events.forEach(event => {
        const eventCard = `
            <article class="event-card event-card-live" data-category="concert">
                <div class="event-badge">🎉 LIVE EVENT</div>
                <div class="event-image" style="background-image: url('${event.cover?.source || 'default.jpg'}');"></div>
                <div class="event-content">
                    <div class="event-header">
                        <span class="event-category concert">Events</span>
                        <span class="event-time">${new Date(event.start_time).toLocaleDateString()}</span>
                    </div>
                    <h2 class="event-title">${event.name}</h2>
                    <p class="event-description">${event.description || 'No description'}</p>
                    <div class="event-footer">
                        <span class="event-location">📍 ${event.place?.name || 'TBA'}</span>
                        <span class="event-source">Source: Facebook</span>
                    </div>
                    <button class="maps-btn" onclick="window.open('https://facebook.com/events/${event.id}', '_blank')">View on Facebook</button>
                </div>
            </article>
        `;
        newsFeed.insertAdjacentHTML('afterbegin', eventCard);
    });
}
```

### Step 4: Find Kosovo Event Pages
Search Facebook for pages that post Kosovo events:
- "Kosovo Events"
- "Prishtina Events"
- "Visit Kosovo"
- Venue pages (ZONE Club, etc.)

Get their Page IDs and fetch events from each.

---

## Option 4: Embed Facebook Page Plugin

Add this to show your Facebook page feed on your website:

```html
<!-- Add where you want the feed to appear -->
<div id="fb-root"></div>
<div class="fb-page"
     data-href="https://www.facebook.com/yourpage"
     data-tabs="timeline,events"
     data-width="500"
     data-height="700"
     data-small-header="false"
     data-adapt-container-width="true"
     data-hide-cover="false"
     data-show-facepile="true">
</div>
```

---

## Recommended Approach

**For Quick Start:**
1. Host on GitHub Pages (5 minutes)
2. Create a Facebook Page (10 minutes)
3. Share your website link on the page
4. Post event updates manually or use Facebook Graph API later

**For Advanced Integration:**
1. Get Facebook Developer account
2. Create app and get API access
3. Fetch real events from Facebook Events
4. Auto-update every hour (you already have this!)

---

## Security Notes

- Never commit API keys to GitHub
- Use environment variables for tokens
- Rotate access tokens regularly
- Follow Facebook's API rate limits

---

## Next Steps

1. **Choose hosting** (GitHub Pages recommended)
2. **Update meta tags** with your real URL
3. **Create Facebook Page** for Dola
4. **Test sharing** on Facebook
5. **(Optional) Add Facebook API** for real events

Need help with any specific step? Let me know!
