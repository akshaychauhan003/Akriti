function Filters({ columns, rows, onApply }) {
  // build options from current data
  const categoricalColumns = columns.filter(
    (col) => typeof rows[0]?.[col] === "string"
  );

  const handleChange = (col, value) => {
    onApply(col, value);
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>Filters</h3>

      {categoricalColumns.map((col) => {
        const uniqueValues = [...new Set(rows.map((r) => r[col]))];

        return (
          <div key={col} style={{ marginBottom: "10px" }}>
            <label>{col}: </label>
            <select onChange={(e) => handleChange(col, e.target.value)}>
              <option value="">All</option>
              {uniqueValues.map((v) => (
                <option key={v} value={v}>
                  {v}
                </option>
              ))}
            </select>
          </div>
        );
      })}
    </div>
  );
}

export default Filters;
