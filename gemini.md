# Project Constitution

**Project Name:** Crypto Competitor Intelligence Dashboard
**Last Updated:** 2026-02-06
**Status:** Schema Definition Complete

---

## 1. Data Schemas

### Input Schema (Scraped Article)
```json
{
  "title": "string (required) - Article headline",
  "url": "string (required) - Article URL (unique)",
  "source": "string (required) - Publisher name (CoinDesk, CoinTelegraph, etc.)",
  "competitor": "string[] (required) - Mentioned competitors [Tangem|Trezor|Coinbase|Metamask|Revolut|Raby|Phantom]",
  "published_at": "ISO8601 datetime (required) - Article publish timestamp",
  "scraped_at": "ISO8601 datetime (required) - When we collected it",
  "summary": "string (optional) - Article snippet/description",
  "image_url": "string (optional) - Featured image URL",
  "author": "string (optional) - Article author",
  "sentiment": "string (optional) - positive|neutral|negative (future enhancement)"
}
```

### Output Schema (Dashboard API Response)
```json
{
  "articles": [
    {
      "id": "uuid (primary key)",
      "title": "string",
      "url": "string",
      "source": "string",
      "competitors": "string[]",
      "published_at": "ISO8601 datetime",
      "scraped_at": "ISO8601 datetime",
      "summary": "string",
      "image_url": "string",
      "author": "string",
      "is_saved": "boolean - User saved status",
      "saved_at": "ISO8601 datetime (nullable) - When user saved it",
      "share_token": "string (nullable) - UUID for sharing"
    }
  ],
  "metadata": {
    "total_count": "integer - Total articles in last 24h",
    "new_count": "integer - Articles added in last scrape",
    "saved_count": "integer - User's saved articles count",
    "last_updated": "ISO8601 datetime - Last scraper run",
    "has_new_data": "boolean - Whether new articles exist"
  }
}
```

### Supabase Tables

#### Table: `articles`
```sql
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL,
  source TEXT NOT NULL,
  competitors TEXT[] NOT NULL,
  published_at TIMESTAMPTZ NOT NULL,
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  summary TEXT,
  image_url TEXT,
  author TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_published_at ON articles(published_at DESC);
CREATE INDEX idx_competitors ON articles USING GIN(competitors);
```

#### Table: `saved_articles`
```sql
CREATE TABLE saved_articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  saved_at TIMESTAMPTZ DEFAULT NOW(),
  share_token UUID DEFAULT gen_random_uuid(),
  UNIQUE(article_id, user_id)
);

CREATE INDEX idx_user_saved ON saved_articles(user_id, saved_at DESC);
CREATE INDEX idx_share_token ON saved_articles(share_token);
```

#### Table: `scraper_runs`
```sql
CREATE TABLE scraper_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  articles_found INTEGER DEFAULT 0,
  articles_added INTEGER DEFAULT 0,
  status TEXT CHECK (status IN ('running', 'completed', 'failed')),
  error_message TEXT
);
```

---

## 2. Behavioral Rules

### System Behavior
- **Time Window**: Only display articles published in the last 24 hours
- **Scraper Frequency**: Run scrapers every 24 hours (cron job)
- **Empty State**: When no new articles exist, display clear message: "No new competitor news in the last 24 hours"
- **Persistence**: Saved articles remain visible across sessions and refreshes
- **Real-time Updates**: Dashboard shows latest data immediately after scraper completes

### UI/UX Requirements
- **Design**: Beautiful, modern, interactive interface (dark theme with purple accents)
- **Layout**: Card-based feed with sidebar navigation
- **Save Feature**: One-click save with visual feedback (bookmark icon)
- **Share Feature**: Generate shareable link for any article
- **Filtering**: Ability to filter by competitor, source, or date
- **Sort Options**: By date (newest first), source, or competitor
- **Responsive**: Mobile-friendly design

### Design System (Brand Guidelines)
**Colors:**
- Primary/Accent: `#966FE8` (Purple)
- Background: `#2A272F` (Dark Purple/Gray)
- Text Primary: `#FFFFFF` (White for dark theme)
- Text Secondary: `#9CA3AF` (Gray for metadata)
- Link: `#966FE8` (Purple)
- Card Background: `#363340` (Lighter than main background)

**Typography:**
- Font Family: Circular Std (fallback: -apple-system, system-ui)
- H1: 51.2px (3.2rem)
- H2: 47.2px (~3rem)
- Body: 18px (1.125rem)
- Small Text: 14px (0.875rem) for metadata

