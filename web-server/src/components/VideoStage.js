import React from "react";

export default function VideoStage({ outputURL }) {
  return (
    <section className="flex min-h-0 flex-1 flex-col bg-zinc-900 lg:w-1/2 lg:min-w-0 lg:flex-none">
      <header className="flex items-center justify-between gap-4 border-b border-white/10 px-6 py-4">
        <h2 className="text-sm font-medium text-zinc-300">
          {outputURL === null ? "Example result" : "Your traced path"}
        </h2>
        {outputURL !== null && (
          <a
            href={outputURL}
            download="eztopo.mp4"
            className="rounded-lg bg-white/10 px-3 py-2 text-sm font-medium text-white hover:bg-white/20"
          >
            Download
          </a>
        )}
      </header>

      <div className="flex min-h-0 flex-1 items-center justify-center p-4 sm:p-6">
        {outputURL === null ? (
          <video
            className="max-h-[55vh] w-full rounded-lg object-contain lg:max-h-full"
            controls
            playsInline
          >
            <source src="outdoors.mp4" />
          </video>
        ) : (
          <video
            key={outputURL}
            className="max-h-[55vh] w-full rounded-lg object-contain lg:max-h-full"
            controls
            autoPlay
            playsInline
          >
            <source type="video/mp4" src={outputURL} />
          </video>
        )}
      </div>
    </section>
  );
}
