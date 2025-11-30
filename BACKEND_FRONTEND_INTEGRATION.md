# Backend-Frontend Integration Guide

## Problem
The backend and frontend are deployed to separate Vercel projects and need to communicate via API.

## Solution

### 1. Deploy Backend First
Deploy the backend to Vercel:
```bash
cd backend
vercel deploy --prod
```

Note the deployed backend URL (e.g., `https://your-backend-project.vercel.app`)

### 2. Set Frontend Environment Variable
In the **Docusaurus/Frontend** project on Vercel:
1. Go to **Settings > Environment Variables**
2. Add:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: `https://your-backend-project.vercel.app` (replace with actual URL)
   - **Environments**: Select "Production" (and "Preview" if testing)

3. Redeploy the frontend for changes to take effect

### 3. For Local Development
Create `my-ai-book/.env.local`:
```
REACT_APP_BACKEND_URL=http://127.0.0.1:8000
```

Then start both:
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd my-ai-book
npm start
```

## API Endpoints

All endpoints accessed through the backend URL:
- `POST {BACKEND_URL}/chat` - Chat with RAG
- `POST {BACKEND_URL}/personalize` - Personalize content
- `POST {BACKEND_URL}/translate` - Translate to Urdu
- `GET {BACKEND_URL}/` - Health check

## Required Backend Environment Variables

Set in Vercel backend project settings:
- `GEMINI_API_KEY` - Your Gemini API key
- `QDRANT_URL` - Qdrant vector database URL
- `QDRANT_API_KEY` - Qdrant API key

## Troubleshooting

If backend is not reachable:
1. Verify `REACT_APP_BACKEND_URL` is set correctly in Vercel frontend settings
2. Ensure backend is deployed and running: `https://your-backend-url/` should return `{"status": "Agentic AI Backend is Running"}`
3. Check browser console for CORS errors
4. Verify backend environment variables are set in Vercel backend project
