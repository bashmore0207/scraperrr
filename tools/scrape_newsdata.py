#!/usr/bin/env python3
"""
NewsData.io Scraper
Fetches competitor news from NewsData.io API and stores in Supabase.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
from dateutil import parser

# Load environment
load_dotenv()

# Constants
SOURCE_NAME = "NewsData.io"
LOOKBACK_HOURS = 24  # Fetch articles from last 24 hours
COMPETITORS = [
    "ledger", "trezor", "tangem", "coinbase",
    "metamask", "revolut", "raby", "phantom"
]
API_URL = "https://newsdata.io/api/1/news"

def init_supabase() -> Client:
    """Initialize Supabase client."""
    url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not url or not key:
        raise ValueError("Missing Supabase credentials in .env file")

    return create_client(url, key)

def fetch_articles():
    """Fetch articles from NewsData.io API.

    Returns:
        list: List of raw articles from the source
    """
    api_key = os.getenv('NEWSDATA_API_KEY')

    if not api_key:
        raise ValueError("Missing NEWSDATA_API_KEY in .env file")

    # Calculate time window
    from_time = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)

    params = {
        'apikey': api_key,
        'q': 'cryptocurrency wallet OR crypto wallet OR hardware wallet',
        'language': 'en',
        'category': 'technology,business'
    }

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data.get('status') == 'success':
            articles = data.get('results', [])

            # Filter for recent articles (API doesn't support 'from' param on free tier)
            recent = []
            for article in articles:
                published = parse_timestamp(article.get('pubDate'))
                published_dt = parser.parse(published)

                if published_dt >= from_time:
                    recent.append(article)

            return recent
        else:
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")

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

def detect_competitors(article_data) -> list:
    """Detect which competitors are mentioned in the article.

    Args:
        article_data: Raw article data

    Returns:
        list: List of competitor names found (capitalized)
    """
    # Combine all text fields
    title = article_data.get('title', '').lower()
    description = article_data.get('description', '').lower() if article_data.get('description') else ''
    content = article_data.get('content', '').lower() if article_data.get('content') else ''

    text = f"{title} {description} {content}"

    found = []
    for competitor in COMPETITORS:
        if competitor in text:
            # Capitalize first letter
            found.append(competitor.capitalize())

    return found

def normalize_article(raw_article) -> dict:
    """Transform NewsData.io format to our standard schema.

    Args:
        raw_article: Raw article data from NewsData.io

    Returns:
        dict: Normalized article matching Supabase schema
    """
    return {
        "title": raw_article.get("title"),
        "url": raw_article.get("link"),
        "source": raw_article.get("source_id", SOURCE_NAME),
        "competitors": detect_competitors(raw_article),
        "published_at": parse_timestamp(raw_article.get("pubDate")),
        "summary": raw_article.get("description"),
        "author": raw_article.get("creator", [None])[0] if raw_article.get("creator") else None,
        "image_url": raw_article.get("image_url")
    }

def article_exists(supabase: Client, url: str) -> bool:
    """Check if article already exists in database.

    Args:
        supabase: Supabase client
        url: Article URL to check

    Returns:
        bool: True if article exists
    """
    try:
        result = supabase.table('articles').select('id').eq('url', url).execute()
        return len(result.data) > 0
    except:
        return False

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
                print(f"   ⏭  Skipped duplicate: {article['title'][:50]}...")
                continue

            # Insert new article
            supabase.table('articles').insert(article).execute()
            stats['inserted'] += 1
            print(f"   ✅ Stored: {article['title'][:50]}... (Competitors: {', '.join(article['competitors'])})")

        except Exception as e:
            print(f"   ❌ Error storing article: {e}")
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
    try:
        supabase.table('scraper_runs').insert({
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "articles_found": stats.get('inserted', 0) + stats.get('skipped', 0),
            "articles_added": stats.get('inserted', 0),
            "status": "completed" if success else "failed",
            "error_message": error
        }).execute()
    except Exception as e:
        print(f"   ⚠️  Failed to log scraper run: {e}")

def main():
    """Main scraper execution."""

    print(f"\n{'='*60}")
    print(f"🚀 {SOURCE_NAME} Scraper Started")
    print(f"   Time Window: Last {LOOKBACK_HOURS} hours")
    print(f"{'='*60}\n")

    try:
        # Initialize
        print(f"🔌 Connecting to Supabase...")
        supabase = init_supabase()
        print(f"✅ Connected to Supabase\n")

        # Fetch articles
        print(f"📡 Fetching articles from {SOURCE_NAME}...")
        raw_articles = fetch_articles()
        print(f"✅ Found {len(raw_articles)} recent articles\n")

        # Normalize articles
        print(f"🔄 Normalizing articles...")
        normalized = [normalize_article(a) for a in raw_articles]
        print(f"✅ Normalized {len(normalized)} articles\n")

        # Filter for competitor mentions
        print(f"🎯 Filtering for competitor mentions...")
        relevant = [a for a in normalized if a['competitors']]
        print(f"✅ Found {len(relevant)} articles mentioning competitors\n")

        if not relevant:
            print(f"ℹ️  No competitor mentions found in this batch")
            log_scraper_run(supabase, {"inserted": 0, "skipped": 0, "errors": 0}, success=True)
            return

        # Store articles
        print(f"💾 Storing articles in database...\n")
        stats = store_articles(supabase, relevant)

        # Log results
        print(f"\n📝 Logging scraper run...")
        log_scraper_run(supabase, stats, success=True)

        # Summary
        print(f"\n{'='*60}")
        print(f"✅ {SOURCE_NAME} Scraper Complete")
        print(f"{'='*60}")
        print(f"   Articles Fetched: {len(raw_articles)}")
        print(f"   Competitor Mentions: {len(relevant)}")
        print(f"   New Articles Stored: {stats['inserted']}")
        print(f"   Duplicates Skipped: {stats['skipped']}")
        print(f"   Errors: {stats['errors']}")
        print(f"\n")

    except Exception as e:
        print(f"\n❌ Scraper failed: {e}")
        print(f"   Error type: {type(e).__name__}\n")

        # Log failure
        try:
            supabase = init_supabase()
            log_scraper_run(supabase, {}, success=False, error=str(e))
        except:
            pass

        sys.exit(1)

if __name__ == "__main__":
    main()
