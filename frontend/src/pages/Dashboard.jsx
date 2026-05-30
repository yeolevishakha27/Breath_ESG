import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const res = await axios.get(
      "https://breath-esg-backend-cx8m.onrender.com/api/review/"
    );

    setRecords(res.data);
  };

  const approved = records.filter(
    (r) => r.status === "APPROVED"
  ).length;

  const rejected = records.filter(
    (r) => r.status === "REJECTED"
  ).length;

  const suspicious = records.filter(
    (r) => r.suspicious
  ).length;

  return (
    <div className="section">
      <h1>Dashboard</h1>

      <div className="cards">
        <div className="card">
          <h2>{records.length}</h2>
          <p>Total Records</p>
        </div>

        <div className="card">
          <h2>{approved}</h2>
          <p>Approved</p>
        </div>

        <div className="card">
          <h2>{rejected}</h2>
          <p>Rejected</p>
        </div>

        <div className="card">
          <h2>{suspicious}</h2>
          <p>Suspicious</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;