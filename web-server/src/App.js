import React, { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [username, setUsername] = useState("Guest");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleFileUpload = async () => {
    console.log("UPLOADING!");
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const data = {
      username: username,
    };
    const response = await fetch("http://localhost:5000/api/startUpload", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    const responseJson = await response.json();
    const uuid = responseJson["uuid"];

    const chunkSize = 5 * 1024 * 1024; // 5MB (adjust based on your requirements)
    const totalChunks = Math.ceil(selectedFile.size / chunkSize);
    const chunkProgress = 100 / totalChunks;
    let chunkNumber = 0;
    let start = 0;
    let end = chunkSize;

    while (chunkNumber < totalChunks) {
      if (end <= selectedFile.size) {
        uploadChunk(selectedFile, start, end, chunkNumber, uuid);
        chunkNumber++;
        start = end;
        end = start + chunkSize;
      } else {
        uploadChunk(selectedFile, start, end, chunkNumber, uuid);

        setProgress(100);
        setSelectedFile(null);
        setStatus("File upload completed");
        break;
      }
    }
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
    </div>
  );
}

export default App;

async function uploadChunk(selectedFile, start, end, chunkNumber, uuid) {
  const chunk = selectedFile.slice(start, end);
  const data = new FormData();
  data.append("file", chunk, selectedFile.name);
  data.append("chunkNumber", chunkNumber);
  data.append("uuid", uuid);
  fetch("http://localhost:5000/api/uploadChunk", {
    method: "POST",
    body: data,
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Sending chunk failed (" + res.status + ")");
      }
    })
    .catch((error) => {
      console.log("Fetch failed: ", error);
    });
}
