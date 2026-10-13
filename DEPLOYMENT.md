# EKIP Deployment Guide

This project is already configured for a split deployment:

- Frontend: Vercel
- Backend: Render or any Python host

## 1) Frontend deployment on Vercel

1. Push this repo to GitHub.
2. Import the `frontend/vite-project` folder into Vercel.
3. Set the environment variable:
   - `VITE_API_BASE_URL=https://your-backend-domain.onrender.com`
4. Deploy.

## 2) Backend deployment on Render

1. Create a new Web Service on Render.
2. Connect the repo.
3. Set the root directory to `backend`.
4. Use the included `Dockerfile` or run:
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables from `backend/.env.example`.

## 3) Required env variables

Backend:
- `OPENAI_API_KEY`
- `MODEL_PROVIDER`
- `MODEL_NAME`
- `COLLECTION_NAME`
- `CORS_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:5173`

Frontend:
- `VITE_API_BASE_URL=https://your-backend-domain.onrender.com`

## 4) Notes

- The backend already includes an in-memory Qdrant fallback for local/demo operation.
- For production, replace the in-memory fallback with a real Qdrant service.
- For a production-ready deployment, add a dedicated Vue/React hosting domain and set the backend CORS origin list accordingly.
