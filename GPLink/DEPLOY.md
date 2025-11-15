# GPLink - Cloud Deployment Guide

## 🚀 Deploy GPLink to Cloud (FREE)

### Prerequisites
- GitHub account (you have: DrSy4h/test ✅)
- MongoDB Atlas (already setup ✅)

---

## 📦 Step 1: Prepare Repository

### Update .env.example for reference
Create `.env.example` file (template for deployment):
```
MONGODB_ATLAS_CLUSTER_URI=your_mongodb_connection_string_here
MONGODB_DATABASE_NAME=gplink_db
```

### Ensure .gitignore excludes sensitive files
- ✅ .env (contains passwords)
- ✅ __pycache__
- ✅ uploads/ (images)

---

## 🎨 Step 2: Deploy Frontend (Streamlit Cloud)

### A. Go to Streamlit Cloud
1. Visit: https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"

### B. Configure Deployment
- **Repository:** `DrSy4h/test`
- **Branch:** `main`
- **Main file path:** `GPLink/frontend/app.py`

### C. Add Secrets (Environment Variables)
In Streamlit Cloud dashboard → Settings → Secrets:
```toml
# Not needed for frontend - it connects to backend API
```

### D. Deploy
- Click "Deploy!"
- Wait 2-3 minutes
- You'll get URL like: `https://gplink-drsy4h.streamlit.app`

---

## ⚡ Step 3: Deploy Backend (Render.com)

### A. Create Render Account
1. Visit: https://render.com
2. Sign up with GitHub
3. Connect your repository

### B. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect repository: `DrSy4h/test`
3. Configure:
   - **Name:** `gplink-backend`
   - **Root Directory:** `GPLink/backend`
   - **Runtime:** `Python 3.12`
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### C. Add Environment Variables
In Render dashboard → Environment:
```
MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://drsy4h:uBwLQoc1F00th8dl@cluster0.wqpjziw.mongodb.net/
MONGODB_DATABASE_NAME=gplink_db
```

### D. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes
- You'll get URL like: `https://gplink-backend.onrender.com`

---

## 🔗 Step 4: Connect Frontend to Backend

### Update Frontend API URL
Edit `GPLink/frontend/app.py`, line 12:
```python
# Change from:
API_URL = "http://localhost:8000/api"

# To:
API_URL = "https://gplink-backend.onrender.com/api"
```

### Update CORS in Backend
Edit `GPLink/backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "https://gplink-drsy4h.streamlit.app",  # Add your Streamlit URL
        "https://*.streamlit.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Commit & Push
```powershell
git add .
git commit -m "Update API URLs for cloud deployment"
git push origin main
```

Both apps will auto-redeploy! 🎉

---

## ✅ Step 5: Test Deployed App

1. Open Streamlit URL: `https://gplink-drsy4h.streamlit.app`
2. Register doctors
3. Create consultations
4. Upload images
5. Share URL with anyone! 🌍

---

## 💰 Pricing (All FREE!)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Streamlit Cloud** | ✅ Free forever | 1 app, unlimited users |
| **Render.com** | ✅ Free tier | 750 hrs/month (enough!) |
| **MongoDB Atlas** | ✅ Free tier | 512MB storage |

Total cost: **$0/month** 🎉

---

## 🔒 Security Notes

### Protect .env file
- ✅ Already in .gitignore
- Never commit passwords to GitHub
- Use Render/Streamlit secrets for production

### MongoDB Atlas Security
1. Go to MongoDB Atlas → Network Access
2. Add IP: `0.0.0.0/0` (allow from anywhere)
3. Or add specific Render IP addresses

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Check API_URL in `frontend/app.py`
- Ensure backend is deployed and running
- Check CORS settings in `backend/main.py`

### Backend crashes on Render
- Check logs in Render dashboard
- Verify environment variables are set
- Check MongoDB connection string

### Images not uploading
- Render free tier has ephemeral storage
- Images will be deleted on redeploy
- For permanent storage, use AWS S3 or Cloudinary

---

## 🎯 Alternative: Quick Deploy (Easier)

### Railway.app (One-click deploy)
1. Visit: https://railway.app
2. "Deploy from GitHub"
3. Select repository
4. Railway auto-detects everything! 🚀

### Vercel (Frontend only)
1. Visit: https://vercel.com
2. Import GitHub repo
3. Auto-deploy Streamlit
4. Super fast! ⚡

---

**Made with ❤️ by DRAHMADSYAHID © 2025**