**Spacing:**
- Base Unit: 8px (use multiples: 8, 16, 24, 32, 40px)
- Container Padding: 32px
- Card Padding: 24px
- Gap Between Cards: 16px

**Components:**
- Border Radius (Cards): 12px (slight rounding for modern feel)
- Border Radius (Buttons): 8px
- Shadows: Subtle shadows for depth on cards
- Hover States: Purple glow/highlight on interactive elements

**Layout Pattern (Inspired by Design):**
- Left sidebar: Filters/categories (competitors, saved, all articles)
- Main content area: Card-based article feed
- Each card contains:
  - Article image (if available)
  - Title (H2 size, bold)
  - Source badge + competitor tags
  - Summary text (gray, smaller)
  - Metadata row (date, author)
  - Action icons (save, share) - subtle, purple on hover

**Personality:**
- Tone: Modern, professional
- Energy: Medium (not overly animated, but responsive)

### Constraints
- **No Duplicate Articles**: URL is unique key - same article not scraped twice
- **Respect Rate Limits**: API calls must respect source rate limits (see maintenance log)
- **Data Retention**: Keep articles for 30 days, then archive or delete
- **Error Handling**: Failed scrapes should not crash dashboard - show last successful data

### Do Not Rules
- **DO NOT** scrape more frequently than every 24 hours (respect source ToS)
- **DO NOT** display articles older than 24 hours in main feed
- **DO NOT** lose user's saved articles on refresh
- **DO NOT** expose API keys in frontend code

---

## 3. Architectural Invariants

### Integrations
1. **Supabase** (Backend/Database)
   - PostgreSQL database for articles
   - Real-time subscriptions for live updates
   - Authentication (future: multi-user support)

2. **News APIs** (Data Sources)
   - Primary: CryptoNews API (cryptonews-api.com)
   - Secondary: CoinDesk API
   - Fallback: Web scraping with Beautiful Soup/Playwright

3. **Competitors Monitored** (Fixed List)
   - Tangem
   - Trezor
   - Coinbase
   - Metamask
   - Revolut (crypto products)
   - Raby
   - Phantom

### Source of Truth
- **Primary Data**: News APIs (CryptoNews API, CoinDesk API)
- **Secondary Data**: Direct website scraping (as fallback)
- **Storage**: Supabase PostgreSQL database
- **Cache**: Articles stored in DB, not re-fetched

### Delivery Mechanism
- **Platform**: Web-based dashboard
- **Frontend**: Next.js + React (recommended for Supabase integration)
- **Styling**: Tailwind CSS for beautiful, responsive design
- **Hosting**: Vercel (Next.js) + Supabase
- **Automation**: Vercel Cron Jobs or GitHub Actions for 24h scraper

---

## 4. Maintenance Log

### Known Issues
None yet

### Error Patterns & Solutions
None yet

### API Rate Limits & Quirks

#### NewsData.io API ✅ WORKING
- **Rate Limit**: 60 requests/hour (200 requests/day on free tier)
- **Free Tier**: Yes - 200 requests/day
- **Response Format**: JSON
- **Authentication**: API key in URL parameter
- **Quirks**:
  - Returns max 10 results per request on free tier
  - Good for general crypto news, less specific competitor coverage
  - Best used with broad keywords like "cryptocurrency hardware wallet"

#### Trezor Blog RSS ✅ WORKING
- **Rate Limit**: None (RSS feed)
- **Free Tier**: Yes - completely free
- **Response Format**: RSS/XML
- **URL**: `https://blog.trezor.io/feed`
- **Quirks**:
  - ~10 recent articles available
  - Focuses on Trezor products but mentions competitors
  - Published dates in GMT

#### Other RSS Feeds (Currently Not Working)
- **Ledger Blog**: Feed URL invalid/not accessible
- **Tangem Blog**: Feed URL invalid/not accessible
- **Coinbase Blog**: Feed parsing errors
- **Consensys Blog**: Feed parsing errors
- **Note**: May need direct web scraping for these sources in Phase 3

**Updated**: 2026-02-06 - Phase 2 Testing Complete

---

## 5. Environment Variables

### Required Keys
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# CryptoNews API
CRYPTONEWS_API_KEY=your-api-key

# CoinDesk API (if needed)
COINDESK_API_KEY=your-api-key

# Scraper Configuration
SCRAPER_INTERVAL_HOURS=24
DATA_RETENTION_DAYS=30
```

### Optional Configuration
```bash
# Feature Flags
ENABLE_SENTIMENT_ANALYSIS=false
ENABLE_EMAIL_NOTIFICATIONS=false

# Development
NODE_ENV=development
```
