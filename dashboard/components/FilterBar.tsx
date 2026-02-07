'use client';

import { useState, useEffect } from 'react';

interface FilterBarProps {
  competitors: string[];
  sources: string[];
  onFilterChange: (filters: {
    competitors: string[];
    sources: string[];
    hours: number;
  }) => void;
}

export default function FilterBar({ competitors, sources, onFilterChange }: FilterBarProps) {
  const [selectedCompetitors, setSelectedCompetitors] = useState<string[]>([]);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [timeRange, setTimeRange] = useState<number>(24);

  // Notify parent of filter changes
  useEffect(() => {
    onFilterChange({
      competitors: selectedCompetitors,
      sources: selectedSources,
      hours: timeRange,
    });
  }, [selectedCompetitors, selectedSources, timeRange, onFilterChange]);

  const toggleCompetitor = (competitor: string) => {
    setSelectedCompetitors(prev =>
      prev.includes(competitor)
        ? prev.filter(c => c !== competitor)
        : [...prev, competitor]
    );
  };

  const toggleSource = (source: string) => {
    setSelectedSources(prev =>
      prev.includes(source)
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  const clearFilters = () => {
    setSelectedCompetitors([]);
    setSelectedSources([]);
    setTimeRange(24);
  };

  const hasActiveFilters = selectedCompetitors.length > 0 || selectedSources.length > 0 || timeRange !== 24;

  return (
    <div className="bg-darker rounded-lg p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-text-primary">Filters</h2>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-purple hover:text-purple/80 transition-colors"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Time Range Filter */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Time Range
          </label>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(Number(e.target.value))}
            className="w-full bg-dark border border-gray-700 rounded-lg px-4 py-2 text-text-primary focus:outline-none focus:border-purple transition-colors"
          >
            <option value={6}>Last 6 hours</option>
            <option value={12}>Last 12 hours</option>
            <option value={24}>Last 24 hours</option>
            <option value={48}>Last 2 days</option>
            <option value={168}>Last week</option>
          </select>
        </div>

        {/* Competitor Filter */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Competitors ({selectedCompetitors.length} selected)
          </label>
          <div className="relative">
            <details className="group">
              <summary className="w-full bg-dark border border-gray-700 rounded-lg px-4 py-2 text-text-primary cursor-pointer hover:border-purple transition-colors list-none flex items-center justify-between">
                <span>
                  {selectedCompetitors.length === 0
                    ? 'All competitors'
                    : `${selectedCompetitors.length} selected`}
                </span>
                <svg
                  className="w-4 h-4 text-text-secondary group-open:rotate-180 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </summary>
              <div className="absolute z-10 w-full mt-2 bg-dark border border-gray-700 rounded-lg shadow-xl max-h-60 overflow-y-auto">
                {competitors.map((competitor) => (
                  <label
                    key={competitor}
                    className="flex items-center px-4 py-2 hover:bg-darker cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={selectedCompetitors.includes(competitor)}
                      onChange={() => toggleCompetitor(competitor)}
                      className="mr-3 w-4 h-4 accent-purple"
                    />
                    <span className="text-text-primary text-sm">{competitor}</span>
                  </label>
                ))}
              </div>
            </details>
          </div>
        </div>

        {/* Source Filter */}
        <div>
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Sources ({selectedSources.length} selected)
          </label>
          <div className="relative">
            <details className="group">
              <summary className="w-full bg-dark border border-gray-700 rounded-lg px-4 py-2 text-text-primary cursor-pointer hover:border-purple transition-colors list-none flex items-center justify-between">
                <span>
                  {selectedSources.length === 0
                    ? 'All sources'
                    : `${selectedSources.length} selected`}
                </span>
                <svg
                  className="w-4 h-4 text-text-secondary group-open:rotate-180 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </summary>
              <div className="absolute z-10 w-full mt-2 bg-dark border border-gray-700 rounded-lg shadow-xl max-h-60 overflow-y-auto">
                {sources.map((source) => (
                  <label
                    key={source}
                    className="flex items-center px-4 py-2 hover:bg-darker cursor-pointer transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={selectedSources.includes(source)}
                      onChange={() => toggleSource(source)}
                      className="mr-3 w-4 h-4 accent-purple"
                    />
                    <span className="text-text-primary text-sm">{source}</span>
                  </label>
                ))}
              </div>
            </details>
          </div>
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <div className="flex flex-wrap gap-2">
            {selectedCompetitors.map((competitor) => (
              <span
                key={competitor}
                className="bg-purple/20 text-purple px-3 py-1 rounded-full text-xs font-medium flex items-center gap-2"
              >
                {competitor}
                <button
                  onClick={() => toggleCompetitor(competitor)}
                  className="hover:text-purple/80"
                >
                  ×
                </button>
              </span>
            ))}
            {selectedSources.map((source) => (
              <span
                key={source}
                className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-xs font-medium flex items-center gap-2"
              >
                {source}
                <button
                  onClick={() => toggleSource(source)}
                  className="hover:text-blue-400/80"
                >
                  ×
                </button>
              </span>
            ))}
            {timeRange !== 24 && (
              <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-xs font-medium">
                Last {timeRange < 24 ? `${timeRange}h` : `${timeRange / 24}d`}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
