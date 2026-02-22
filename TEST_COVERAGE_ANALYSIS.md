# Test Coverage Analysis

## Executive Summary

The current test suite consists of **4 Python scripts** that serve as integration/connectivity checks against live services. There are **no unit tests, no frontend tests, and no test framework integration** despite `pytest` being listed in `requirements.txt`. The effective unit-test coverage of business logic is **0%**.

---

## Current State of Tests

### What Exists

| File | Type | What It Does |
|------|------|-------------|
| `tools/test_newsdata_api.py` | Integration check | Hits the live NewsData.io API, prints results |
| `tools/test_rss_feeds.py` | Integration check | Fetches live RSS feeds, prints results |
| `tools/test_supabase.py` | Integration check | Performs CRUD on live Supabase database |
| `tools/test_all_connections.py` | Orchestrator | Runs the above three scripts via subprocess |

### What's Wrong With the Current Tests

1. **Not real tests** - They use `print()` and `sys.exit(1)` instead of assertions. No test framework (pytest, unittest) is used despite `pytest==7.4.0` being in `requirements.txt`.
2. **Require live services** - Every test hits real external APIs and databases. They can't run in CI without credentials and network access, and they consume API rate limits.
3. **No isolation** - No mocking or stubbing. A single network hiccup fails the entire suite.
4. **No business logic coverage** - The core functions (`detect_competitors`, `parse_timestamp`, `normalize_article`, `store_articles`) are never tested in isolation.
5. **No frontend tests at all** - Zero test files exist for the Next.js dashboard (no Jest, no React Testing Library, no Playwright/Cypress).

---

## Coverage Gaps by Area

### 1. Python Scraper Unit Tests (HIGH PRIORITY)

Both `scrape_newsdata.py` and `scrape_rss.py` contain pure functions that can be tested without any external services:

#### `detect_competitors()` - Both scrapers
- **Current coverage: 0%**
- Should test: single competitor match, multiple matches, no matches, case insensitivity, partial word matching (e.g. "ledgerman" should not match "ledger"), empty/null fields

#### `parse_timestamp()` - Both scrapers
- **Current coverage: 0%**
- Should test: valid ISO format, various timezone formats, naive datetimes, `None` input, malformed strings, edge cases like epoch timestamps

#### `normalize_article()` - Both scrapers
- **Current coverage: 0%**
- Should test: complete article data, missing optional fields (`author`, `image_url`, `description`), `None` values in nested fields (e.g. `creator` list in NewsData), content extraction from RSS `content` vs `summary` fallback

#### `article_exists()` - Both scrapers
- **Current coverage: 0%**
- Should test with mocked Supabase client: article found, article not found, database error returns `False`

#### `store_articles()` - Both scrapers
- **Current coverage: 0%**
- Should test with mocked Supabase: successful insert, duplicate skipping, error handling, stats accumulation

#### `fetch_articles()` - Both scrapers
- **Current coverage: 0%**
- Should test with mocked HTTP responses: successful fetch, API error response, network timeout, rate limit (429), time window filtering

### 2. Frontend Utility Tests (HIGH PRIORITY)

#### `lib/supabase.ts` - `timeAgo()`
- **Current coverage: 0%**
- Pure function, trivially testable
- Should test: seconds ago, minutes ago, hours ago, days ago, weeks ago, months ago, years ago, "just now" for very recent dates, future dates

#### `lib/supabase.ts` - `fetchArticles()`
- **Current coverage: 0%**
- Should test with mocked Supabase client: no filters, time filter, competitor filter, source filter, custom limit, default limit of 100, error handling

#### `lib/supabase.ts` - `getFilters()`
- **Current coverage: 0%**
- Should test with mocked Supabase: deduplication logic, sorting, error returns empty arrays

### 3. API Route Tests (MEDIUM PRIORITY)

#### `app/api/scrape/route.ts`
- **Current coverage: 0%**
- Contains branching auth logic and multiple trigger mechanisms
- Should test: unauthorized request returns 401, GitHub Actions trigger path, webhook trigger path, no-config returns 501, error handling returns 500, POST delegates to GET

