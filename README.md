# Crypto Competitor Intelligence Dashboard

A beautiful, automated dashboard for monitoring competitor news from crypto wallet companies (Ledger, Trezor, Tangem, Coinbase, Metamask, Revolut, Raby, Phantom).

![Dashboard Preview](https://via.placeholder.com/1200x600/2A272F/966FE8?text=Crypto+Competitor+Intelligence+Dashboard)

## Features

- 📰 **Automated News Collection** - Scrapes crypto news every 24 hours
- 🎯 **Competitor Detection** - Automatically identifies mentions of 7+ competitors
- 🎨 **Beautiful UI** - Purple/dark design with smooth animations
- 🔍 **Advanced Filtering** - Filter by time, competitor, and source
- 💜 **Save Articles** - Bookmark articles for later reading
- 📱 **Responsive Design** - Works on mobile, tablet, and desktop
- ⚡ **Real-time Updates** - Fresh data from Supabase database

## Tech Stack

**Frontend:**
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- Supabase Client

**Backend:**
- Supabase (PostgreSQL + RLS)
- Python 3.9
- NewsData.io API
- RSS Feeds

**Deployment:**
- Vercel (Dashboard)
- GitHub Actions (Scrapers)

## Project Structure

```
Scraperrr/
├── dashboard/              # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities (Supabase client)
│   └── types/            # TypeScript types
├── tools/                 # Python scrapers
│   ├── scrape_newsdata.py    # NewsData.io scraper
│   ├── scrape_rss.py         # RSS feed scraper
│   └── run_all_scrapers.py   # Master orchestrator
├── architecture/          # Architecture SOPs
├── .github/workflows/     # GitHub Actions
└── progress.md           # Project history
```

## Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd Scraperrr

# Install Python dependencies
pip install -r tools/requirements.txt

# Install dashboard dependencies
cd dashboard
npm install
```

### 2. Set Up Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Run the migration:
   ```sql
   -- Copy contents from tools/migrations/001_initial_schema.sql
   -- Paste into Supabase SQL Editor and run
   ```
3. Get your credentials from Project Settings → API

### 3. Get API Keys

- **NewsData.io**: Sign up at [newsdata.io](https://newsdata.io) (free tier: 200 req/day)
- **Supabase**: From your project settings

### 4. Configure Environment Variables

Create `.env` in project root:
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# News API
NEWSDATA_API_KEY=your_newsdata_key
```

Create `dashboard/.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

### 5. Run Locally

**Start the dashboard:**
```bash
cd dashboard
npm run dev
# Open http://localhost:3000
```

**Run scrapers manually:**
```bash
python3 tools/run_all_scrapers.py
```

## Deployment Guide

### Deploy Dashboard to Vercel

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set root directory to `dashboard`
   - Add environment variables:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Deploy!

3. **Enable Cron Jobs:**
   - Vercel will automatically detect `vercel.json` cron configuration
   - Add `CRON_SECRET` environment variable (generate a random string)

### Set Up Automated Scraping

**Option 1: GitHub Actions (Recommended)**

1. Add GitHub Secrets (Settings → Secrets → Actions):
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `NEWSDATA_API_KEY`

2. Add to Vercel environment variables:
   - `GITHUB_TOKEN` - Generate at GitHub Settings → Developer Settings → Personal Access Tokens
   - `GITHUB_REPO` - Format: `username/repo-name`
   - `CRON_SECRET` - Random string for security

3. Workflow runs automatically:
   - Daily at midnight UTC (GitHub Actions schedule)
   - Every 24 hours via Vercel cron → GitHub API

**Option 2: External Webhook**

Deploy scrapers to Railway/Render and set:
- `SCRAPER_WEBHOOK_URL` in Vercel
- `SCRAPER_WEBHOOK_SECRET` for authentication

## Usage

### View Dashboard

Visit your deployed URL or `localhost:3000` to:
- View latest competitor news (last 24 hours)
- Filter by competitor, source, or time range
- Save articles for later
- Share articles via native share or clipboard

### Manual Scraper Run

```bash
# Run all scrapers
python3 tools/run_all_scrapers.py

# Run individual scrapers
python3 tools/scrape_newsdata.py
python3 tools/scrape_rss.py
```

### Add New Scrapers

1. Create new scraper in `tools/` following SOP pattern (see `architecture/01_scraper_sop.md`)
2. Add to `tools/run_all_scrapers.py`
3. Test locally
4. Deploy!

## API Routes

### `/api/scrape` (GET/POST)

Triggers scraper run via GitHub Actions or webhook.

**Headers:**
```
Authorization: Bearer <CRON_SECRET>
```

**Response:**
```json
{
  "success": true,
  "message": "Scraper workflow triggered via GitHub Actions",
  "timestamp": "2026-02-06T22:00:00.000Z"
}
```

## Database Schema

See [tools/migrations/001_initial_schema.sql](tools/migrations/001_initial_schema.sql) for complete schema.

**Key Tables:**
- `articles` - All scraped news articles
- `saved_articles` - User bookmarks
- `scraper_runs` - Execution logs

## Design System

**Colors:**
- Purple: `#966FE8` (primary accent)
- Dark: `#2A272F` (background)
- Darker: `#1F1D23` (cards)

**Typography:**
- Font: System UI (sans-serif)
- Headings: Bold, purple accent
- Body: Regular, white/gray

## Monitoring

**Check Scraper Runs:**
```sql
SELECT * FROM scraper_runs ORDER BY started_at DESC LIMIT 10;
```

**Check Article Count:**
```sql
SELECT
  source,
  COUNT(*) as article_count,
  MAX(published_at) as latest_article
FROM articles
GROUP BY source;
```

## Troubleshooting

**No articles showing:**
1. Run scrapers manually: `python3 tools/run_all_scrapers.py`
2. Check Supabase dashboard for data
3. Verify environment variables

**Scraper errors:**
1. Check API rate limits (NewsData.io: 60 req/hour)
2. Verify Supabase credentials
3. Review logs in GitHub Actions

**Deployment issues:**
1. Ensure root directory is set to `dashboard` in Vercel
2. Verify all environment variables are set
3. Check build logs

## Contributing

1. Follow B.L.A.S.T. protocol (Blueprint → Link → Architect → Stylize → Trigger)
2. Document changes in `progress.md`
3. Follow architecture SOPs in `architecture/`
4. Test locally before pushing

## License

MIT

## Support

For issues or questions, open an issue on GitHub.

---

Built with 💜 by Claude Sonnet 4.5
