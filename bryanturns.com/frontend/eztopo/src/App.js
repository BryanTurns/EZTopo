import styles from "./index.css"

function App() {
  return (
  <div className="grid grid-cols-2 grid-rows-12 h-screen max-h-screen">
      <h1 className="col-span-1 col-start-1 sm:row-span-2 xl:row-span-1 row-start-1 text-3xl font-semibold border-b-4 border-r-2 p-2 border-black bg-stone-200">
        Auto-draw your climbing path!
      </h1>
      <div className="p-4 col-span-1 col-start-1 sm:row-start-3 xl:row-start-2 row-span-12 border-r-2 border-black bg-stone-200 ">
        <form className="">
          <h2 className="text-lg font-medium">
            Upload your video for processing:
          </h2>
          <input
            type="file"
            id="videoUploadID"
            name="videoUpload"
            accept="video/*"
            className="mx-4 my-4 block"
          ></input>

          <button
            className="py-1 px-3 mx-4 my-4 border-4 hover:bg-zinc-100 border-stone-700  rounded-lg font-semibold bg-zinc-300 block "
            type="button"
          >
            Upload
          </button>
        </form>
        <p className="mt-8 font-bold">Status: </p>
        <p>
          Note: Currently the AI only tracks the person with the highest hip
          position in the frame
        </p>
      </div>
      <h1 className="col-span-1 col-start-2 row-start-1 sm:row-span-2 xl:row-span-1 font-semibold text-3xl border-b-4 p-2 border-black bg-stone-400">
      </h1>
      <div className="col-span-1 col-start-2 sm:row-start-3 xl:row-start-2 row-span-12 max-h-full justify-items-center  bg-stone-400 ">
        <video id="videoPlayer" className="max-h-full" controls>
          <source src="videos/outdoors.mp4"></source>
        </video>
      </div>
    </div>
  );
}

export default App;
