import React from "react";
import { STEPS, stepState } from "../constants";

export default function ProgressSteps({ status, uploadFraction }) {
  return (
    <ol className="space-y-3">
      {STEPS.map((step, index) => {
        const state = stepState(step, status);
        // Only the upload step can report real progress; the rest are opaque
        // server-side work, so they just show as active.
        const showFraction = index === 0 && state === "active";
        return (
          <li key={step.label} className="flex items-center gap-3">
            <StepMarker state={state} />
            <span
              className={`text-sm ${
                state === "pending"
                  ? "text-zinc-400"
                  : state === "active"
                    ? "font-medium text-zinc-900"
                    : "text-zinc-500"
              }`}
            >
              {step.label}
              {showFraction && ` — ${Math.round(uploadFraction * 100)}%`}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

function StepMarker({ state }) {
  if (state === "done") {
    return (
      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-emerald-600">
        <svg
          className="h-3 w-3 text-white"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M5 13l4 4L19 7" />
        </svg>
      </span>
    );
  }
  if (state === "active") {
    return (
      <span className="h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-900" />
    );
  }
  return (
    <span className="h-5 w-5 shrink-0 rounded-full border-2 border-zinc-200" />
  );
}
