import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

/**
 * Scraper Trigger API Route
 * Called by Vercel Cron every 24 hours to trigger article scraping
 *
 * Options for running Python scrapers:
 * 1. GitHub Actions (recommended for this project)
 * 2. External webhook service (Railway, Render, etc.)
 * 3. Vercel Serverless Functions with Python runtime
 */
export async function GET(request: Request) {
  try {
    // Verify the request is from Vercel Cron
    const authHeader = request.headers.get('authorization');
    const cronSecret = process.env.CRON_SECRET;

    if (cronSecret && authHeader !== `Bearer ${cronSecret}`) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Option 1: Trigger GitHub Actions workflow (recommended)
    if (process.env.GITHUB_TOKEN && process.env.GITHUB_REPO) {
      const response = await fetch(
        `https://api.github.com/repos/${process.env.GITHUB_REPO}/actions/workflows/scrape.yml/dispatches`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ref: 'main',
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.statusText}`);
      }

      return NextResponse.json({
        success: true,
        message: 'Scraper workflow triggered via GitHub Actions',
        timestamp: new Date().toISOString(),
      });
    }

    // Option 2: Trigger external webhook
    if (process.env.SCRAPER_WEBHOOK_URL) {
      const response = await fetch(process.env.SCRAPER_WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(process.env.SCRAPER_WEBHOOK_SECRET && {
            'Authorization': `Bearer ${process.env.SCRAPER_WEBHOOK_SECRET}`,
          }),
        },
        body: JSON.stringify({
          action: 'run_scrapers',
          timestamp: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error(`Webhook error: ${response.statusText}`);
      }

      return NextResponse.json({
        success: true,
        message: 'Scraper webhook triggered',
        timestamp: new Date().toISOString(),
      });
    }

    // No scraper trigger configured
    return NextResponse.json({
      success: false,
      message: 'No scraper trigger configured. Set GITHUB_TOKEN + GITHUB_REPO or SCRAPER_WEBHOOK_URL',
      timestamp: new Date().toISOString(),
    }, { status: 501 });

  } catch (error) {
    console.error('Scraper trigger error:', error);
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}

// Manual trigger endpoint (for testing)
export async function POST(request: Request) {
  return GET(request);
}
