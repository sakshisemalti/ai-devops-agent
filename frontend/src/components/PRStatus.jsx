import { useState } from "react";
import api from "../services/api";

export default function PRStatus() {
  const [directory, setDirectory] = useState("");
  const [branch, setBranch] = useState("ai-fix-" + Math.floor(Math.random() * 10000));
  const [title, setTitle] = useState("AI style fixes");
  const [body, setBody] = useState("Automated style fixes (tabs->spaces, ensure newline).");
  const [result, setResult] = useState(null);

  const runFixAndPR = async () => {
    try {
      const res = await api.post("/code/fix-and-pr", {
        directory: directory || "",   // allow empty for root
        branch,
        pr_title: title,
        pr_body: body,
      });
      setResult(res.data);
    } catch (e) {
      alert("Failed: " + (e.response?.data?.detail || e.message));
    }
  };

  return (
    <>
      <h2>AI Fix & Raise PR (GitHub)</h2>
      <input
        type="text"
        placeholder="repo directory (leave empty for root)"
        value={directory}
        onChange={(e) => setDirectory(e.target.value)}
      />
      <input
        type="text"
        placeholder="branch name"
        value={branch}
        onChange={(e) => setBranch(e.target.value)}
      />
      <input
        type="text"
        placeholder="PR title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        rows={3}
        placeholder="PR body"
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button onClick={runFixAndPR}>Fix & Create PR</button>

      {result && (
        <div style={{ marginTop: "1rem" }}>
          <p>Changed files: {result.changed_files}</p>
          {result.pr?.url ? (
            <p>
              PR: #{result.pr.number} —{" "}
              <a href={result.pr.url} target="_blank" rel="noreferrer">Open</a>
            </p>
          ) : (
            <p>No PR created (no changes)</p>
          )}
        </div>
      )}
    </>
  );
}
