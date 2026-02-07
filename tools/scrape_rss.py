#!/usr/bin/env python3
"""
RSS Feed Scraper
Fetches competitor news from company blog RSS feeds and stores in Supabase.
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
import feedparser
from dateutil import parser

# Load environment
load_dotenv()

# Constants
SOURCE_NAME = "RSS Feeds"
LOOKBACK_HOURS = 24  # Fetch articles from last 24 hours
COMPETITORS = [
    "ledger", "trezor", "tangem", "coinbase",
    "metamask", "revolut", "raby", "phantom"
]

# RSS feed URLs to scrape
RSS_FEEDS = {
    "Trezor Blog": "https://blog.trezor.io/feed",
    # Add more working RSS feeds here as discovered
}

def init_supabase() -> Client:
    """Initialize Supabase client."""
    url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not url or not key:
        raise ValueError("Missing Supabase credentials in .env file")

    return create_client(url, key)

def fetch_articles_from_feed(feed_url: str, feed_name: str, cutoff: datetime):
    """Fetch articles from a single RSS feed.

    Args:
        feed_url: URL of the RSS feed
        feed_name: Name of the feed source
        cutoff: Datetime cutoff for filtering old articles

    Returns:
        list: List of raw articles from the feed
    """
    try:
        print(f"   📡 Fetching {feed_name}...")
        parsed = feedparser.parse(feed_url)

        if parsed.get('bozo', 1) == 1 and not parsed.entries:
            print(f"   ⚠️  Feed parsing failed: {parsed.get('bozo_exception', 'Unknown error')}")
            return []

        # Filter for recent articles
        recent = []
        for entry in parsed.entries:
            published = parse_timestamp(entry.get('published', entry.get('updated')))
            published_dt = parser.parse(published)

            if published_dt >= cutoff:
                # Add feed name to entry
                entry['_feed_name'] = feed_name
                recent.append(entry)

        print(f"   ✅ Found {len(recent)} recent articles from {feed_name}")
        return recent

    except Exception as e:
        print(f"   ❌ Error fetching {feed_name}: {e}")
        return []

def fetch_articles():
    """Fetch articles from all RSS feeds.

    Returns:
        list: List of raw articles from all sources
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)

    all_articles = []
    for feed_name, feed_url in RSS_FEEDS.items():
        articles = fetch_articles_from_feed(feed_url, feed_name, cutoff)
        all_articles.extend(articles)

    return all_articles

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
    summary = article_data.get('summary', '').lower()
    content = article_data.get('content', [{}])[0].get('value', '').lower() if article_data.get('content') else ''

    text = f"{title} {summary} {content}"

    found = []
    for competitor in COMPETITORS:
        if competitor in text:
            # Capitalize first letter
            found.append(competitor.capitalize())

    return found

def normalize_article(raw_article) -> dict:
    """Transform RSS feed format to our standard schema.

    Args:
        raw_article: Raw article data from RSS feed

    Returns:
        dict: Normalized article matching Supabase schema
    """
    # Extract content
    content = ""
    if raw_article.get('content'):
        content = raw_article['content'][0].get('value', '')
    elif raw_article.get('summary'):
        content = raw_article['summary']

    # Extract image
    image_url = None
    if raw_article.get('media_content'):
        image_url = raw_article['media_content'][0].get('url')
    elif raw_article.get('enclosures') and len(raw_article['enclosures']) > 0:
        image_url = raw_article['enclosures'][0].get('href')

    return {
        "title": raw_article.get("title"),
        "url": raw_article.get("link"),
        "source": raw_article.get("_feed_name", SOURCE_NAME),
        "competitors": detect_competitors(raw_article),
        "published_at": parse_timestamp(raw_article.get("published", raw_article.get("updated"))),
        "summary": raw_article.get("summary", content[:300] if content else None),
        "author": raw_article.get("author"),
        "image_url": image_url
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
    print(f"🚀 RSS Feed Scraper Started")
    print(f"   Time Window: Last {LOOKBACK_HOURS} hours")
    print(f"   Sources: {len(RSS_FEEDS)} RSS feeds")
    print(f"{'='*60}\n")

    try:
        # Initialize
        print(f"🔌 Connecting to Supabase...")
        supabase = init_supabase()
        print(f"✅ Connected to Supabase\n")

        # Fetch articles
        print(f"📡 Fetching articles from RSS feeds...\n")
        raw_articles = fetch_articles()
        print(f"\n✅ Found {len(raw_articles)} total recent articles\n")

        if not raw_articles:
            print(f"ℹ️  No recent articles found in RSS feeds")
            log_scraper_run(supabase, {"inserted": 0, "skipped": 0, "errors": 0}, success=True)
            return

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
        print(f"✅ RSS Feed Scraper Complete")
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
