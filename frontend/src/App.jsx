import { useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [latencyMs, setLatencyMs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  async function runSearch() {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const url = `${API_BASE}/search?q=${encodeURIComponent(query)}&k=10`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      const data = await response.json();
      setResults(data.results);
      setLatencyMs(data.latency_ms);
    } catch (err) {
      setError(err.message);
      setResults([]);
      setLatencyMs(null);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      runSearch();
    }
  }

  return (
    <div className="page">
      <header className="header">
        <h1 className="wordmark">search</h1>
        <div className="search-bar">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search the corpus..."
            className="search-input"
            autoFocus
          />
          <button onClick={runSearch} disabled={loading} className="search-button">
            {loading ? "Searching" : "Search"}
          </button>
        </div>

        {error && <p className="error-text">Something went wrong: {error}</p>}

        {latencyMs !== null && !error && (
          <p className="meta-line">
            {results.length} {results.length === 1 ? "result" : "results"} · {latencyMs} ms
          </p>
        )}
      </header>

      <main className="results">
        {hasSearched && !loading && results.length === 0 && !error && (
          <p className="empty-state">No matches found.</p>
        )}

        {results.map((r) => (
          <article key={r.doc_id} className="result-card">
            <h2 className="result-title">{r.title}</h2>
            <div className="result-meta">
              <span>#{r.doc_id}</span>
              {r.score !== null && <span>score {r.score.toFixed(2)}</span>}
            </div>
            <p
              className="result-snippet"
              dangerouslySetInnerHTML={{ __html: r.snippet }}
            />
          </article>
        ))}
      </main>
    </div>
  );
}

export default App;