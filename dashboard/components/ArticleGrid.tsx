'use client';

import { useState, useCallback } from 'react';
import ArticleCard from './ArticleCard';
import FilterBar from './FilterBar';
import { Article } from '@/lib/supabase';

interface ArticleGridProps {
  initialArticles: Article[];
  competitors: string[];
  sources: string[];
}

export default function ArticleGrid({ initialArticles, competitors, sources }: ArticleGridProps) {
  const [filters, setFilters] = useState({
    competitors: [] as string[],
    sources: [] as string[],
    hours: 24,
  });

  const handleFilterChange = useCallback((newFilters: typeof filters) => {
    setFilters(newFilters);
  }, []);

  // Filter articles based on current filters
  const filteredArticles = initialArticles.filter(article => {
    // Filter by competitor
    if (filters.competitors.length > 0) {
      const hasMatchingCompetitor = article.competitors.some(comp =>
        filters.competitors.includes(comp)
      );
      if (!hasMatchingCompetitor) return false;
    }

    // Filter by source
    if (filters.sources.length > 0) {
      if (!filters.sources.includes(article.source)) return false;
    }

    // Filter by time range
    const articleDate = new Date(article.published_at);
    const cutoff = new Date();
    cutoff.setHours(cutoff.getHours() - filters.hours);
    if (articleDate < cutoff) return false;

    return true;
  });

  return (
    <>
      {/* Filter Bar */}
      <FilterBar
        competitors={competitors}
        sources={sources}
        onFilterChange={handleFilterChange}
      />

      {/* Results Count */}
      <div className="mb-4 text-text-secondary">
        Showing {filteredArticles.length} of {initialArticles.length} articles
      </div>

      {/* Articles Grid */}
      {filteredArticles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredArticles.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-darker rounded-lg">
          <p className="text-text-secondary text-lg">
            No articles match your filters.
          </p>
          <p className="text-text-tertiary text-sm mt-2">
            Try adjusting your filter criteria above.
          </p>
        </div>
      )}
    </>
  );
}
