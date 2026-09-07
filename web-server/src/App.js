import React, { useCallback, useEffect, useRef, useState } from "react";
import Dropzone from "./components/Dropzone";
import ProgressSteps from "./components/ProgressSteps";
import VideoStage from "./components/VideoStage";
import { checkStatus, fetchOutputVideo, uploadVideo } from "./api";
import { STATUS_DONE, STATUS_UPLOADING } from "./constants";

const POLL_INTERVAL_MS = 1000;
// A blip on the network shouldn't throw away a job the server is still running.
const MAX_CONSECUTIVE_POLL_FAILURES = 5;

export default function App() {
  const [file, setFile] = useState(null);
  const [phase, setPhase] = useState("idle");
  const [status, setStatus] = useState(null);
  const [uploadFraction, setUploadFraction] = useState(0);
  const [outputURL, setOutputURL] = useState(null);
  const [error, setError] = useState(null);

  const outputURLRef = useRef(null);
  const abandonedRef = useRef(false);

  useEffect(() => {
    return () => {
      abandonedRef.current = true;
      if (outputURLRef.current) URL.revokeObjectURL(outputURLRef.current);
    };
  }, []);

  const showOutput = useCallback((url) => {
    if (outputURLRef.current) URL.revokeObjectURL(outputURLRef.current);
    outputURLRef.current = url;
    setOutputURL(url);
  }, []);

  const isBusy = phase === "uploading" || phase === "processing";

  async function handleUpload() {
    if (!file || isBusy) return;

    abandonedRef.current = false;
    setError(null);
    setStatus(STATUS_UPLOADING);
    setUploadFraction(0);
    showOutput(null);
    setPhase("uploading");

    try {
      const uuid = await uploadVideo({
        file: file,
        username: "Guest",
        onProgress: setUploadFraction,
      });
      setPhase("processing");

      await waitForCompletion(uuid);
      if (abandonedRef.current) return;

      const url = await fetchOutputVideo(uuid);
      if (abandonedRef.current) {
        URL.revokeObjectURL(url);
        return;
      }
      showOutput(url);
      setPhase("done");
    } catch (caught) {
      if (abandonedRef.current) return;
      setError(caught.message);
      setPhase("error");
    }
  }

  async function waitForCompletion(uuid) {
    let consecutiveFailures = 0;
    while (!abandonedRef.current) {
      try {
        const current = await checkStatus(uuid);
        consecutiveFailures = 0;
        setStatus(current);
        if (current === STATUS_DONE) return;
      } catch (caught) {
        consecutiveFailures += 1;
        if (consecutiveFailures >= MAX_CONSECUTIVE_POLL_FAILURES) throw caught;
      }
      await sleep(POLL_INTERVAL_MS);
    }
  }

  function handleReset() {
    setFile(null);
    setStatus(null);
    setUploadFraction(0);
    setError(null);
    setPhase("idle");
  }

  return (
    <div className="flex min-h-dvh flex-col bg-zinc-50 text-zinc-900 lg:h-dvh lg:flex-row lg:overflow-hidden">
      <section className="flex flex-col border-b border-zinc-200 lg:w-1/2 lg:min-w-0 lg:overflow-y-auto lg:border-b-0 lg:border-r">
        <div className="mx-auto w-full max-w-md px-6 py-8 sm:px-8">
          <header className="mb-6">
            <div className="flex items-center gap-3">
              <img
                src={`${process.env.PUBLIC_URL}/logo192.png`}
                alt=""
                className="h-9 w-9 sm:h-10 sm:w-10"
              />
              <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                EZTopo
              </h1>
            </div>
            <p className="mt-1 text-sm text-zinc-500">
              Upload a climbing video and get your path traced onto it.
            </p>
          </header>

          <div className="flex flex-col gap-6">
            <Dropzone
              file={file}
              onSelect={setFile}
              onClear={() => setFile(null)}
              disabled={isBusy}
            />

            {phase === "done" ? (
              <button
                type="button"
                onClick={handleReset}
                className="w-full rounded-xl border border-zinc-300 bg-white px-5 py-3 text-sm font-medium hover:bg-zinc-100"
              >
                Trace another video
              </button>
            ) : (
              <button
                type="button"
                onClick={handleUpload}
                disabled={!file || isBusy}
                className="w-full rounded-xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white hover:bg-zinc-800 disabled:cursor-not-allowed disabled:bg-zinc-300"
              >
                {isBusy ? "Working..." : "Trace my path"}
              </button>
            )}

            {(isBusy || phase === "done") && (
              <div className="rounded-xl border border-zinc-200 bg-white p-5">
                <ProgressSteps
                  status={status}
                  uploadFraction={uploadFraction}
                />
              </div>
            )}

            {error !== null && (
              <div
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
              >
                {error}
              </div>
            )}

            <p className="text-xs leading-relaxed text-zinc-500">
              The model tracks the person with the highest hip position in each
              frame, so the climber is followed rather than the belayer.
            </p>
          </div>
        </div>
      </section>

      <VideoStage outputURL={outputURL} />
    </div>
  );
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
