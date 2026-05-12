import pandas as pd
from app.ai.service import recommend_charts

def generate_charts(dataset_id, user_id):
    data = load_dataset(dataset_id, user_id)
    schema = {"columns": data.dtypes.to_dict(), "sample": data.head(10).to_dict()}
    recommendations = recommend_charts(schema)  # AI call
    return recommendations  # List of chart JSONs