# EZTopo frontend

A React app built to static files and served by an existing web server — it is
not containerised. Run `npm install && npm run build`, then serve `build/` and
proxy `/api` to the backend. The root README has an nginx example.

`npm start` still works for development, but it needs the backend reachable at
the same origin or a `REACT_APP_API_BASE_URL` pointing at it.

## Layout

| File | Role |
| ---- | ---- |
| `src/App.js` | Screen composition and the upload → poll → download state machine |
| `src/api.js` | The three backend calls |
| `src/constants.js` | Pipeline steps, status codes, formatting helpers |
| `src/components/Dropzone.js` | Drag-and-drop / click-to-browse file picker |
| `src/components/ProgressSteps.js` | Per-stage progress list |
| `src/components/VideoStage.js` | Result player and download button |

## How it talks to the backend

Requests go to `${API_BASE_URL}/api/...`, where `API_BASE_URL` comes from
`REACT_APP_API_BASE_URL` at build time and defaults to empty — the same origin
that served the page.

A video is uploaded to `/api/uploadVideo` via `XMLHttpRequest` rather than
`fetch`, because only XHR reports upload progress and these files are large.
The returned UUID is then polled against `/api/checkStatus` once a second; the
integer that comes back drives the step list (see `STEPS` in `constants.js`, and
the status table in `backend/README.md`). Once it reaches 9 the finished video is
pulled from `/api/getOutputVideo` as a blob and played in place.

Transient poll failures are tolerated up to `MAX_CONSECUTIVE_POLL_FAILURES` so a
brief network blip does not discard a job the backend is still working on.
