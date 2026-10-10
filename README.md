# Apex Enterprise API Engine

A high-performance FastAPI backend serving dynamic JSON endpoints, bundled with a modern frontend UI (`index.html`).

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)

## Setup Instructions

1. Open a terminal and navigate to the project directory:
   ```bash
   cd "path/to/AIML INTERN PROJECT"
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required Python dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

## Execution Instructions

To start the application, simply run the `main.py` file:

```bash
python main.py
```

The server will start locally. You can access the following URLs in your web browser:

- **Web Application UI**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive API Documentation (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Documentation (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Key API Endpoints

- `GET /api/v1/health`: System health check and runtime specifications.
- `GET /api/v1/users`: Directory of all available mock user profiles.
- `GET /api/v1/data`: Retrieve structured enterprise data payload for a user.
- `POST /api/v1/action`: Process dynamic frontend user actions (e.g., Freeze Card, Transfers, etc.).
- `GET /api/v1/telemetry`: Retrieve system operational metrics for real-time charts.
