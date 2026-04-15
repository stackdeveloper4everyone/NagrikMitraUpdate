# NagrikMitra

AI-powered multilingual citizen service assistant with a FastAPI backend and Streamlit frontend.

## Run locally

```powershell
cd citizen-assistant
python run.py
```

- API docs: `http://localhost:8000/docs`
- Streamlit UI: `http://localhost:8501`

## Deploy Streamlit frontend

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set the **Main file path** to:

```text
frontend/streamlit_app.py
```

4. Streamlit Cloud will use `frontend/requirements.txt` for dependency install.

5. Add app secrets in Streamlit:

```toml
API_BASE_URL = "https://<your-backend-domain>"
```

The Streamlit app uses `API_BASE_URL` from Streamlit secrets (or environment variable) and falls back to `http://localhost:8000` for local development.

## Note

For cloud deployment, the FastAPI backend must be hosted separately (e.g., Render, Railway, Azure, AWS, etc.) and exposed via HTTPS.
