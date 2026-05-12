from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import uuid
import os

router = APIRouter()

# 📁 data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))
os.makedirs(DATA_DIR, exist_ok=True)


# -------------------------
# Chart Builder
# -------------------------
def build_charts(df: pd.DataFrame):
    charts = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    # Histograms
    for col in numeric_cols[:3]:
        charts.append({
            "type": "histogram",
            "x": df[col].tolist(),
            "title": f"Distribution of {col}",
            "name": f"Distribution Histogram",
            "description": f"Shows the frequency distribution of the '{col}' column. Helps identify patterns, outliers, and data clustering.",
        })

    # Bar charts
    if numeric_cols and categorical_cols:
        charts.append({
            "type": "bar",
            "x": df[categorical_cols[0]].astype(str).tolist()[:20],
            "y": df[numeric_cols[0]].tolist()[:20],
            "title": f"{numeric_cols[0]} by {categorical_cols[0]}",
            "name": f"Bar Chart",
            "description": f"Compares '{numeric_cols[0]}' across different categories of '{categorical_cols[0]}'. Useful for comparing values across groups.",
        })

    # Scatter
    if len(numeric_cols) >= 2:
        charts.append({
            "type": "scatter",
            "x": df[numeric_cols[0]].tolist(),
            "y": df[numeric_cols[1]].tolist(),
            "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
            "name": f"Scatter Plot",
            "description": f"Displays relationship between '{numeric_cols[0]}' (X-axis) and '{numeric_cols[1]}' (Y-axis). Reveals correlations and trends.",
        })

    return charts


# -------------------------
# Upload Dataset
# -------------------------
@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported")

    dataset_id = str(uuid.uuid4())
    file_path = os.path.join(DATA_DIR, f"{dataset_id}.csv")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    return {
        "dataset_id": dataset_id,
        "columns": df.columns.tolist(),
        "rows": df.head(10).to_dict(orient="records"),
        "charts": build_charts(df),
    }


# -------------------------
# Apply Filters
# -------------------------
@router.post("/{dataset_id}/filter")
def apply_filters(dataset_id: str, filters: dict):
    file_path = os.path.join(DATA_DIR, f"{dataset_id}.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(file_path)

    for col, condition in filters.items():
        if col not in df.columns:
            continue

        if isinstance(condition, list):
            df = df[df[col].isin(condition)]

        elif isinstance(condition, dict):
            if "min" in condition:
                df = df[df[col] >= float(condition["min"])]
            if "max" in condition:
                df = df[df[col] <= float(condition["max"])]

    return {
        "columns": df.columns.tolist(),
        "rows": df.head(10).to_dict(orient="records"),
        "charts": build_charts(df),
    }
