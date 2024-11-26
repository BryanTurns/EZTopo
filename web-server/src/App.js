import React, { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState(0);

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

    const chunkSize = 5 * 1024; // 5MB (adjust based on your requirements)
    // const totalChunks = Math.ceil(selectedFile.size / chunkSize);
    const totalChunks = 1;
    const chunkProgress = 100 / totalChunks;
    let chunkNumber = 0;
    let start = 0;
    let end = chunkSize;

    while (chunkNumber < totalChunks) {
      if (end <= selectedFile.size) {
        const chunk = selectedFile.slice(start, end);
        const data = new FormData();
        data.append("file", chunk, "boulder.mp4");
        fetch("http://localhost:5000/api/uploadChunk", {
          method: "POST",
          body: data,
        })
          .then((res) => {
            console.log("success ", res);
            console.log("status", res.status);
            return res.json();
          })
          .then((data) => {
            console.log(data);
          })
          .catch((error) => {
            console.log("Fetch failed: ", error);
          });
        // var requestBody = {
        //   chunk: "",
        //   chunkNumber: chunkNumber,
        //   totalChunks: totalChunks,
        //   originalName: selectedFile.name,
        // };
        // chunk
        //   .arrayBuffer()
        //   .then((arrayBuffer) => {
        //     var base64String = _arrayBufferToBase64(arrayBuffer);
        //     requestBody["chunk"] = base64String;
        //     var request = axios
        //       .post("http://localhost:5000/api/uploadChunk", requestBody)
        //       .then((response) => {
        //         console.log(response.status);
        //       })
        //       .catch((error) => {
        //         console.log("Error in request: ", error);
        //       });
        //   })
        //   .catch((error) => {
        //     console.log("Error in arraybuffer: ", error);
        //   });
        console.log("Chunk " + chunkNumber + " uploaded.");
        chunkNumber++;
        start = end;
        end = start + chunkSize;
      } else {
        setProgress(100);
        setSelectedFile(null);
        setStatus("File upload completed");
        break;
      }
    }
  };

  return (
    <div>
      <form
      // onSubmit={() => {
      //   handleFileUpload();
      //   return false;
      // }}
      // method="POST"
      // action="http://localhost:5000/api/uploadChunk"
      >
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

function _arrayBufferToBase64(buffer) {
  var binary = "";
  var bytes = new Uint8Array(buffer);
  var len = bytes.byteLength;
  for (var i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}
