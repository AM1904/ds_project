# Running the web app

The backend is Flask (`web_server.py`, SQLite in `portal_data.db`). The UI is a React + TypeScript + Vite app in `frontend/`. Flask serves the built UI from `frontend/dist`.

## Prerequisites

- Python 3.10+ and Node.js 20+ (Node is needed once, to build the UI)
- From the repo root: `pip install -r requirements.txt`

## Run it (one command)

```bash
python run_web.py
```

Open http://localhost:5050. On the first run it installs the frontend packages and builds the UI automatically. Stop with Ctrl+C.

## Run Flask only (after the UI is built)

```bash
python web_server.py
```

If the UI has not been built, the page shows "Frontend not built". Build it as below.

## Build the UI by hand

```bash
cd frontend
npm install
npm run build        # type-checks, then writes frontend/dist
```

Rebuild after any change in `frontend/src`, then refresh the page (Flask serves `frontend/dist`).

## Frontend development (hot reload)

Use two terminals.

```bash
# terminal 1, repo root: API on :5050
python web_server.py

# terminal 2: UI on :5173, forwards /api to Flask
cd frontend
npm run dev
```

Open http://localhost:5173. To point the UI at a different API port:

```bash
# macOS / Linux / Git Bash
API_TARGET=http://localhost:5051 npm run dev
# PowerShell
$env:API_TARGET="http://localhost:5051"; npm run dev
```

## Other commands

| Command (run in `frontend/`) | What it does |
|---|---|
| `npm run typecheck` | TypeScript check, no output files |
| `npm run build` | Type-check, then production build into `dist/` |
| `npm run preview` | Serve the built `dist/` locally with Vite |

Run Flask on another port (the port is read from `PORT`):

```bash
# macOS / Linux / Git Bash
PORT=5051 python web_server.py
# PowerShell
$env:PORT=5051; python web_server.py
```

`run_web.py` always uses port 5050.

## Demo accounts

Click one on the sign-in page, or type the credentials.

| Role | Email | Password |
|---|---|---|
| Admin | `admin@college.edu` | `admin123` |
| Teacher | `ananya@college.edu`, `ravi.k@college.edu`, `priya.nair@college.edu` | `faculty123` |
| Student | `student.a@college.edu` (MCA A), `student.b@college.edu` (MCA B) | `student123` |

The two student accounts are created the first time you use them from the sign-in page.

## Troubleshooting

- **"Frontend not built" (HTTP 503):** run `cd frontend && npm install && npm run build`.
- **Port 5050 already in use:** stop the other process, or run `PORT=5051 python web_server.py`.
- **Blank page after changing the UI:** rebuild with `npm run build` and hard-refresh (Ctrl+F5).
- **Sign-in says it cannot reach the server:** Flask is not running; start `python web_server.py`.
- **Past days cannot be edited:** by design. Days before today are read-only.
