import { useState } from "react";
import axios from "axios";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      const res = await axios.post(
        "https://breath-esg-backend-cx8m.onrender.com/api/upload/sap/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      setResponse(res.data);
    } catch (error) {
      console.error(error);
      alert("Upload Failed");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>ESG SAP Upload</h1>

      <input
        type="file"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br />
      <br />

      <button onClick={handleUpload}>
        Upload CSV
      </button>

      {response && (
        <div className="upload-card">
          <h3>✅ Upload Successful</h3>

          <p>
            Rows Processed:
            {response.rows_read}
          </p>

          <p>
            Records Created:
            {response.records_created}
          </p>

          <p>
            Suspicious Records:
            {response.suspicious_records}
          </p>
        </div>
      )}
    </div>
  );
}

export default UploadPage;