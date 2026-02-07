export default function ArticleCardSkeleton() {
  return (
    <div className="bg-darker rounded-lg p-6 animate-pulse">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="h-4 w-24 bg-gray-700 rounded"></div>
        <div className="h-5 w-5 bg-gray-700 rounded"></div>
      </div>

      {/* Image placeholder */}
      <div className="mb-4 h-48 bg-gray-700 rounded"></div>

      {/* Title */}
      <div className="space-y-2 mb-4">
        <div className="h-6 bg-gray-700 rounded w-full"></div>
        <div className="h-6 bg-gray-700 rounded w-3/4"></div>
      </div>

      {/* Summary */}
      <div className="space-y-2 mb-4">
        <div className="h-4 bg-gray-700 rounded w-full"></div>
        <div className="h-4 bg-gray-700 rounded w-full"></div>
        <div className="h-4 bg-gray-700 rounded w-2/3"></div>
      </div>

      {/* Footer */}
      <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-700">
        <div className="flex gap-2">
          <div className="h-6 w-16 bg-gray-700 rounded-full"></div>
          <div className="h-6 w-16 bg-gray-700 rounded-full"></div>
        </div>
        <div className="flex items-center gap-3">
          <div className="h-4 w-20 bg-gray-700 rounded"></div>
          <div className="h-4 w-4 bg-gray-700 rounded"></div>
        </div>
      </div>
    </div>
  );
}
