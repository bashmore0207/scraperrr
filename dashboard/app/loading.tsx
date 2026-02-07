import ArticleCardSkeleton from "@/components/ArticleCardSkeleton";

export default function Loading() {
  return (
    <div className="min-h-screen bg-dark">
      {/* Header */}
      <header className="bg-darker border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-text-primary">
            Crypto Competitor Intelligence
          </h1>
          <p className="text-text-secondary mt-2">
            Loading latest news from crypto wallet competitors...
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-darker rounded-lg p-6 animate-pulse">
              <div className="h-4 w-24 bg-gray-700 rounded mb-2"></div>
              <div className="h-10 w-16 bg-gray-700 rounded"></div>
            </div>
          ))}
        </div>

        {/* Filter Bar Skeleton */}
        <div className="bg-darker rounded-lg p-6 mb-8 animate-pulse">
          <div className="h-6 w-20 bg-gray-700 rounded mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <div key={i}>
                <div className="h-4 w-32 bg-gray-700 rounded mb-2"></div>
                <div className="h-10 bg-gray-700 rounded"></div>
              </div>
            ))}
          </div>
        </div>

        {/* Articles Grid Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <ArticleCardSkeleton key={i} />
          ))}
        </div>
      </main>
    </div>
  );
}
