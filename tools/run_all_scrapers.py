#!/usr/bin/env python3
"""
Master Scraper Orchestrator
Runs all scrapers sequentially and provides a summary report.
"""

import subprocess
import sys
from datetime import datetime, timezone

def run_scraper(script_name: str, description: str) -> dict:
    """Run a scraper script and return its result.

    Args:
        script_name: Path to the scraper script
        description: Human-readable description

    Returns:
        dict: Result with success status and output
    """
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*70}")

    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per scraper
        )

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        success = result.returncode == 0

        if success:
            print(f"\n✅ {description} completed successfully")
        else:
            print(f"\n❌ {description} failed (exit code: {result.returncode})")

        return {
            "name": description,
            "success": success,
            "output": result.stdout + result.stderr
        }

    except subprocess.TimeoutExpired:
        print(f"\n❌ {description} timed out")
        return {
            "name": description,
            "success": False,
            "output": "Timeout after 5 minutes"
        }
    except Exception as e:
        print(f"\n❌ Error running {description}: {e}")
        return {
            "name": description,
            "success": False,
            "output": str(e)
        }

def main():
    """Run all scrapers and provide summary."""

    print("\n" + "="*70)
    print("🚀 MASTER SCRAPER ORCHESTRATOR")
    print("="*70)
    print(f"\nStarted at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("\nRunning all scrapers to collect competitor intelligence...\n")

    # Define scrapers to run
    scrapers = [
        ('tools/scrape_newsdata.py', 'NewsData.io API Scraper'),
        ('tools/scrape_rss.py', 'RSS Feed Scraper'),
        # Add more scrapers here as they're built
    ]

    results = []

    # Run each scraper sequentially
    for script, description in scrapers:
        result = run_scraper(script, description)
        results.append(result)

        # Small delay between scrapers to avoid rate limiting
        import time
        time.sleep(2)

    # Generate Summary Report
    print("\n\n" + "="*70)
    print("📊 FINAL SUMMARY REPORT")
    print("="*70 + "\n")

    passed = sum(1 for r in results if r['success'])
    total = len(results)

    print(f"Completed at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Scrapers Run: {total}")
    print(f"Successful: {passed}")
    print(f"Failed: {total - passed}\n")

    print("Individual Results:")
    print("-" * 70)

    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"   {status} - {result['name']}")

    print("\n" + "="*70)

    # Overall status
    if passed == total:
        print("✅ ALL SCRAPERS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n🎉 Data collection complete!")
        print("   Check your Supabase database for new articles")
        print("   Dashboard will now show the latest competitor intelligence\n")
        return 0
    elif passed > 0:
        print("⚠️  PARTIAL SUCCESS")
        print("="*70)
        print(f"\n{passed}/{total} scrapers completed successfully")
        print(f"{total - passed} scraper(s) failed - check logs above")
        print("\n💡 Partial data has been collected")
        print("   Review failed scrapers and try running them individually\n")
        return 1
    else:
        print("❌ ALL SCRAPERS FAILED")
        print("="*70)
        print("\n⚠️  No data was collected")
        print("\n💡 Troubleshooting:")
        print("   1. Check your .env file has all API keys")
        print("   2. Verify Supabase credentials are correct")
        print("   3. Check network connectivity")
        print("   4. Run individual scrapers to see detailed errors\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
