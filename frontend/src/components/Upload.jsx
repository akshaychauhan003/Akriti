import axios from "axios";
import { useState } from "react";
import DataTable from "./DataTable";
import Chart from "./Chart";

function Upload() {
  const [data, setData] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://localhost:8001/datasets/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setData(res.data);
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  return (
    <div className="upload-container">
      <input
        type="file"
        id="fileUpload"
        hidden
        onChange={handleUpload}
      />

      <label htmlFor="fileUpload" className="upload-btn">
        📤 Upload Dataset
      </label>

      {data && (
        <>
          <h3>Dataset Preview</h3>
          <DataTable columns={data.columns} rows={data.rows} />

          <h3 style={{ marginTop: "30px" }}>Auto Chart</h3>
          {data.charts.map((chart, index) => (
  <Chart key={index} chart={chart} />
))}

        </>
      )}
    </div>
  );
}

export default Upload;
