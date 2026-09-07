const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "";

/**
 * fetch() cannot report upload progress, so a large video would sit at 0% for
 * minutes. XMLHttpRequest still exposes it.
 */
export function uploadVideo({ file, username, onProgress }) {
  return new Promise((resolve, reject) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("username", username);

    const request = new XMLHttpRequest();
    request.open("POST", `${API_BASE_URL}/api/uploadVideo`);

    request.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) onProgress(event.loaded / event.total);
    });

    request.addEventListener("load", () => {
      if (request.status < 200 || request.status >= 300) {
        reject(new Error(`The server rejected the upload (${request.status})`));
        return;
      }
      try {
        resolve(JSON.parse(request.responseText).uuid);
      } catch (error) {
        reject(new Error("The server sent a malformed response"));
      }
    });
    request.addEventListener("error", () =>
      reject(new Error("Could not reach the server")),
    );

    request.send(formData);
  });
}

export async function checkStatus(uuid) {
  const response = await fetch(`${API_BASE_URL}/api/checkStatus`, {
    method: "POST",
    body: JSON.stringify({ uuid: uuid }),
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Could not check status (${response.status})`);
  }
  const data = await response.json();
  return data.status;
}

export async function fetchOutputVideo(uuid) {
  const response = await fetch(`${API_BASE_URL}/api/getOutputVideo`, {
    method: "POST",
    body: JSON.stringify({ uuid: uuid }),
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Could not download your video (${response.status})`);
  }
  const blob = await response.blob();
  return URL.createObjectURL(blob);
}
