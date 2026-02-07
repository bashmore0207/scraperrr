'use client';

import { Article, timeAgo } from '@/lib/supabase';
import SaveButton from './SaveButton';

interface ArticleCardProps {
  article: Article;
  initialSaved?: boolean;
}

export default function ArticleCard({ article, initialSaved = false }: ArticleCardProps) {
  return (
    <article className="group bg-darker rounded-lg p-6 border border-transparent hover:border-purple hover:shadow-lg hover:shadow-purple/20 transition-all duration-300 hover:-translate-y-1">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <span className="text-xs text-text-secondary font-medium">
          {article.source}
        </span>
        <SaveButton articleId={article.id} initialSaved={initialSaved} />
      </div>

      {/* Image (if exists) */}
      {article.image_url && (
        <div className="mb-4 rounded overflow-hidden">
          <img
            src={article.image_url}
            alt={article.title}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>
      )}

      {/* Title */}
      <h3 className="text-xl font-bold text-text-primary mb-2 line-clamp-2">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-purple transition-colors"
        >
          {article.title}
        </a>
      </h3>

      {/* Summary */}
      {article.summary && (
        <p className="text-text-secondary text-sm mb-4 line-clamp-3">
          {article.summary}
        </p>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-700">
        {/* Competitor tags */}
        <div className="flex gap-2 flex-wrap">
          {article.competitors.map((competitor) => (
            <span
              key={competitor}
              className="bg-purple/20 text-purple px-2 py-1 rounded text-xs font-medium"
            >
              {competitor}
            </span>
          ))}
        </div>

        {/* Timestamp + Share */}
        <div className="flex items-center gap-3">
          <span className="text-xs text-text-tertiary">
            {timeAgo(article.published_at)}
          </span>
          <button
            className="text-text-secondary hover:text-purple transition-colors"
            title="Share article"
            onClick={() => {
              if (navigator.share) {
                navigator.share({
                  title: article.title,
                  text: article.summary || '',
                  url: article.url,
                });
              } else {
                navigator.clipboard.writeText(article.url);
                alert('Link copied to clipboard!');
              }
            }}
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
              />
            </svg>
          </button>
        </div>
      </div>
    </article>
  );
}
