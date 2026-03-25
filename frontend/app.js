const backendBase = "http://localhost:8000/api";

const statusEl = document.getElementById("status");
const outputEl = document.getElementById("output");

function setStatus(text, type = "info") {
  statusEl.className = `alert alert-${type}`;
  statusEl.textContent = text;
  statusEl.classList.remove("d-none");
}

function setOutput(data) {
  outputEl.textContent = JSON.stringify(data, null, 2);
}

async function upload(kind) {
  const inputEl = kind === "audio" ? document.getElementById("audioInput") : document.getElementById("videoInput");
  const file = inputEl.files[0];

  if (!file) {
    setStatus(`Choose a ${kind} file first`, "warning");
    return;
  }

  setStatus(`Uploading ${file.name}...`, "info");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${backendBase}/upload/${kind}`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.detail || "Upload failed");
    }

    setStatus("Analysis complete", "success");
    setOutput(result);
  } catch (error) {
    setStatus(`Error: ${error.message}`, "danger");
    setOutput({ error: error.message });
  }
}

document.getElementById("audioUploadBtn").addEventListener("click", () => upload("audio"));
document.getElementById("videoUploadBtn").addEventListener("click", () => upload("video"));
