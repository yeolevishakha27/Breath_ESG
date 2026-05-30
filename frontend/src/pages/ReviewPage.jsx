import { useEffect, useState } from "react";
import axios from "axios";

function ReviewPage() {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    const res = await axios.get(
      "https://breath-esg-backend-cx8m.onrender.com/api/review/"
    );

    setRecords(res.data);
  };

  const updateStatus = async (
    id,
    status
  ) => {
    await axios.post(
      `https://breath-esg-backend-cx8m.onrender.com/api/review/${id}/`,
      {
        status
      }
    );

    fetchRecords();
  };

  const filteredRecords =
    records.filter((record) =>
      record.fuel
        .toLowerCase()
        .includes(search.toLowerCase())
    );

  return (
    <div className="section">
      <h1>Review Queue</h1>

      <input
        className="search-box"
        placeholder="Search Fuel..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
      />

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Fuel</th>
              <th>Value</th>
              <th>Normalized</th>
              <th>Status</th>
              <th>Suspicious</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredRecords.map(
              (record) => (
                <tr
                  key={record.id}
                  className={
                    record.suspicious
                      ? "danger-row"
                      : ""
                  }
                >
                  <td>{record.id}</td>

                  <td>{record.fuel}</td>

                  <td>
                    {record.value}
                    {" "}
                    {record.unit}
                  </td>

                  <td>
                    {record.normalized_value}
                    {" "}
                    {
                      record.normalized_unit
                    }
                  </td>

                  <td>
                    <span className="status">
                      {record.status}
                    </span>
                  </td>

                  <td>
                    {record.suspicious
                      ? "⚠️ Yes"
                      : "✅ No"}
                  </td>

                  <td>
                    <button
                      className="approve-btn"
                      onClick={() =>
                        updateStatus(
                          record.id,
                          "APPROVED"
                        )
                      }
                    >
                      Approve
                    </button>

                    <button
                      className="reject-btn"
                      onClick={() =>
                        updateStatus(
                          record.id,
                          "REJECTED"
                        )
                      }
                    >
                      Reject
                    </button>
                  </td>
                </tr>
              )
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ReviewPage;