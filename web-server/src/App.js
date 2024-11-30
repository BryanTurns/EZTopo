import React, { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("No Upload");
  const [progress, setProgress] = useState(0);
  const [username, setUsername] = useState("Guest");

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
    formData.append("file", selectedFile);
    formData.append("username", username);

    fetch("http://localhost:5000/api/uploadVideo", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const uuid = data["uuid"];
        statusLoop(uuid, setStatus);
      })
      .catch((error) => {
        setStatus("Can't connect to server...");
        console.log("Failed to fetch uploadVideo: ", error);
      });
  };

  return (
    <div>
      <form>
        <input
          type="file"
          id="videoUploadID"
          name="videoUpload"
          onChange={(event) => handleFileChange(event)}
        ></input>
        <br></br>
        <br></br>
        <button type="button" onClick={() => handleFileUpload()}>
          Submit
        </button>
      </form>
      <p className="font-bold">Status: {status}</p>
    </div>
  );
}

async function statusLoop(uuid, setStatus) {
  var checkStatusBody = JSON.stringify({ uuid: uuid });
  while (true) {
    fetch("http://localhost:5000/api/checkStatus", {
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
        setStatus(translateStatus(data["status"]));
      })
      .catch((error) => {
        console.log("Can't connect to server: ", error);
        setStatus("Can't connect to server...");
      });
    await sleep(1000);
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
