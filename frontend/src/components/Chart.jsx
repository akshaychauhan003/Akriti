import Plot from "react-plotly.js";

function Chart({ chart }) {
  if (!chart) {
    return <p>No chart available for this data</p>;
  }

  return (
    <div style={{ marginBottom: "30px" }}>
      <div style={{ marginBottom: "10px" }}>
        <h4 style={{ margin: "0 0 5px 0", color: "#333" }}>
          {chart.name || "Chart"}
        </h4>
        <p style={{ margin: "0", fontSize: "14px", color: "#666", fontStyle: "italic" }}>
          {chart.description || "No description available"}
        </p>
      </div>
      <Plot
        data={[
          {
            type: chart.type,
            x: chart.x,
            y: chart.y,
          },
        ]}
        layout={{
          title: `${chart.y_label} by ${chart.x_label}`,
        }}
        style={{ width: "100%", height: "400px" }}
      />
    </div>
  );
}

export default Chart;
