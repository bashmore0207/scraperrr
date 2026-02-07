# Dashboard Architecture SOP

## Purpose
Defines the standard operating procedure for the Next.js dashboard frontend.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **State Management**: React hooks + Supabase Realtime
- **Deployment**: Vercel

## Design System

### Colors
```css
/* Primary */
--purple: #966FE8;      /* Brand purple - buttons, links, accents */
--dark: #2A272F;        /* Background dark */
--darker: #1F1D23;      /* Card/section backgrounds */

/* Text */
--text-primary: #FFFFFF;    /* Main text */
--text-secondary: #A0A0A0;  /* Muted text */
--text-tertiary: #666666;   /* Disabled/placeholder */

/* Status */
--success: #10B981;     /* Green - saved articles */
--warning: #F59E0B;     /* Orange - alerts */
--error: #EF4444;       /* Red - errors */
```

### Typography
- **Font Family**: Circular Std (fallback: system-ui, sans-serif)
- **Headings**: Bold (700), Purple accent
- **Body**: Regular (400), White text
- **Small Text**: Medium (500), Gray secondary

### Spacing
- **Container**: max-w-7xl (1280px)
- **Padding**: px-4 sm:px-6 lg:px-8
- **Gap**: gap-4 (16px) for cards, gap-6 (24px) for sections

## Project Structure

```
dashboard/
├── app/
│   ├── layout.tsx              # Root layout with design system
│   ├── page.tsx                # Homepage (article feed)
│   ├── saved/
│   │   └── page.tsx            # Saved articles page
│   └── api/
│       ├── articles/
│       │   └── route.ts        # Fetch articles API
│       └── save/
│           └── route.ts        # Save article API
├── components/
│   ├── ArticleCard.tsx         # Article card component
│   ├── ArticleGrid.tsx         # Grid layout for articles
│   ├── CompetitorFilter.tsx    # Filter by competitor
│   ├── SourceFilter.tsx        # Filter by source
│   ├── SaveButton.tsx          # Save/unsave toggle
│   ├── ShareButton.tsx         # Share functionality
│   └── Sidebar.tsx             # Navigation sidebar
├── lib/
│   ├── supabase.ts             # Supabase client
│   └── utils.ts                # Utility functions
├── public/
│   └── fonts/                  # Circular Std font files
└── types/
    └── article.ts              # TypeScript types
```

## Core Components

### 1. Article Card

**Purpose**: Display a single article with all relevant info

**Props**:
```typescript
interface ArticleCardProps {
  article: Article;
  onSave?: (articleId: string) => void;
  onShare?: (articleId: string) => void;
  isSaved?: boolean;
}
```