### 4. React Component Tests (MEDIUM PRIORITY)

#### `FilterBar.tsx` (213 lines - most complex component)
- **Current coverage: 0%**
- Contains significant interactive logic: toggling competitors/sources, time range selection, clear all filters, active filter display
- Should test: initial render, toggling a competitor filter, toggling a source filter, changing time range, clear all resets state, `onFilterChange` callback fires with correct values

#### `SaveButton.tsx` (82 lines - Supabase interaction)
- **Current coverage: 0%**
- Contains async save/unsave logic with error handling
- Should test: initial unsaved state, clicking save triggers insert, clicking unsaved triggers delete, loading state disables button, error shows alert, duplicate key error is ignored

#### `ArticleCard.tsx` (105 lines)
- **Current coverage: 0%**
- Should test: renders title/source/date, competitor badges display, external link behavior, truncation of long titles

#### `ArticleGrid.tsx` (82 lines)
- **Current coverage: 0%**
- Should test: renders list of articles, empty state, client-side filtering

### 5. End-to-End / Integration Tests (LOW PRIORITY - FUTURE)

No E2E test framework is set up. Playwright is in `requirements.txt` but only for Python web scraping, not for testing the dashboard.

- Full scrape-to-display pipeline
- Filter interactions on the live dashboard
- Save/unsave flow persistence

---

## Recommended Action Plan

### Phase 1: Python unit tests with pytest (highest impact)

Set up `pytest` properly with a `conftest.py` and write isolated unit tests for both scrapers. Use `unittest.mock` to stub Supabase and HTTP calls.

**Files to create:**
- `tools/tests/conftest.py` - Shared fixtures (mock Supabase client, sample article data)
- `tools/tests/test_detect_competitors.py` - Competitor detection logic
- `tools/tests/test_parse_timestamp.py` - Timestamp parsing
- `tools/tests/test_normalize_article.py` - Article normalization for both scrapers
- `tools/tests/test_store_articles.py` - Storage with mocked DB
- `tools/tests/test_fetch_articles.py` - API fetching with mocked HTTP

**Estimated test count: ~40-50 test cases**

### Phase 2: Frontend utility + API route tests

Install Jest + React Testing Library. Write tests for pure utility functions first, then the API route.

**Setup needed:**
- Install `jest`, `@testing-library/react`, `@testing-library/jest-dom`, `ts-jest`
- Create `jest.config.ts` in `dashboard/`

**Files to create:**
- `dashboard/__tests__/lib/supabase.test.ts` - `timeAgo`, `fetchArticles`, `getFilters`
- `dashboard/__tests__/api/scrape.test.ts` - API route handler

**Estimated test count: ~25-30 test cases**

### Phase 3: React component tests

Test interactive components with React Testing Library.

**Files to create:**
- `dashboard/__tests__/components/FilterBar.test.tsx`
- `dashboard/__tests__/components/SaveButton.test.tsx`
- `dashboard/__tests__/components/ArticleCard.test.tsx`

**Estimated test count: ~20-25 test cases**

---

## Specific Bugs Likely Caught by Proper Tests

1. **False positive competitor detection** - `detect_competitors()` uses simple substring matching (`competitor in text`). The word "ledgerman" or "metamasked" would incorrectly match. Tests would expose this and motivate word-boundary matching.

2. **`parse_timestamp()` silent failures** - The bare `except:` clause on line 96 of `scrape_newsdata.py` (and line 107 of `scrape_rss.py`) silently swallows all parsing errors and returns `now()`. Malformed dates get stored as the current time with no indication of the error.

3. **`normalize_article()` crash on null `creator`** - In `scrape_newsdata.py:139`, `raw_article.get("creator", [None])[0]` will crash with `IndexError` if `creator` is an empty list `[]`.

4. **`timeAgo()` returns "just now" for future dates** - The function doesn't handle dates in the future, which could happen with timezone mismatches.

5. **Supabase client with placeholder credentials** - `lib/supabase.ts:8-9` creates a client with `'https://placeholder.supabase.co'` and `'placeholder-key'` when env vars are missing. This silently produces a broken client instead of failing fast.
