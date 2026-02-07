# Findings

## Project Overview
**Crypto Competitor Intelligence Dashboard**
- Monitor 7 competitors: Tangem, Trezor, Coinbase, Metamask, Revolut (crypto), Raby, Phantom
- Collect articles/news from last 24 hours only
- Beautiful, interactive web dashboard
- Save/share functionality with persistence

## Discovery Answers

### 1. North Star
Build an interactive dashboard showing latest competitor intelligence for Ledger alternatives

### 2. Integrations
- **Supabase**: Backend database and authentication
- **Web Scrapers**: Multiple sources (start simple, scale complexity)
- **Potential Data Sources** (to research):
  - CoinDesk, CoinTelegraph, The Block, Decrypt
  - Company blogs/press releases
  - Reddit (crypto subreddits)
  - Twitter/X (company accounts)
  - Google News API
  - NewsAPI.org

### 3. Source of Truth
- Web sources (news sites, blogs, social media)
- Data stored in Supabase database

### 4. Delivery Payload
- Web-based dashboard
- Saved articles persist across sessions
- Share functionality

### 5. Behavioral Rules
- **Frequency**: Run scrapers every 24 hours
- **Time Window**: Only show data from last 24 hours
- **UX**: Highlight when no new information available
- **Features**: Save articles, share articles, beautiful/interactive design
- **Persistence**: Saved articles visible after refresh

## Technical Constraints
- Need to respect rate limits on scraping
- Need to handle different website structures
- Consider using headless browser for dynamic content
- Need Supabase account and API keys

## Research Completed

### Best Crypto News APIs (2026)
1. **CryptoNews API** (cryptonews-api.com) - Indexes CoinTelegraph, Coindesk, NewsBTC, Decrypt, CoinMarketCap
2. **CoinDesk API** - Official API with news, prices, social insights
3. **NewsData.io** - Real-time crypto news API
4. **Financial Modeling Prep** - Crypto news with headlines and snippets
5. **Cylynx Crypto News API** - Includes sentiment analysis

### News Sources Identified
- CoinDesk, CoinTelegraph, NewsBTC, Decrypt
- Coin Bureau, CryptoVantage, Cointribune
- Money.com, HardwareWalletOnline, Webopedia
- Company blogs: Tangem Blog, Trezor Blog

### Recent Competitor Activity (Jan 2026)
- **Tangem**: Launching Tangem Pay (VISA partnership), 2M+ cards, never hacked
- **Trezor**: Launched Safe 7 with quantum-ready security
- Both featured in "Best Wallets 2026" roundups

## Design Direction

### Brand Guidelines Applied
- **Color Palette**: Dark theme with purple (#966FE8) accents on dark background (#2A272F)
- **Typography**: Circular Std font family, modern sizing (H1: 51.2px, Body: 18px)
- **Spacing**: 8px base unit system
- **Personality**: Modern, medium energy

### Dashboard Layout (Inspired by design/dashboard design inspiration.png)
- **Structure**: Left sidebar navigation + card-based main content area
- **Cards**: Article cards with image previews, metadata, action icons
- **Dark Theme**: Professional dark mode with purple highlights
- **Icons**: Subtle icons for save/share actions
- **Preview Images**: Feature images displayed in cards when available

### Key Visual Elements
- Card-based layout for articles
- Sidebar with competitor filters
- Purple accent color for interactive elements
- Clean typography hierarchy
- Subtle shadows for depth
- Bookmark/save icons with purple hover states

## Phase 2: Data Sources Connected

### Working Data Sources (Verified 2026-02-06)

1. **Supabase Database** ✅
   - All 3 tables created and tested
   - CRUD operations verified
   - Row Level Security configured
   - Rate Limit: None (database)

2. **NewsData.io API** ✅
   - API Key: Configured
   - Rate Limit: 60 req/hour (200/day free tier)
   - Coverage: General crypto news
   - Test Results: 7 articles fetched successfully

3. **Trezor Blog RSS** ✅
   - URL: https://blog.trezor.io/feed
   - Rate Limit: None (RSS feed)
   - Coverage: Trezor-focused with competitor mentions
   - Test Results: 10 articles available

### Data Sources Attempted (Not Working)
- Ledger Blog RSS: Feed parsing errors
- Tangem Blog RSS: Feed parsing errors
- Coinbase Blog RSS: Feed parsing errors
- Consensys Blog RSS: Feed parsing errors

**Note**: Will implement direct web scraping for failed RSS feeds in Phase 3

### Data Source Strategy
- **Primary**: NewsData.io for broad crypto news coverage
- **Secondary**: Trezor RSS for competitor-specific content
- **Future**: Add web scraping for Ledger/Tangem/Coinbase blogs
- **Future**: Consider adding Reddit API (free) for community discussions

## Research Todo
- [x] Determine scraping approach (APIs preferred, fallback to Beautiful Soup/Playwright)
- [x] Research Supabase schema design best practices
- [x] Frontend framework decision (Next.js recommended for Supabase integration)
- [x] Review design inspiration and brand guidelines
- [x] Test and verify data source connections (Phase 2)

---

**Last Updated:** 2026-02-06
