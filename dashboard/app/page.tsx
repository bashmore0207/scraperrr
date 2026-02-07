import ArticleGrid from "@/components/ArticleGrid";
import Header from "@/components/Header";
import { fetchArticles, getFilters } from "@/lib/supabase";

export const dynamic = 'force-dynamic'; // Always fetch fresh data

export default async function HomePage() {
  // Fetch articles from last week (filtering happens client-side)
  const articles = await fetchArticles({ hours: 168 });
  const filters = await getFilters();

  return (
    <div className="min-h-screen bg-dark">
      <Header />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-darker rounded-lg p-6">
            <div className="text-text-secondary text-sm mb-1">Total Articles</div>
            <div className="text-3xl font-bold text-purple">
              {articles.length}
            </div>
          </div>
          <div className="bg-darker rounded-lg p-6">
            <div className="text-text-secondary text-sm mb-1">Competitors Tracked</div>
            <div className="text-3xl font-bold text-purple">
              {filters.competitors.length}
            </div>
          </div>
          <div className="bg-darker rounded-lg p-6">
            <div className="text-text-secondary text-sm mb-1">Data Sources</div>
            <div className="text-3xl font-bold text-purple">
              {filters.sources.length}
            </div>
          </div>
        </div>

        {/* Articles Grid with Filters */}
        {articles.length > 0 ? (
          <ArticleGrid
            initialArticles={articles}
            competitors={filters.competitors}
            sources={filters.sources}
          />
        ) : (
          <div className="text-center py-12 bg-darker rounded-lg">
            <p className="text-text-secondary text-lg">
              No articles found.
            </p>
            <p className="text-text-tertiary text-sm mt-2">
              Run the scrapers to collect data: <code className="bg-dark px-2 py-1 rounded">python3 tools/run_all_scrapers.py</code>
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-darker border-t border-gray-700 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-text-tertiary text-sm text-center">
            Last updated: {new Date().toLocaleString()}
          </p>
        </div>
      </footer>
    </div>
  );
}
