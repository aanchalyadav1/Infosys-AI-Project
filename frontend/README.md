# AI Music Frontend (Corrected Flow)

This frontend implements:
- Email/password signup & login (Firebase)
- Dashboard (after login) with upload & camera capture
- Calls backend /detect and /recommend
- Plays preview audio returned by backend

Setup:
1. Copy `.env.example` -> `.env` and fill values (especially REACT_APP_BACKEND_URL)
2. npm install
3. npm start

Backend expected endpoints:
POST {BACKEND_URL}/detect (form-data key: image) -> { "success": true, "emotion": "<label>" }
POST {BACKEND_URL}/recommend (json: { emotion: "<label>" }) -> { "success": true, "songs": [...] }
