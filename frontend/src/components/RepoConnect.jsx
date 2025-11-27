import { useState } from "react";
import api from "../services/api";

export default function RepoConnect() {
  const [repo, setRepo] = useState("");

  const connectRepo = async () => {
    if (!repo.includes("/")) {
      alert("Enter as username/repo");
      return;
    }
    try {
      const res = await api.post("/repo/connect", { repo_full_name: repo });
      alert(`Connected: ${res.data.repo}`);
    } catch (e) {
      alert("Failed to connect: " + (e.response?.data?.detail || e.message));
    }
  };

  return (
    <>
      <h2>Connect GitHub Repo</h2>
      <input
        type="text"
        placeholder="username/repo"
        value={repo}
        onChange={(e) => setRepo(e.target.value)}
      />
      <button onClick={connectRepo}>Connect</button>
    </>
  );
}
