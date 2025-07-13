# Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended for beginners)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Create a new project** and select "Deploy from GitHub repo"
4. **Add PostgreSQL** database from Railway's database section
5. **Set environment variables**:
   ```
   DB_HOST=your-railway-postgres-host
   DB_PORT=5432
   DB_NAME=railway
   DB_USER=postgres
   DB_PASSWORD=your-railway-password
   SECRET_KEY=your-secret-key
   DEBUG=False
   ```
6. **Deploy!** Railway will automatically build and deploy your app

### Option 2: Render

1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub** repository
4. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Add PostgreSQL** database from Render's database section
6. **Set environment variables** (same as Railway)
7. **Deploy!**

### Option 3: Heroku

1. **Install Heroku CLI** and sign up
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Add PostgreSQL**: `heroku addons:create heroku-postgresql:mini`
5. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
6. **Deploy**: `git push heroku main`

## 🔧 Environment Variables

Set these in your hosting platform:

```bash
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
SECRET_KEY=your-secret-key-here
DEBUG=False  # Set to False in production
```

## 📁 Required Files

Your project already includes:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells platform how to run the app
- ✅ `runtime.txt` - Python version specification
- ✅ `Dockerfile` - For containerized deployment
- ✅ `docker-compose.yml` - For local development

## 🐳 Docker Deployment

If you prefer Docker deployment:

1. **Build the image**: `docker build -t your-app-name .`
2. **Run with database**: `docker-compose up -d`
3. **Deploy to platforms** that support Docker (Railway, Render, DigitalOcean)

## 🔍 Testing Your Deployment

After deployment, test these endpoints:
- `GET /` - Main page
- `POST /upload/` - File upload
- `GET /files/` - List files
- `GET /files/{id}/json` - Get file data

## 🛠️ Troubleshooting

### Common Issues:

1. **Database Connection**: Ensure environment variables are set correctly
2. **Port Issues**: Make sure your app listens on `0.0.0.0` and uses `$PORT`
3. **Dependencies**: Check that all packages in `requirements.txt` are compatible
4. **File Uploads**: Ensure your platform supports file uploads and has sufficient storage

### Debug Mode:
- Set `DEBUG=True` temporarily to see detailed error messages
- Check platform logs for specific error information

## 📊 Monitoring

Most platforms provide:
- **Application logs**
- **Database monitoring**
- **Performance metrics**
- **Error tracking**

Enable these features in your hosting platform's dashboard. 