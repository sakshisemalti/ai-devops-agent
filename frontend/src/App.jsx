import RepoConnect from "./components/RepoConnect.jsx";
import CodeCheck from "./components/CodeCheck.jsx";
import PRStatus from "./components/PRStatus.jsx";

export default function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1 className="title">Autonomous DevOps Intelligence</h1>
        <p className="subtitle">Your intelligent automation assistant for code cleanup, GitHub commits, and seamless PR generation.</p>
      </header>

      <main className="grid">
        <div className="card glass">
          <RepoConnect />
        </div>
        <div className="card glass">
          <CodeCheck />
        </div>
        <div className="card glass">
          <PRStatus />
        </div>
      </main>
    </div>
  );
}
