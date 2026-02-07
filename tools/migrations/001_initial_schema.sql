-- Crypto Competitor Intelligence Dashboard
-- Initial Database Schema
-- Created: 2026-02-06

-- Table 1: Articles
-- Stores all scraped competitor news articles
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL,
  source TEXT NOT NULL,
  competitors TEXT[] NOT NULL,
  published_at TIMESTAMPTZ NOT NULL,
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  summary TEXT,
  image_url TEXT,
  author TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_published_at ON articles(published_at DESC);
CREATE INDEX idx_competitors ON articles USING GIN(competitors);

-- Table 2: Saved Articles
-- Tracks user-saved articles with share functionality
CREATE TABLE saved_articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  saved_at TIMESTAMPTZ DEFAULT NOW(),
  share_token UUID DEFAULT gen_random_uuid(),
  UNIQUE(article_id, user_id)
);

-- Indexes for saved articles
CREATE INDEX idx_user_saved ON saved_articles(user_id, saved_at DESC);
CREATE INDEX idx_share_token ON saved_articles(share_token);

-- Table 3: Scraper Runs
-- Logs all scraper executions for monitoring
CREATE TABLE scraper_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  articles_found INTEGER DEFAULT 0,
  articles_added INTEGER DEFAULT 0,
  status TEXT CHECK (status IN ('running', 'completed', 'failed')),
  error_message TEXT
);

-- Row Level Security (RLS) Policies
-- Enable RLS on tables
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE scraper_runs ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read articles
CREATE POLICY "Articles are viewable by everyone"
  ON articles FOR SELECT
  USING (true);

-- Policy: Authenticated users can save articles
CREATE POLICY "Users can manage their own saved articles"
  ON saved_articles FOR ALL
  USING (auth.uid() = user_id);

-- Policy: Only service role can write articles
CREATE POLICY "Service role can insert articles"
  ON articles FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

-- Policy: Anyone can read scraper runs (for dashboard monitoring)
CREATE POLICY "Scraper runs are viewable by everyone"
  ON scraper_runs FOR SELECT
  USING (true);

-- Policy: Only service role can write scraper runs
CREATE POLICY "Service role can manage scraper runs"
  ON scraper_runs FOR ALL
  WITH CHECK (auth.role() = 'service_role');
