import Link from 'next/link';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showSavedLink?: boolean;
}

export default function Header({
  title = "Crypto Competitor Intelligence",
  subtitle = "Latest news from crypto wallet competitors (last 24 hours)",
  showSavedLink = true,
}: HeaderProps) {
  return (
    <header className="bg-darker border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-text-primary">
              {title}
            </h1>
            <p className="text-text-secondary mt-2">
              {subtitle}
            </p>
          </div>

          {showSavedLink && (
            <Link
              href="/saved"
              className="flex items-center gap-2 bg-purple hover:bg-purple/80 text-white px-4 py-2 rounded-lg transition-all duration-200 hover:scale-105"
            >
              <svg
                className="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span className="hidden sm:inline">Saved Articles</span>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
