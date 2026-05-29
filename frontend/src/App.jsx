import UploadPage from "./pages/UploadPage";
import Dashboard from "./pages/Dashboard";
import ReviewPage from "./pages/ReviewPage";

function App() {
  return (
    <div>
      <nav className="navbar">
        <div>
          <h1>Breathe ESG Platform</h1>
          <p>Carbon Data Ingestion & Review System</p>
        </div>

        <div>
          <span className="badge">SAP</span>
          <span className="badge">CSV</span>
          <span className="badge">ESG</span>
        </div>
      </nav>

      <UploadPage />

      <Dashboard />

      <ReviewPage />

      <footer className="footer">
        Built by Vishakha Yeole | Breathe ESG Assignment
      </footer>
    </div>
  );
}

export default App;