#!/usr/bin/env python3
"""
Master Connection Test Script
Runs all connection tests and provides a summary report.
"""

import subprocess
import sys

def run_test(script_name, description):
    """Run a test script and return its result."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*70}")

    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=False,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"\n❌ {script_name} timed out")
        return False
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")
        return False

def main():
    """Run all connection tests."""

    print("\n" + "="*70)
    print("🚀 MASTER CONNECTION TEST - Phase 2 Verification")
    print("="*70)
    print("\nTesting all data sources for the Crypto Competitor Dashboard\n")

    tests = [
        ('tools/test_supabase.py', 'Supabase Database'),
        ('tools/test_newsdata_api.py', 'NewsData.io News API'),
        ('tools/test_rss_feeds.py', 'Company Blog RSS Feeds'),
    ]

    results = {}

    for script, description in tests:
        success = run_test(script, description)
        results[description] = success

    # Summary Report
    print("\n\n" + "="*70)
    print("📊 FINAL TEST SUMMARY")
    print("="*70 + "\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"Tests Passed: {passed}/{total}\n")

    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test}")

    print("\n" + "="*70)

    # Data Sources Summary
    if passed >= 2:  # Minimum 2 sources needed
        print("✅ PHASE 2 SUCCESS!")
        print("="*70)
        print("\n🎉 Connectivity Verified!")
        print(f"   {passed} data sources ready for production")
        print("\n📝 Working Data Sources:")
        if results.get('Supabase Database'):
            print("   ✓ Supabase - Database (articles, saved_articles, scraper_runs)")
        if results.get('NewsData.io News API'):
            print("   ✓ NewsData.io - Crypto news API (60 requests/hour)")
        if results.get('Company Blog RSS Feeds'):
            print("   ✓ RSS Feeds - Trezor blog (and potentially others)")

        print("\n🚀 Ready to proceed to Phase 3: Architect")
        print("   - Build scrapers using verified connections")
        print("   - Create Next.js dashboard")
        print("   - Implement save/share features")

        print("\n" + "="*70 + "\n")
        return 0
    else:
        print("❌ PHASE 2 INCOMPLETE")
        print("="*70)
        print(f"\n⚠️  Only {passed} source(s) working")
        print("   Minimum 2 required to proceed")
        print("\n💡 Next Steps:")
        print("   - Fix failing tests")
        print("   - Get additional API keys")
        print("   - Check network connectivity")

        print("\n" + "="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
