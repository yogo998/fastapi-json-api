from fastapi import FastAPI
import json
import os

app = FastAPI()

# Load JSON file
json_file = "AutoQuoteResponse_500.json"

if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
else:
    data = {"error": "JSON file not found"}

# Default page size
PAGE_SIZE = 35

@app.get("/")
def home():
    return {"message": "FastAPI is running on Render!"}

@app.get("/project/{date}/{page}/{page_size}")
def get_project_data(date: str, page: int, page_size: int):
    """Fetch paginated project data based on date, page number, and page size."""
    
    if "projects" not in data:
        return {"error": "Invalid JSON format"}
    
    projects = data["projects"]
    total_records = len(projects)
    
    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size
    paginated_data = projects[start:end]

    return {
        "date_requested": date,
        "page": page,
        "page_size": page_size,
        "total_pages": (total_records // page_size) + (1 if total_records % page_size > 0 else 0),
        "total_records": total_records,
        "records_on_page": len(paginated_data),
        "data": paginated_data
    }
