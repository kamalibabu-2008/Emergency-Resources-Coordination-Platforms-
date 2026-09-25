# ResQLink — Full Hackathon Prototype

## One-tap run

### Windows
1. Install Python.
2. Open this folder in Command Prompt.
3. Run:
   `pip install flask flask-cors`
4. Run:
   `python app.py`
5. Open:
   `http://127.0.0.1:5000/`

The frontend is `index.html` and the backend is `app.py`.
A SQLite database named `resqlink.db` is created automatically.

## Backend API
- GET /api/health
- GET/POST /api/incidents
- PATCH /api/incidents/<id>
- GET/POST /api/requests
- PATCH /api/requests/<id>
- GET/POST /api/volunteers
- POST /api/sos
- GET /api/dashboard

## Important
The current visual frontend remains the original attractive prototype. Its forms are already functional in demo mode.
For a fully API-connected version, replace the form JavaScript with fetch() calls to the endpoints above.
