#!/usr/bin/env python3
"""
RSS Feed Test Script
Tests RSS feeds from company blogs for competitor news.
"""

import sys
import feedparser
from datetime import datetime, timezone
import requests

def test_rss_feeds():
    """Test RSS feeds from crypto wallet company blogs."""

    print("\n" + "="*60)
    print("🧪 Testing Company Blog RSS Feeds")
    print("="*60 + "\n")

    # RSS feed URLs to test
    feeds = {
        "Trezor Blog": "https://blog.trezor.io/feed",
        "Ledger Blog": "https://www.ledger.com/blog/feed",
        "Tangem Blog": "https://tangem.com/en/blog/rss.xml",
        "Coinbase Blog": "https://blog.coinbase.com/feed",
        "Consensys Blog (Metamask)": "https://consensys.io/blog/feed"
    }

    working_feeds = []
    failed_feeds = []

    for company, feed_url in feeds.items():
        print(f"📡 Testing: {company}")
        print(f"   URL: {feed_url}")

        try:
            # Try to fetch the feed
            parsed = feedparser.parse(feed_url)

            # Check if feed was successfully parsed
            if parsed.get('bozo', 1) == 0 or parsed.entries:
                # Feed is valid
                num_entries = len(parsed.entries)

                if num_entries > 0:
                    print(f"✅ Feed working - {num_entries} entries found")

                    # Show latest entry
                    latest = parsed.entries[0]
                    print(f"   Latest: {latest.get('title', 'No title')[:60]}...")

                    published = latest.get('published', latest.get('updated', 'Unknown'))
                    print(f"   Published: {published}")

                    working_feeds.append({
                        'company': company,
                        'url': feed_url,
                        'entries': num_entries
                    })
                else:
                    print(f"⚠️  Feed accessible but empty")
                    failed_feeds.append({'company': company, 'error': 'Empty feed'})
            else:
                # Feed parse error
                error = parsed.get('bozo_exception', 'Parse error')
                print(f"❌ Feed parsing failed: {error}")
                failed_feeds.append({'company': company, 'error': str(error)})

        except Exception as e:
            print(f"❌ Error accessing feed: {e}")
            failed_feeds.append({'company': company, 'error': str(e)})

        print()

    # Summary
    print("=" * 60)
    print("📊 RSS Feed Test Summary")
    print("=" * 60 + "\n")

    if working_feeds:
        print(f"✅ Working Feeds ({len(working_feeds)}):")
        for feed in working_feeds:
            print(f"   - {feed['company']}: {feed['entries']} articles")
        print()

    if failed_feeds:
        print(f"❌ Failed Feeds ({len(failed_feeds)}):")
        for feed in failed_feeds:
            print(f"   - {feed['company']}: {feed['error']}")
        print()

    # Test competitor detection
    if working_feeds:
        print("🔍 Testing Competitor Mention Detection...")
        print("   Checking latest articles for competitor keywords...\n")

        competitors = ['trezor', 'ledger', 'tangem', 'coinbase', 'metamask', 'revolut', 'phantom']
        mentions_found = 0

        for feed in working_feeds[:3]:  # Check first 3 working feeds
            parsed = feedparser.parse(feed['url'])

            for entry in parsed.entries[:5]:  # Check 5 latest articles
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                content = f"{title} {summary}"

                for competitor in competitors:
                    if competitor in content:
                        mentions_found += 1
                        print(f"   ✓ Found '{competitor}' in {feed['company']}")
                        break

        print(f"\n   Total competitor mentions: {mentions_found}")

    # Final result
    print("\n" + "=" * 60)

    if len(working_feeds) >= 2:
        print("✅ RSS Feed Test Successful!")
        print(f"   {len(working_feeds)}/{len(feeds)} feeds working")
        print("   RSS feeds ready for production use")
    elif len(working_feeds) >= 1:
        print("⚠️  Partial Success")
        print(f"   {len(working_feeds)}/{len(feeds)} feeds working")
        print("   At least one feed available for use")
    else:
        print("❌ All RSS feeds failed")
        print("   Check feed URLs or try again later")
        sys.exit(1)

    print("=" * 60 + "\n")

    # Output working feed URLs for reference
    if working_feeds:
        print("📋 Working Feed URLs (for gemini.md):")
        for feed in working_feeds:
            print(f"   {feed['company']}: {feed['url']}")
        print()

if __name__ == "__main__":
    test_rss_feeds()
