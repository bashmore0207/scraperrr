import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Create client with fallback for build time
export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseKey || 'placeholder-key'
);

// Type definitions for our database
export interface Article {
  id: string;
  title: string;
  url: string;
  source: string;
  competitors: string[];
  published_at: string;
  scraped_at: string;
  summary: string | null;
  image_url: string | null;
  author: string | null;
  created_at: string;
}

export interface SavedArticle {
  id: string;
  article_id: string;
  user_id: string;
  saved_at: string;
  share_token: string;
}

export interface ScraperRun {
  id: string;
  started_at: string;
  completed_at: string | null;
  articles_found: number;
  articles_added: number;
  status: 'running' | 'completed' | 'failed';
  error_message: string | null;
}

// Fetch articles with filters
export async function fetchArticles(filters?: {
  hours?: number;
  competitors?: string[];
  sources?: string[];
  limit?: number;
}) {
  let query = supabase
    .from('articles')
    .select('*')
    .order('published_at', { ascending: false });

  // Filter by time window
  if (filters?.hours) {
    const cutoff = new Date();
    cutoff.setHours(cutoff.getHours() - filters.hours);
    query = query.gte('published_at', cutoff.toISOString());
  }

  // Filter by competitors
  if (filters?.competitors?.length) {
    query = query.overlaps('competitors', filters.competitors);
  }

  // Filter by sources
  if (filters?.sources?.length) {
    query = query.in('source', filters.sources);
  }

  // Limit results
  if (filters?.limit) {
    query = query.limit(filters.limit);
  } else {
    query = query.limit(100); // Default limit
  }

  const { data, error } = await query;

  if (error) {
    console.error('Error fetching articles:', error);
    throw error;
  }

  return data as Article[];
}

// Get unique competitors and sources for filters
export async function getFilters() {
  const { data, error } = await supabase
    .from('articles')
    .select('competitors, source');

  if (error) {
    console.error('Error fetching filters:', error);
    return { competitors: [], sources: [] };
  }

  const competitors = new Set<string>();
  const sources = new Set<string>();

  data.forEach((article: any) => {
    article.competitors?.forEach((comp: string) => competitors.add(comp));
    if (article.source) sources.add(article.source);
  });

  return {
    competitors: Array.from(competitors).sort(),
    sources: Array.from(sources).sort(),
  };
}

// Format time ago (e.g., "2 hours ago")
export function timeAgo(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  const intervals: { [key: string]: number } = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
    second: 1,
  };

  for (const [name, value] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / value);
    if (interval >= 1) {
      return interval === 1
        ? `1 ${name} ago`
        : `${interval} ${name}s ago`;
    }
  }

  return 'just now';
}