**Design**:
- Dark card background (#1F1D23)
- Purple border on hover
- Competitor tags (purple pills)
- Source badge (top-right)
- Save heart icon (top-right)
- Share icon (bottom-right)
- Published timestamp (relative: "2 hours ago")
- Image thumbnail (if available)

**Layout**:
```jsx
<article className="bg-darker rounded-lg p-6 hover:border-purple transition">
  {/* Header */}
  <div className="flex justify-between items-start">
    <span className="text-xs text-secondary">{source}</span>
    <SaveButton isSaved={isSaved} onClick={onSave} />
  </div>

  {/* Image (if exists) */}
  {imageUrl && <img src={imageUrl} className="rounded mt-4" />}

  {/* Title */}
  <h3 className="text-xl font-bold text-primary mt-4">{title}</h3>

  {/* Summary */}
  <p className="text-secondary mt-2">{summary}</p>

  {/* Footer */}
  <div className="flex justify-between items-center mt-4">
    {/* Competitor tags */}
    <div className="flex gap-2">
      {competitors.map(c => (
        <span className="bg-purple/20 text-purple px-2 py-1 rounded text-xs">
          {c}
        </span>
      ))}
    </div>

    {/* Share + Timestamp */}
    <div className="flex items-center gap-3">
      <span className="text-xs text-tertiary">{timeAgo}</span>
      <ShareButton articleId={id} />
    </div>
  </div>
</article>
```

### 2. Sidebar Navigation

**Purpose**: Persistent navigation with competitor filters

**Features**:
- Logo/title at top
- "All Articles" link
- "Saved Articles" link
- Competitor filter checkboxes
- Source filter checkboxes
- Last updated timestamp

**Design**:
- Fixed left sidebar (hidden on mobile, toggle menu)
- Dark background (#2A272F)
- Purple active states
- Smooth transitions

### 3. Article Grid

**Purpose**: Responsive grid layout for article cards

**Breakpoints**:
- Mobile: 1 column
- Tablet: 2 columns
- Desktop: 3 columns

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {articles.map(article => (
    <ArticleCard key={article.id} article={article} />
  ))}
</div>
```

## Data Fetching Strategy

### Server Components (RSC)
- Homepage fetches articles server-side
- Better SEO, faster initial load
- Use `fetch()` with `cache: 'no-store'` for fresh data

```typescript
// app/page.tsx
export default async function HomePage() {
  const articles = await fetchArticles({ hours: 24 });

  return <ArticleGrid articles={articles} />;
}
```

### Client Components (Interactive)
- Filters use client state
- Save/share buttons use client actions
- Mark with `'use client'`

```typescript
'use client';

export function CompetitorFilter({ onFilter }) {
  const [selected, setSelected] = useState<string[]>([]);
  // ...
}
```

### Supabase Integration

**Client Setup**:
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseKey);
```

**Fetching Articles**:
```typescript
export async function fetchArticles(filters?: {
  hours?: number;
  competitors?: string[];
  sources?: string[];
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

  const { data, error } = await query;

  if (error) throw error;
  return data;
}
```

## Save/Share Functionality

### Save Article

**Client Action**:
```typescript
'use client';

export function SaveButton({ articleId, initialSaved }) {
  const [isSaved, setIsSaved] = useState(initialSaved);

  async function handleSave() {
    if (isSaved) {
      // Unsave
      await supabase
        .from('saved_articles')
        .delete()
        .eq('article_id', articleId);
    } else {
      // Save
      await supabase
        .from('saved_articles')
        .insert({ article_id: articleId, saved_at: new Date().toISOString() });
    }

    setIsSaved(!isSaved);
  }

  return (
    <button onClick={handleSave}>
      {isSaved ? <HeartFilledIcon /> : <HeartOutlineIcon />}
    </button>
  );
}
```

### Share Article

**Client Action**:
```typescript
'use client';

export function ShareButton({ article }) {
  async function handleShare() {
    const shareData = {
      title: article.title,
      text: article.summary,
      url: article.url
    };

    if (navigator.share) {
      // Native share (mobile)
      await navigator.share(shareData);
    } else {
      // Fallback: copy link
      await navigator.clipboard.writeText(article.url);
      toast.success('Link copied to clipboard!');
    }
  }

  return (
    <button onClick={handleShare}>
      <ShareIcon />
    </button>
  );
}
```

## Responsive Design

### Mobile (<768px)
- Hamburger menu for sidebar
- 1-column grid
- Smaller card padding
- Stack save/share buttons vertically

### Tablet (768px - 1024px)
- Collapsible sidebar (slide-in)
- 2-column grid
- Medium card padding

### Desktop (>1024px)
- Fixed sidebar (always visible)
- 3-column grid
- Full card padding
- Hover effects

## Performance Optimizations

1. **Image Optimization**: Use Next.js `<Image>` component
2. **Lazy Loading**: Load articles as user scrolls (pagination)
3. **Caching**: Cache article fetches for 60 seconds
4. **Debouncing**: Debounce filter changes (300ms)
5. **Virtualization**: If >100 articles, use virtual scrolling

## Accessibility

- Semantic HTML (`<article>`, `<nav>`, `<main>`)
- ARIA labels for icon buttons
- Keyboard navigation (Tab, Enter, Escape)
- Focus indicators (purple outline)
- Color contrast WCAG AA compliant

## Error States

### No Articles Found
```jsx
<div className="text-center py-12">
  <p className="text-secondary">No articles found in the last 24 hours.</p>
  <p className="text-tertiary text-sm mt-2">Try adjusting your filters or check back later.</p>
</div>
```

### Loading State
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {[...Array(9)].map((_, i) => (
    <SkeletonCard key={i} />
  ))}
</div>
```

### Error State
```jsx
<div className="bg-error/10 border border-error rounded-lg p-6">
  <p className="text-error">Failed to load articles. Please try again.</p>
</div>
```

## Environment Variables

```env
# .env.local (Next.js)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

## Deployment

1. Push to GitHub
2. Connect Vercel to repo
3. Set environment variables in Vercel dashboard
4. Deploy (automatic on push to main)

## Testing Checklist

Before deploying:
- [ ] All articles render correctly
- [ ] Filters work (competitor, source, time)
- [ ] Save/unsave functionality works
- [ ] Share functionality works (mobile + desktop)
- [ ] Responsive on mobile, tablet, desktop
- [ ] No console errors
- [ ] Dark theme applied correctly
- [ ] Purple accents visible throughout
- [ ] Circular Std font loaded
- [ ] Timestamps show relative time ("2 hours ago")
- [ ] Empty state shows when no articles
- [ ] Loading state shows during fetch
