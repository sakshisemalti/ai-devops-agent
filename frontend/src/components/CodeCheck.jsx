import { useState } from "react";
import api from "../services/api";

export default function CodeCheck() {
  const [localPath, setLocalPath] = useState("");

  const runLint = async () => {
    if (!localPath) return alert("Enter a local path on the backend server");
    const res = await api.post("/code/check", { local_path: localPath });
    console.log(res.data);
    alert(`Issues: ${res.data.issues ? res.data.issues.length : 0}`);
  };

  const runFormat = async () => {
    if (!localPath) return alert("Enter a local path on the backend server");
    const res = await api.post("/code/format", { local_path: localPath });
    alert(res.data.status || res.data.error);
  };

  return (
    <>
      <h2>Local Lint & Format (Server Path)</h2>
      <input
        type="text"
        placeholder="/path/on/server/project"
        value={localPath}
        onChange={(e) => setLocalPath(e.target.value)}
      />
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button onClick={runLint}>Run Lint</button>
        <button onClick={runFormat}>Run Format</button>
      </div>
      <p style={{ opacity: 0.8 }}>
        Tip: Use this for local code directories mounted to the backend server.
      </p>
    </>
  );
}
