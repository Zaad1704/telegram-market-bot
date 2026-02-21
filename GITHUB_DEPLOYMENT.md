# 🚀 GitHub Deployment Guide

This guide will help you deploy your Telegram bot to run continuously on GitHub using various deployment options.

## 📋 Prerequisites

1. **GitHub Repository**: Create a new repository on GitHub
2. **Bot Token**: Your Telegram bot token (already configured)
3. **News API Key**: Optional but recommended (get from [NewsAPI.org](https://newsapi.org/))

## 🎯 Deployment Options

### Option 1: GitHub Actions (Recommended for Development)

**Best for**: Testing, CI/CD, temporary deployments

#### Setup Steps:

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Telegram Market Monitor Bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/telegram-market-bot.git
   git push -u origin main
   ```

2. **Configure GitHub Secrets**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `TELEGRAM_TOKEN`: `8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A`
     - `NEWS_API_KEY`: Your News API key (optional)

3. **Enable GitHub Actions**
   - Push to main branch to trigger the workflow
   - Monitor deployment in Actions tab

**⚠️ Limitation**: GitHub Actions has timeout limits (max 6 hours), not suitable for 24/7 bot operation.

---

### Option 2: Railway (Recommended for Production)

**Best for**: Easy deployment, 24/7 operation, free tier available

#### Setup Steps:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Deploy**
   ```bash
   railway up
   ```

4. **Configure Environment Variables**
   - In Railway dashboard, set these variables:
     - `TELEGRAM_TOKEN`: `8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A`
     - `NEWS_API_KEY`: Your News API key

5. **Configure GitHub Secrets for Railway**
   - `RAILWAY_TOKEN`: Your Railway API token
   - `RAILWAY_SERVICE_ID`: Your Railway service ID

---

### Option 3: Render (Alternative Free Hosting)

**Best for**: Free hosting, easy setup, good performance

#### Setup Steps:

1. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the telegram-bot repository

3. **Configure Deployment**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python market_monitor_bot.py`
   - **Instance Type**: Free

4. **Set Environment Variables**
   - `TELEGRAM_TOKEN`: `8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A`
   - `NEWS_API_KEY`: Your News API key

---

### Option 4: Docker + Any Cloud Provider

**Best for**: Maximum flexibility, custom deployments

#### Setup Steps:

1. **Build Docker Image**
   ```bash
   docker build -t telegram-market-bot .
   ```

2. **Push to Registry**
   ```bash
   docker tag telegram-market-bot YOUR_USERNAME/telegram-market-bot:latest
   docker push YOUR_USERNAME/telegram-market-bot:latest
   ```

3. **Deploy to Cloud**
   - **AWS ECS**: Use Fargate for serverless deployment
   - **Google Cloud Run**: Serverless container deployment
   - **Azure Container Instances**: Simple container hosting
   - **DigitalOcean App Platform**: Simple app deployment

---

## 🔧 Configuration Files Explained

### `.github/workflows/deploy.yml`
- **CI/CD Pipeline**: Automated testing and deployment
- **Multi-stage**: Test → Deploy → Docker build
- **Secrets Management**: Secure handling of API keys

### `Dockerfile`
- **Multi-stage**: Optimized for production
- **Security**: Non-root user, minimal dependencies
- **Health Checks**: Automatic monitoring

### `docker-compose.yml`
- **Local Development**: Easy local testing
- **Redis**: Optional caching for user preferences
- **Volumes**: Persistent data storage

### `railway.json`
- **Railway Configuration**: Optimized settings for Railway deployment
- **Health Checks**: Automatic restart on failure

### `render.yaml`
- **Render Configuration**: Optimized for Render platform
- **Environment Variables**: Secure configuration

---

## 🚀 Quick Deployment Commands

### Railway (Fastest)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up

# Set environment variables in Railway dashboard
```

### Render (Web Interface)
1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Configure build and start commands
4. Set environment variables

### Docker (Universal)
```bash
# Build and run locally
docker-compose up -d

# Deploy to cloud (example: AWS)
docker build -t telegram-bot .
aws ecs create-cluster --cluster-name telegram-bot
```

---

## 🔐 Security Best Practices

### 1. API Key Management
- ✅ **Never commit API keys to repository**
- ✅ **Use GitHub Secrets or environment variables**
- ✅ **Rotate keys regularly**

### 2. Bot Security
- ✅ **Token is already configured and secure**
- ✅ **Rate limiting implemented**
- ✅ **Input validation for user commands**

### 3. Deployment Security
- ✅ **Non-root Docker user**
- ✅ **Minimal dependencies**
- ✅ **Health checks enabled**

---

## 📊 Monitoring and Logs

### Railway
- **Logs**: Available in Railway dashboard
- **Metrics**: Built-in monitoring
- **Alerts**: Configure for downtime notifications

### Render
- **Logs**: Real-time logs in dashboard
- **Metrics**: Performance monitoring
- **Alerts**: Email notifications on errors

### Docker
- **Logs**: `docker-compose logs -f`
- **Monitoring**: Use Prometheus/Grafana
- **Alerts**: Configure custom alerting

---

## 🛠️ Troubleshooting

### Common Issues

#### Bot Not Starting
```bash
# Check logs
docker-compose logs telegram-bot

# Or on Railway/Render, check dashboard logs
```

#### API Key Issues
- Verify secrets are correctly set
- Check API key validity
- Ensure proper environment variable names

#### Memory Issues
- Free tiers have memory limits
- Monitor memory usage
- Optimize code if needed

#### Rate Limiting
- Telegram has rate limits
- Implement proper delays
- Use caching where possible

### Debug Mode
Enable debug logging by setting environment variable:
```bash
LOG_LEVEL=DEBUG
```

---

## 📈 Scaling Options

### Free Tiers
- **Railway**: 500 hours/month
- **Render**: 750 hours/month
- **GitHub Actions**: 2000 minutes/month

### Paid Scaling
- **Vertical**: Increase memory/CPU
- **Horizontal**: Multiple instances
- **Geographic**: Deploy closer to users

---

## 🎯 Recommended Setup

**For Production**: Railway + GitHub Actions
- **Continuous Deployment**: Auto-deploy on push
- **24/7 Operation**: Railway handles uptime
- **Easy Management**: Web interface
- **Cost Effective**: Free tier sufficient

**For Development**: Local Docker + GitHub Actions
- **Local Testing**: Docker Compose
- **CI/CD**: GitHub Actions
- **Staging**: Deploy to Railway before production

---

## 📞 Support

### GitHub Issues
- Report bugs in repository Issues
- Include logs and error messages
- Specify deployment method

### Documentation
- Check this guide first
- Review README.md
- Look at code comments

### Community
- Telegram: @Sajib
- GitHub: Repository discussions
- Stack Overflow: Tag with telegram-bot

---

## 🎉 Deployment Checklist

- [ ] Create GitHub repository
- [ ] Set up GitHub Secrets
- [ ] Choose deployment platform
- [ ] Configure environment variables
- [ ] Test deployment
- [ ] Set up monitoring
- [ ] Configure alerts
- [ ] Document customizations

---

**Your bot is now ready for GitHub deployment! 🚀**

Choose the deployment option that best fits your needs and follow the specific setup instructions.
