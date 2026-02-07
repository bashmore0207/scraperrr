#!/usr/bin/env python3
"""
NewsData.io API Test Script
Tests NewsData.io crypto news API for competitor mentions.
"""

import os
import sys
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

def test_newsdata_api():
    """Test NewsData.io API connection and fetch crypto news."""

    print("\n" + "="*60)
    print("🧪 Testing NewsData.io API")
    print("="*60 + "\n")

    # Get API key from environment
    api_key = os.getenv('NEWSDATA_API_KEY')

    if not api_key:
        print("❌ Error: NEWSDATA_API_KEY not found in .env file")
        sys.exit(1)

    print(f"🔑 API Key found: {api_key[:20]}...")

    # Competitors to search for
    competitors = [
        "Ledger", "Trezor", "Tangem", "Coinbase",
        "Metamask", "Revolut crypto", "Phantom wallet"
    ]

    base_url = "https://newsdata.io/api/1/news"

    try:
        # Test 1: Search for cryptocurrency + hardware wallet news
        print("\n📰 Test 1: Fetching cryptocurrency hardware wallet news...")

        params = {
            'apikey': api_key,
            'q': 'cryptocurrency hardware wallet OR crypto wallet',
            'language': 'en',
            'category': 'technology,business'
        }

        response = requests.get(base_url, params=params, timeout=30)

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            if data.get('status') == 'success':
                results = data.get('results', [])
                total_results = data.get('totalResults', 0)

                print(f"✅ API call successful")
                print(f"   Total Results Available: {total_results}")
                print(f"   Articles Returned: {len(results)}\n")

                # Test 2: Filter for competitor mentions
                print("🔍 Test 2: Checking for competitor mentions...")

                competitor_mentions = {}
                for competitor in competitors:
                    competitor_mentions[competitor] = 0

                for article in results[:10]:  # Check first 10 articles
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower() if article.get('description') else ''
                    content = article.get('content', '').lower() if article.get('content') else ''

                    full_text = f"{title} {description} {content}"

                    for competitor in competitors:
                        if competitor.lower() in full_text:
                            competitor_mentions[competitor] += 1

                print("   Competitor Mentions:")
                for comp, count in competitor_mentions.items():
                    if count > 0:
                        print(f"   ✓ {comp}: {count} mention(s)")

                total_mentions = sum(competitor_mentions.values())
                if total_mentions > 0:
                    print(f"\n✅ Found {total_mentions} total competitor mentions")
                else:
                    print(f"\n⚠️  No competitor mentions in current results")
                    print("   (This is normal - try different search terms or wait for new news)")

                # Test 3: Display sample article
                if results:
                    print("\n📄 Sample Article:")
                    sample = results[0]
                    print(f"   Title: {sample.get('title', 'N/A')[:80]}...")
                    print(f"   Source: {sample.get('source_id', 'N/A')}")
                    print(f"   Published: {sample.get('pubDate', 'N/A')}")
                    print(f"   URL: {sample.get('link', 'N/A')[:60]}...")

                # Test 4: Check rate limits
                print("\n📊 API Info:")
                remaining = response.headers.get('X-RateLimit-Remaining', 'Unknown')
                limit = response.headers.get('X-RateLimit-Limit', 'Unknown')
                print(f"   Rate Limit: {remaining}/{limit} requests remaining")
                print(f"   Free Tier: 200 requests/day")

                print("\n" + "="*60)
                print("✅ NewsData.io API Test Successful!")
                print("="*60)
                print("\n📝 Summary:")
                print(f"   - API Key: Valid")
                print(f"   - Connection: Working")
                print(f"   - Results: {len(results)} articles fetched")
                print(f"   - Competitor Mentions: {total_mentions}")
                print(f"   - Rate Limit: {remaining}/{limit}")
                print("\n")

            else:
                print(f"❌ API returned error status: {data.get('status')}")
                print(f"   Message: {data.get('message', 'No message')}")
                sys.exit(1)

        elif response.status_code == 401:
            print("❌ Authentication failed - check API key")
            sys.exit(1)
        elif response.status_code == 429:
            print("❌ Rate limit exceeded - try again later")
            sys.exit(1)
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Type: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    test_newsdata_api()
