Team Name : Nexora

Team Members : KAMALI B, INDHUJA N, ANGELIN SHERLY S

WEB-02: Emergency Resource Coordination Platform Problem Statement: Develop a web application that helps coordinate emergency resources during situations such as floods, accidents, or other local emergencies. Users should be able to report incidents and request resources such as food, medical assistance, transportation, or volunteers.
Expected Features:  Incident reporting  Resource requests  Location information  Volunteer registration  Admin dashboard  Request status tracking 
Challenge Level: High 

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
