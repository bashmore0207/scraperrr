# Scraper Architecture SOP

## Purpose
Defines the standard operating procedure for all data scrapers in the Crypto Competitor Intelligence Dashboard.

## Core Principles

1. **Source Isolation**: Each scraper handles ONE data source
2. **Idempotent Operations**: Re-running a scraper doesn't create duplicates
3. **Graceful Degradation**: Failed sources don't crash the entire system
4. **Structured Logging**: All actions logged with timestamps and status
5. **Rate Limit Respect**: Honor API limits, implement backoff strategies

## Standard Scraper Structure

Every scraper must follow this template:

```python
#!/usr/bin/env python3
"""
[Source Name] Scraper
Fetches competitor news from [Source Name] and stores in Supabase.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment
load_dotenv()

# Constants
SOURCE_NAME = "[Source Name]"
LOOKBACK_HOURS = 24  # Fetch articles from last 24 hours
COMPETITORS = [
    "ledger", "trezor", "tangem", "coinbase",
    "metamask", "revolut", "raby", "phantom"
]

def init_supabase() -> Client:
    """Initialize Supabase client."""
    url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not url or not key:
        raise ValueError("Missing Supabase credentials")

    return create_client(url, key)

def fetch_articles():
    """Fetch articles from the data source.

    Returns:
        list: List of raw articles from the source
    """
    # Source-specific fetching logic
    pass

def normalize_article(raw_article) -> dict:
    """Transform source-specific format to our standard schema.

    Args:
        raw_article: Raw article data from source

    Returns:
        dict: Normalized article matching Supabase schema
    """
    return {
        "title": raw_article.get("title"),
        "url": raw_article.get("link"),
        "source": SOURCE_NAME,
        "competitors": detect_competitors(raw_article),
        "published_at": parse_timestamp(raw_article.get("published")),
        "summary": raw_article.get("description"),
        "author": raw_article.get("author"),
        "image_url": raw_article.get("image"),
        "sentiment": None  # Optional: add sentiment analysis
    }

def detect_competitors(article_data) -> list:
    """Detect which competitors are mentioned in the article.

    Args:
        article_data: Raw article data

    Returns:
        list: List of competitor names found (lowercase)
    """
    text = f"{article_data.get('title', '')} {article_data.get('description', '')}".lower()

    found = []
    for competitor in COMPETITORS:
        if competitor in text:
            found.append(competitor.capitalize())

    return found if found else []

def article_exists(supabase: Client, url: str) -> bool:
    """Check if article already exists in database.

    Args:
        supabase: Supabase client
        url: Article URL to check

    Returns:
        bool: True if article exists
    """
    result = supabase.table('articles').select('id').eq('url', url).execute()
    return len(result.data) > 0

def store_articles(supabase: Client, articles: list) -> dict:
    """Store articles in Supabase, skipping duplicates.

    Args:
        supabase: Supabase client
        articles: List of normalized articles

    Returns:
        dict: Statistics (inserted, skipped, errors)
    """
    stats = {"inserted": 0, "skipped": 0, "errors": 0}

    for article in articles:
        try:
            # Skip if already exists
            if article_exists(supabase, article['url']):
                stats['skipped'] += 1
                continue

            # Insert new article
            supabase.table('articles').insert(article).execute()
            stats['inserted'] += 1

        except Exception as e:
            print(f"Error storing article: {e}")
            stats['errors'] += 1

    return stats

def log_scraper_run(supabase: Client, stats: dict, success: bool, error: str = None):
    """Log scraper execution to scraper_runs table.

    Args:
        supabase: Supabase client
        stats: Run statistics
        success: Whether scraper completed successfully
        error: Error message if failed
    """
    supabase.table('scraper_runs').insert({
        "scraper_name": SOURCE_NAME,
        "run_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "articles_found": stats.get('inserted', 0) + stats.get('skipped', 0),
        "articles_stored": stats.get('inserted', 0),
        "error_message": error
    }).execute()

def main():
    """Main scraper execution."""

    print(f"\n{'='*60}")
    print(f"🚀 {SOURCE_NAME} Scraper Started")
    print(f"{'='*60}\n")

    try:
        # Initialize
        supabase = init_supabase()
        print(f"✅ Connected to Supabase")

        # Fetch articles
        print(f"📡 Fetching articles from {SOURCE_NAME}...")
        raw_articles = fetch_articles()
        print(f"✅ Found {len(raw_articles)} articles")

        # Normalize articles
        print(f"🔄 Normalizing articles...")
        normalized = [normalize_article(a) for a in raw_articles]

        # Filter for competitor mentions
        relevant = [a for a in normalized if a['competitors']]
        print(f"🎯 {len(relevant)} articles mention competitors")

        # Store articles
        print(f"💾 Storing articles in database...")
        stats = store_articles(supabase, relevant)

        # Log results
        log_scraper_run(supabase, stats, success=True)

        # Summary
        print(f"\n{'='*60}")
        print(f"✅ {SOURCE_NAME} Scraper Complete")
        print(f"{'='*60}")
        print(f"   Articles Found: {len(raw_articles)}")
        print(f"   Competitor Mentions: {len(relevant)}")
        print(f"   New Articles: {stats['inserted']}")
        print(f"   Duplicates Skipped: {stats['skipped']}")
        print(f"   Errors: {stats['errors']}")
        print(f"\n")

    except Exception as e:
        print(f"\n❌ Scraper failed: {e}")

        # Log failure
        try:
            supabase = init_supabase()
            log_scraper_run(supabase, {}, success=False, error=str(e))
        except:
            pass

        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Data Source Patterns

### 1. REST API Pattern (NewsData.io, CryptoNews, etc.)
```python
def fetch_articles():
    api_key = os.getenv('NEWSDATA_API_KEY')

    params = {
        'apikey': api_key,
        'q': 'cryptocurrency hardware wallet OR crypto wallet',
        'language': 'en',
        'from': (datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)).isoformat()
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get('results', [])
```

### 2. RSS Feed Pattern (Trezor Blog, etc.)
```python
def fetch_articles():
    import feedparser

    feed = feedparser.parse(RSS_URL)

    # Filter for recent articles
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)

    recent = []
    for entry in feed.entries:
        published = parse_timestamp(entry.get('published'))
        if published >= cutoff:
            recent.append(entry)

    return recent
