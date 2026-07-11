# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## API + Frontend (Phase 6)

- FastAPI backend (search_engine/api/main.py): index + corpus loaded once at
  startup into memory (not per-request). CORS enabled for localhost:5173.
- GET /search?q=...&k=... dispatches to the unified search() from Phase 5,
  returns doc_id, score, title, snippet, and query latency_ms per request.
- Snippet highlighting (search_engine/api/snippet.py): re-stems each word of
  the raw doc text and compares against query terms (since the index vocab
  is stemmed but doc text is not), wraps matches in <mark> tags. Window
  widened from 8 to 18 words each side after initial version produced
  choppy, mid-sentence-cut excerpts.
- React frontend (Vite): single search page, calls /search on Enter or
  button click, renders ranked results with title/score/snippet.
  Initial UI pass used bright yellow highlights on a plain layout;
  redesigned to a dark theme with restrained indigo accent/highlight,
  card-style results, Inter + IBM Plex Mono typefaces.
- Manual end-to-end latency: ~120-150ms for standard BM25/boolean/phrase
  queries; fuzzy fallback queries remain slow (~9-10s, known limitation
  from Phase 5, full vocab scan) — acceptable for v1 demo purposes.
