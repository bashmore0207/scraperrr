# Task Plan - Crypto Competitor Intelligence Dashboard

## Project Status
**Current Phase:** Blueprint (Awaiting User Approval)
**Schema Status:** ✅ Complete
**Ready to Build:** Pending approval

---

## Blueprint Summary

### What We're Building
A beautiful, interactive web dashboard that monitors 7 crypto wallet competitors (Tangem, Trezor, Coinbase, Metamask, Revolut, Raby, Phantom) by collecting news articles from the last 24 hours. Users can save articles, share them, and see persistent data across sessions.

### Tech Stack
- **Frontend**: Next.js + React + Tailwind CSS
- **Backend**: Supabase (PostgreSQL + Real-time)
- **Scrapers**: Python (Beautiful Soup, Playwright, API clients)
- **Automation**: Vercel Cron Jobs or GitHub Actions (24h interval)
- **Hosting**: Vercel (frontend) + Supabase (backend)

### Data Flow
1. Scrapers run every 24h → Collect articles from APIs/websites
2. Store in Supabase → Deduplicate by URL
3. Dashboard fetches → Shows last 24h + saved articles
4. User saves/shares → Persist in Supabase

---

## Phase 0: Initialization ✅
- [x] Create project structure
- [x] Initialize memory files (gemini.md, findings.md, progress.md, task_plan.md)
- [x] Complete discovery questions
- [x] Define data schema in gemini.md
- [x] Research news APIs and sources
- [ ] **GET USER APPROVAL TO PROCEED**

---

## Phase 1: Blueprint (Vision & Logic) ✅
- [x] Answer discovery questions
- [x] Define JSON schemas (input/output)
- [x] Design Supabase database schema
- [x] Research external resources (CryptoNews API, CoinDesk API)
- [x] Document behavioral rules in gemini.md
- [ ] User approves blueprint

---

## Phase 2: Link (Connectivity)

### 2.1 Supabase Setup
- [ ] Create Supabase project
- [ ] Run SQL migrations (create tables: articles, saved_articles, scraper_runs)
- [ ] Configure Row Level Security (RLS) policies
- [ ] Get API keys and add to .env
- [ ] Test connection with handshake script

### 2.2 API Verification
- [ ] Sign up for CryptoNews API (cryptonews-api.com)
- [ ] Get API key and test endpoint
- [ ] Test CoinDesk API (if using)
- [ ] Document rate limits in gemini.md
- [ ] Build `tools/test_apis.py` handshake script

### 2.3 Environment Setup
- [ ] Create .env file with all keys
- [ ] Create .env.example template
- [ ] Verify all credentials work

**Success Criteria:** All API calls return 200, Supabase connection established

---

## Phase 3: Architect (3-Layer Build)

### 3.1 Layer 1: Architecture SOPs
- [ ] Create `architecture/scraper_sop.md` - How scrapers work
- [ ] Create `architecture/database_sop.md` - Schema and queries
- [ ] Create `architecture/dashboard_sop.md` - Frontend logic
- [ ] Create `architecture/automation_sop.md` - Cron job setup

### 3.2 Layer 3: Python Tools (Backend)
- [ ] `tools/scrape_cryptonews_api.py` - Fetch from CryptoNews API
- [ ] `tools/scrape_coindesk.py` - Fetch from CoinDesk
- [ ] `tools/competitor_filter.py` - Filter articles by competitor mentions
- [ ] `tools/supabase_client.py` - Database operations (insert, dedupe, query)
- [ ] `tools/orchestrator.py` - Main scraper orchestrator
- [ ] Write unit tests for each tool

### 3.3 Layer 3: Frontend (Next.js)
- [ ] Initialize Next.js project with Tailwind CSS
- [ ] Create Supabase client configuration
- [ ] Build components:
  - [ ] `ArticleCard.tsx` - Individual article display
  - [ ] `ArticleFeed.tsx` - Main feed with filters
  - [ ] `SavedArticles.tsx` - User's saved items
  - [ ] `CompetitorFilter.tsx` - Filter by competitor
  - [ ] `EmptyState.tsx` - "No new articles" message
- [ ] Implement save/unsave functionality
- [ ] Implement share functionality (generate share links)
- [ ] Add real-time updates (Supabase subscriptions)

