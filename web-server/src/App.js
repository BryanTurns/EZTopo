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

  const handleFileUpload = () => {
    console.log("UPLOADING!");
    if (!selectedFile) {
      alert("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("username", username);

    const response = fetch("http://localhost:5000/api/uploadVideo", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const uuid = data["uuid"];
        console.log(uuid);
      })
      .catch((error) => {
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