```

### 3. Web Scraping Pattern (for sites without APIs)
```python
def fetch_articles():
    from bs4 import BeautifulSoup

    response = requests.get(BLOG_URL, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.select('.article-card'):  # Adjust selector
        articles.append({
            'title': article.select_one('.title').text,
            'url': article.select_one('a')['href'],
            'published': article.select_one('.date').text,
            'description': article.select_one('.summary').text
        })

    return articles
```

## Error Handling Rules

1. **API Rate Limits**: Catch 429 errors, log, and exit gracefully
2. **Network Timeouts**: Set 30-second timeout on all requests
3. **Malformed Data**: Skip individual articles, don't crash entire run
4. **Missing Credentials**: Fail fast with clear error message

## Deduplication Strategy

Articles are deduplicated by URL:
1. Before inserting, check if `url` exists in `articles` table
2. If exists, skip insertion (log as "duplicate")
3. If URL is modified (tracking params), normalize before checking

## Timestamp Handling

All timestamps must be:
- Converted to UTC timezone
- Stored in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS+00:00`
- Parsed using `python-dateutil` for flexibility

```python
from dateutil import parser

def parse_timestamp(timestamp_str):
    """Parse various timestamp formats to UTC ISO string."""
    if not timestamp_str:
        return datetime.now(timezone.utc).isoformat()

    try:
        dt = parser.parse(timestamp_str)
        # Convert to UTC if timezone-aware
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except:
        return datetime.now(timezone.utc).isoformat()
```

## Competitor Detection

**Case-insensitive matching** across:
- Article title
- Article description/summary
- Article content (if available)

**Exact matches** for:
- ledger, trezor, tangem, coinbase, metamask, revolut, raby, phantom

**Store as capitalized**: Ledger, Trezor, etc.

## Scraper Orchestration

The master script `run_all_scrapers.py` will:
1. Run each scraper sequentially (avoid parallel API hammering)
2. Continue if one fails (don't block others)
3. Aggregate statistics across all scrapers
4. Send summary notification (optional)

## Performance Guidelines

- **Batch operations**: Insert articles in batches of 50 if > 100 articles
- **Connection pooling**: Reuse Supabase client throughout run
- **Lazy loading**: Only fetch full content if needed for competitor detection

## Testing Requirements

Every scraper must have a corresponding test script:
- `scrape_newsdata.py` → `test_newsdata_scraper.py`
- Test with small dataset (last 1 hour, not 24 hours)
- Verify deduplication works (run twice, check stats)
- Test error handling (invalid API key, network timeout)

## Deployment Checklist

Before deploying a scraper:
- [ ] Follows standard structure
- [ ] Handles all error cases
- [ ] Respects rate limits
- [ ] Logs to scraper_runs table
- [ ] Has test script
- [ ] Documented in gemini.md Section 3 (Integrations)
