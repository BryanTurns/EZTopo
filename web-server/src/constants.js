export const STATUS_DONE = 9;
// The browser knows it is uploading before the backend has been asked anything,
// so the first step is driven locally rather than by a poll.
export const STATUS_UPLOADING = 2;

/**
 * The backend reports an integer per pipeline stage (see backend/README.md).
 * Each step below owns the pair of codes for "started" and "finished".
 */
export const STEPS = [
  { label: "Uploading your video", from: 2, to: 3 },
  { label: "Splitting it into frames", from: 4, to: 5 },
  { label: "Estimating body positions", from: 6, to: 7 },
  { label: "Drawing your path", from: 8, to: 9 },
];

export function stepState(step, status) {
  if (status === null || status < step.from) return "pending";
  if (status > step.to) return "done";
  return step.to === STATUS_DONE && status === STATUS_DONE ? "done" : "active";
}

export function formatBytes(bytes) {
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