### 3.4 Layer 2: Navigation Logic
- [ ] Dashboard fetches articles from Supabase (last 24h)
- [ ] Dashboard fetches user's saved articles (persistent)
- [ ] Scrapers write to Supabase (deduplicate by URL)
- [ ] Error handling: failed scrapes don't break dashboard

**Success Criteria:** End-to-end flow works - scrapers → database → dashboard

---

## Phase 4: Stylize (Refinement & UI)

### 4.1 Design System Implementation
- [ ] Configure Tailwind with custom colors (#966FE8 purple, #2A272F background)
- [ ] Add Circular Std font (or similar system fallback)
- [ ] Set up 8px spacing scale in Tailwind config
- [ ] Create design tokens for consistency

### 4.2 Layout & Components (Based on Design Inspiration)
- [ ] **Sidebar Navigation**:
  - Dark sidebar with competitor filters
  - "All Articles", "Saved Articles" sections
  - Competitor list with counts
  - Purple highlight on active filter
- [ ] **Article Cards**:
  - Card background (#363340, lighter than main bg)
  - Featured image at top (if available)
  - Title (H2, bold, white text)
  - Source badge + competitor tags (purple accents)
  - Summary text (gray, smaller)
  - Metadata row (date, author, gray text)
  - Action icons (bookmark, share) - subtle, purple on hover
- [ ] **Empty State**: "No new articles" message with icon
- [ ] **Header**: Logo/title area, last updated timestamp

### 4.3 Visual Polish
- [ ] Add subtle card shadows for depth
- [ ] Smooth hover transitions (purple glow on cards)
- [ ] Loading skeleton screens with purple shimmer
- [ ] Toast notifications (purple accent, slide-in animation)
- [ ] Smooth animations for save/unsave
- [ ] Purple ripple effect on button clicks

### 4.4 Responsive Design
- [ ] Mobile: Stack sidebar, hamburger menu
- [ ] Tablet: Collapsible sidebar
- [ ] Desktop: Full sidebar + cards layout
- [ ] Ensure cards look great on all screen sizes

### 4.2 UX Enhancements
- [ ] Add search functionality
- [ ] Add sort options (date, source, competitor)
- [ ] Implement infinite scroll or pagination
- [ ] Add keyboard shortcuts (save with 's', etc.)
- [ ] Add dark mode toggle

### 4.3 User Testing
- [ ] Present dashboard to user for feedback
- [ ] Gather improvement suggestions
- [ ] Iterate on design based on feedback

**Success Criteria:** User approves design, dashboard is beautiful and interactive

---

## Phase 5: Trigger (Deployment)

### 5.1 Automation Setup
- [ ] Create `vercel.json` with cron job configuration (runs every 24h)
- [ ] OR: Set up GitHub Actions workflow for scraper
- [ ] Test cron job runs successfully
- [ ] Add error notifications (email/Slack if scraper fails)

### 5.2 Cloud Deployment
- [ ] Deploy Next.js app to Vercel
- [ ] Configure environment variables in Vercel
- [ ] Test production deployment
- [ ] Verify Supabase connection in production

### 5.3 Final Documentation
- [ ] Create README.md with setup instructions
- [ ] Document maintenance procedures in gemini.md
- [ ] Create user guide for dashboard features
- [ ] Finalize scraper_runs log for monitoring

### 5.4 Monitoring & Maintenance
- [ ] Set up Supabase dashboard monitoring
- [ ] Create alerts for scraper failures
- [ ] Implement data retention policy (30 days)
- [ ] Schedule first scraper run

**Success Criteria:** Dashboard is live, scrapers run automatically every 24h, user can access from anywhere

---

## Current Goals
1. ✅ Complete data schema definition
2. ✅ Document all behavioral rules
3. ✅ Create detailed blueprint
4. **🎯 GET USER APPROVAL TO PROCEED TO PHASE 2**

## Blockers
None - awaiting user approval to begin Phase 2 (Link)

---

## Estimated Timeline
- **Phase 2 (Link)**: 1-2 hours - API setup and verification
- **Phase 3 (Architect)**: 8-12 hours - Core development (scrapers + dashboard)
- **Phase 4 (Stylize)**: 3-4 hours - Design and UX refinement
- **Phase 5 (Trigger)**: 2-3 hours - Deployment and automation

**Total**: ~14-21 hours of development time
