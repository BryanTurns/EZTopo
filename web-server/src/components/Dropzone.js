import React, { useEffect, useRef, useState } from "react";
import { formatBytes } from "../constants";

export default function Dropzone({ file, onSelect, onClear, disabled }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isPreparing, setIsPreparing] = useState(false);

  // iOS only fires "change" once it has exported the clip out of the photo
  // library, which takes seconds for a long video. Nothing tells us a file was
  // picked before that, so we swap the picker out as soon as it opens and show
  // that we are waiting. "cancel" tells us the picker was dismissed instead.
  useEffect(() => {
    const input = inputRef.current;
    const handleCancel = () => setIsPreparing(false);
    input.addEventListener("cancel", handleCancel);
    return () => input.removeEventListener("cancel", handleCancel);
  }, []);

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    const dropped = event.dataTransfer.files[0];
    if (dropped) onSelect(dropped);
  }

  return (
    <>
      {/* Kept mounted in every state: unmounting it while the native picker is
          open would lose the change event the picker eventually fires. */}
      <input
        ref={inputRef}
        type="file"
        accept="video/*"
        className="hidden"
        onChange={(event) => {
          const selected = event.target.files[0];
          setIsPreparing(false);
          if (selected) onSelect(selected);
          event.target.value = "";
        }}
      />
      {renderState()}
    </>
  );

  function renderState() {
    if (file) {
      return (
        <div className="flex items-center gap-3 rounded-xl border border-zinc-200 bg-white p-4">
          <FilmIcon className="h-5 w-5 shrink-0 text-zinc-400" />
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-zinc-900">
              {file.name}
            </p>
            <p className="text-xs text-zinc-500">{formatBytes(file.size)}</p>
          </div>
          <button
            type="button"
            onClick={onClear}
            disabled={disabled}
            aria-label="Remove selected video"
            className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-900 disabled:pointer-events-none disabled:opacity-40"
          >
            <XIcon className="h-4 w-4" />
          </button>
        </div>
      );
    }

    if (isPreparing) {
      return (
        <div className="flex items-center gap-3 rounded-xl border border-zinc-200 bg-white p-4">
          <span className="h-5 w-5 shrink-0 animate-spin rounded-full border-2 border-zinc-200 border-t-zinc-900" />
          <div className="min-w-0 flex-1">
            <p className="text-sm font-medium text-zinc-900">
              Preparing your video...
            </p>
            <p className="text-xs text-zinc-500">
              Large clips can take a moment to export.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setIsPreparing(false)}
            className="rounded-lg px-3 py-2 text-sm font-medium text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900"
          >
            Cancel
          </button>
        </div>
      );
    }

    return (
      <button
        type="button"
        onClick={() => {
          setIsPreparing(true);
          inputRef.current.click();
        }}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        disabled={disabled}
        className={`flex w-full flex-col items-center gap-2 rounded-xl border-2 border-dashed px-6 py-10 text-center outline-none focus-visible:ring-2 focus-visible:ring-zinc-900 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
          isDragging
            ? "border-zinc-900 bg-zinc-100"
            : "border-zinc-300 bg-white hover:border-zinc-400 hover:bg-zinc-50"
        }`}
      >
        <UploadIcon className="h-6 w-6 text-zinc-400" />
        <span className="text-sm font-medium text-zinc-900">
          Drop a video here, or <span className="underline">browse</span>
        </span>
        <span className="text-xs text-zinc-500">MP4, up to 1 GB</span>
      </button>
    );
  }
}

function UploadIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5" />
      <path d="M4 16v2.5A1.5 1.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V16" />
    </svg>
  );
}

function FilmIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="M3 10h18M8 5v14M16 5v14" />
    </svg>
  );
}

function XIcon({ className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  );
}
