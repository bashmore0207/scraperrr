import ArticleCard from "@/components/ArticleCard";
import { supabase, Article } from "@/lib/supabase";
import Link from "next/link";

export const dynamic = 'force-dynamic';

async function getSavedArticles() {
  // Fetch saved articles with article details
  const { data, error } = await supabase
    .from('saved_articles')
    .select(`
      id,
      saved_at,
      article_id,
      articles (*)
    `)
    .order('saved_at', { ascending: false });

  if (error) {
    console.error('Error fetching saved articles:', error);
    return [];
  }

  // Extract article data
  return data.map((saved: any) => ({
    ...saved.articles,
    saved_at: saved.saved_at,
  })) as Article[];
}

export default async function SavedArticlesPage() {
  const savedArticles = await getSavedArticles();

  return (
    <div className="min-h-screen bg-dark">
      {/* Header */}
      <header className="bg-darker border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-4 mb-2">
            <Link
              href="/"
              className="text-text-secondary hover:text-purple transition-colors"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 19l-7-7m0 0l7-7m-7 7h18"
                />
              </svg>
            </Link>
            <h1 className="text-3xl font-bold text-text-primary">
              Saved Articles
            </h1>
          </div>
          <p className="text-text-secondary">
            {savedArticles.length} article{savedArticles.length !== 1 ? 's' : ''} saved for later
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {savedArticles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedArticles.map((article) => (
              <ArticleCard
                key={article.id}
                article={article}
                initialSaved={true}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-darker rounded-lg">
            <svg
              className="w-16 h-16 text-text-tertiary mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
            <p className="text-text-secondary text-lg mb-2">
              No saved articles yet
            </p>
            <p className="text-text-tertiary text-sm mb-6">
              Click the heart icon on any article to save it for later
            </p>
            <Link
              href="/"
              className="inline-block bg-purple hover:bg-purple/80 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Browse Articles
            </Link>
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
