import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("No Upload");
  const [progress, setProgress] = useState(0);
  const [username, setUsername] = useState("Guest");
  const [outputURL, setOutputURL] = useState(null);

  // const videoPlayer = document.getElementById("videoPlayer");
  // useEffect(() => {
  //   videoPlayer.current.reload();
  // }, [outputURL]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleFileUpload = () => {
    setStatus("Initiating upload..");
    console.log("UPLOADING!");
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    var uuid;
    formData.append("file", selectedFile);
    formData.append("username", username);

    fetch("http://localhost:80/api/uploadVideo", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        uuid = data["uuid"];
        waitForProcessingFinish(uuid, setStatus).then(() => {
          setStatus("Retrieving your video...");
          downloadVideo(uuid, setOutputURL);
          setStatus("Complete!");
        });
      })
      .catch((error) => {
        setStatus("Can't connect to server...");
        console.log("Failed to fetch uploadVideo: ", error);
      });
  };

  return (
    <div className="grid grid-cols-2 grid-rows-12 h-screen max-h-screen">
      <h1 className="col-span-1 col-start-1 sm:row-span-2 xl:row-span-1 row-start-1 text-3xl font-semibold border-b-4 border-r-2 p-2 border-black bg-stone-200">
        Auto-draw your climbing path!
      </h1>
      <div className="p-4 col-span-1 col-start-1 sm:row-start-3 xl:row-start-2 row-span-12 border-r-2 border-black bg-stone-200 ">
        <form className="">
          <h2 className="text-lg">Upload your video for processing:</h2>
          <input
            type="file"
            id="videoUploadID"
            name="videoUpload"
            onChange={(event) => handleFileChange(event)}
            accept="video/*"
            className="mx-4 my-4 block"
          ></input>

          <button
            className="py-1 px-3 mx-4 my-4 border-4 hover:bg-zinc-100 border-stone-700  rounded-lg font-semibold bg-zinc-300 block "
            type="button"
            onClick={() => handleFileUpload()}
          >
            Upload
          </button>
        </form>
        <p className="my-8 font-bold">Status: {status}</p>
      </div>
      <h1 className="col-span-1 col-start-2 row-start-1 sm:row-span-2 xl:row-span-1 font-semibold text-3xl border-b-4 p-2 border-black bg-stone-400">
        {outputURL == null ? "Example Video:" : "Your Video:"}
      </h1>
      <div className="col-span-1 col-start-2 sm:row-start-3 xl:row-start-2 row-span-12 max-h-full justify-items-center  bg-stone-400 ">
        {outputURL == null ? (
          <video id="videoPlayer" className="max-h-full" controls>
            <source src="outdoors.mp4"></source>
          </video>
        ) : (
          <video className="max-h-full" key={outputURL} controls autoPlay>
            <source type="video/mp4" src={outputURL} />
          </video>
        )}
      </div>
    </div>
  );
}

async function waitForProcessingFinish(uuid, setStatus) {
  var checkStatusBody = JSON.stringify({ uuid: uuid });
  var dataBeingProcessed = true;
  while (dataBeingProcessed) {
    fetch("http://localhost:80/api/checkStatus", {
      method: "POST",
      body: checkStatusBody,
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data["status"] == 9) dataBeingProcessed = false;
        setStatus(translateStatus(data["status"]));
      })
      .catch((error) => {
        console.log("Can't connect to server: ", error);
        setStatus("Can't connect to server...");
      });
    if (dataBeingProcessed) await sleep(1000);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function translateStatus(status) {
  switch (status) {
    case 2:
      return "Uploading to main server...";
    case 3:
      return "Uploaded to main server!";
    case 4:
      return "Splitting your video into chunks...";
    case 5:
      return "Your video is split!";
    case 6:
      return "Running your frames through our model...";
    case 7:
      return "Your body positions have been estimated!";
    case 8:
      return "Drawing your path onto the original video...";
    case 9:
      return "Your path has been drawn!";
  }
}
export default App;

function downloadVideo(uuid, setOutputURL) {
  fetch("http://localhost:80/api/getOutputVideo", {
    method: "POST",
    body: JSON.stringify({ uuid: uuid }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      console.log(response);
      // var responseStream = response.body;
      return response.blob();
      // fs.writeFile("test.mp4", responseStream);
    })
    .then((blob) => {
      console.log(blob);
      const url = URL.createObjectURL(blob);
      setOutputURL(url);
      console.log(url);
    })
    .catch((error) => {
      console.log(error);
    });
}

// async function uploadChunk(selectedFile, start, end, chunkNumber, uuid) {
//   const chunk = selectedFile.slice(start, end);
//   const data = new FormData();
//   data.append("file", chunk, selectedFile.name);
//   data.append("chunkNumber", chunkNumber);
//   data.append("uuid", uuid);
//   fetch("http://localhost:5000/api/uploadChunk", {
//     method: "POST",
//     body: data,
//   })
//     .then((res) => {
//       if (!res.ok) {
//         throw new Error("Sending chunk failed (" + res.status + ")");
//       }
//     })
//     .catch((error) => {
//       console.log("Fetch failed: ", error);
//     });
// }
