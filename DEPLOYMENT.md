# Streamlit Cloud Deployment Guide

## Prerequisites
1. GitHub repository with your code (already done ✓)
2. Streamlit Cloud account (free at https://streamlit.io/cloud)
3. Backend API deployed and accessible

## Steps to Deploy Frontend

### 1. Deploy Backend First
Your Streamlit app needs a backend API running. Deploy your FastAPI backend to:
- **Heroku** (deprecated, use alternatives)
- **Railway.app** (recommended, free tier available)
- **Fly.io** 
- **AWS Elastic Beanstalk**
- **Google Cloud Run**
- **Azure Container Instances**

Get the deployed backend URL (e.g., `https://your-backend.railway.app`)

### 2. Push Code to GitHub
Make sure all these files are committed:
```
citizen-assistant/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
└── other files...
```

### 3. Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repository
4. Set the main file path: `frontend/streamlit_app.py`
5. Click "Deploy"

### 4. Configure Secrets in Streamlit Cloud
1. In your deployed app settings, go to "Secrets"
2. Add this configuration:
```toml
API_BASE_URL = "https://your-deployed-backend-url.com"
```

## Troubleshooting

### "Cannot connect to backend server"
- Ensure backend API is deployed and running
- Verify API_BASE_URL in Streamlit secrets is correct
- Check CORS settings in backend (app/main.py)

### Timeout errors
- Backend might be on free tier (slow startup)
- Increase timeout in requests calls if needed
- Check backend logs

### Import errors
- Ensure all required packages are in `frontend/requirements.txt`
- Run locally first: `streamlit run frontend/streamlit_app.py`

## Local Testing
```bash
cd citizen-assistant
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
export API_BASE_URL="http://localhost:8000"  # Point to local backend
streamlit run frontend/streamlit_app.py
```

## Notes
- Default timeout for requests: 30-60 seconds
- Max file upload: 200MB (configurable in config.toml)
- Frontend runs on port 8501 (local) or Streamlit Cloud assigns a URL
