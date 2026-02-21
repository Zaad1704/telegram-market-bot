#!/bin/bash

# 🚀 Telegram Bot Deployment Script
# This script helps deploy the bot to various platforms

set -e

echo "🤖 Telegram Market Monitor Bot Deployment Script"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "All dependencies are installed!"
}

# Initialize Git repository
init_git() {
    print_status "Initializing Git repository..."
    
    if [ ! -d ".git" ]; then
        git init
        git add .
        git commit -m "Initial commit: Telegram Market Monitor Bot"
        print_success "Git repository initialized!"
    else
        print_warning "Git repository already exists."
    fi
}

# Setup GitHub repository
setup_github() {
    print_status "Setting up GitHub repository..."
    
    echo "Please enter your GitHub username:"
    read -r GITHUB_USERNAME
    
    echo "Please enter your desired repository name (default: telegram-market-bot):"
    read -r REPO_NAME
    REPO_NAME=${REPO_NAME:-telegram-market-bot}
    
    # Add remote if not exists
    if ! git remote get-url origin &> /dev/null; then
        git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        print_success "GitHub remote added!"
    fi
    
    # Push to GitHub
    print_status "Pushing to GitHub..."
    git branch -M main
    git push -u origin main || {
        print_warning "Push failed. You may need to create the repository on GitHub first."
        echo "Please create a repository at: https://github.com/new"
        echo "Then run: git push -u origin main"
    }
}

# Deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
        print_status "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    print_status "Logging into Railway..."
    railway login
    
    print_status "Deploying to Railway..."
    railway up
    
    print_success "Deployed to Railway!"
    print_warning "Don't forget to set environment variables in Railway dashboard:"
    echo "  - TELEGRAM_TOKEN=8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A"
    echo "  - NEWS_API_KEY=your_news_api_key"
}

# Deploy to Render (provide instructions)
deploy_render() {
    print_status "Render Deployment Instructions:"
    echo "1. Go to https://render.com"
    echo "2. Sign up with your GitHub account"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect your GitHub repository"
    echo "5. Configure:"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python market_monitor_bot.py"
    echo "   - Instance Type: Free"
    echo "6. Set Environment Variables:"
    echo "   - TELEGRAM_TOKEN=8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A"
    echo "   - NEWS_API_KEY=your_news_api_key"
}

# Deploy with Docker
deploy_docker() {
    print_status "Building Docker image..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    docker build -t telegram-market-bot .
    print_success "Docker image built!"
    
    print_status "Running with Docker Compose..."
    docker-compose up -d
    
    print_success "Bot is running with Docker!"
    print_warning "Don't forget to create .env file with your API keys."
}

# Main menu
main_menu() {
    echo ""
    echo "Choose deployment option:"
    echo "1) Setup GitHub Repository"
    echo "2) Deploy to Railway (Recommended)"
    echo "3) Deploy to Render (Free)"
    echo "4) Deploy with Docker (Local)"
    echo "5) Full Setup (GitHub + Railway)"
    echo "6) Exit"
    echo ""
    echo "Enter your choice (1-6):"
    read -r CHOICE
    
    case $CHOICE in
        1)
            check_dependencies
            init_git
            setup_github
            ;;
        2)
            deploy_railway
            ;;
        3)
            deploy_render
            ;;
        4)
            deploy_docker
            ;;
        5)
            check_dependencies
            init_git
            setup_github
            deploy_railway
            ;;
        6)
            print_success "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please try again."
            main_menu
            ;;
    esac
}

# Start script
main_menu

print_success "Deployment process completed!"
echo ""
echo "📚 Next Steps:"
echo "1. Set up your News API key (optional but recommended)"
echo "2. Configure environment variables"
echo "3. Test your bot on Telegram"
echo "4. Check logs for any issues"
echo ""
echo "🤖 Your bot: t.me/Sajib_Market_Trading_Monitor_bot"
echo "📖 Documentation: README.md"
echo "🚀 Deployment Guide: GITHUB_DEPLOYMENT.md"
