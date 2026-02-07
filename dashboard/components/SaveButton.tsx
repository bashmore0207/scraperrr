'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';

interface SaveButtonProps {
  articleId: string;
  initialSaved?: boolean;
}

export default function SaveButton({ articleId, initialSaved = false }: SaveButtonProps) {
  const [isSaved, setIsSaved] = useState(initialSaved);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSave() {
    setIsLoading(true);

    try {
      if (isSaved) {
        // Unsave - delete from saved_articles
        const { error } = await supabase
          .from('saved_articles')
          .delete()
          .eq('article_id', articleId);

        if (error) throw error;
        setIsSaved(false);
      } else {
        // Save - insert into saved_articles
        // Note: user_id would normally come from auth, but we'll use a placeholder for now
        const { error } = await supabase
          .from('saved_articles')
          .insert({
            article_id: articleId,
            user_id: '00000000-0000-0000-0000-000000000000', // Placeholder user
          });

        if (error) {
          // Ignore duplicate key errors (already saved)
          if (!error.message.includes('duplicate')) {
            throw error;
          }
        }
        setIsSaved(true);
      }
    } catch (error) {
      console.error('Error saving article:', error);
      alert('Failed to save article. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <button
      onClick={handleSave}
      disabled={isLoading}
      className={`transition-all duration-200 ${
        isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-110'
      }`}
      title={isSaved ? 'Unsave article' : 'Save article'}
    >
      <svg
        className={`w-5 h-5 transition-colors ${
          isSaved
            ? 'text-purple fill-purple'
            : 'text-text-secondary hover:text-purple'
        }`}
        fill={isSaved ? 'currentColor' : 'none'}
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
    </button>
  );
}
