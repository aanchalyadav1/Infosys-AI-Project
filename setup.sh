#!/bin/bash

echo "🎵 AI Music Recommendation System Setup"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Backend setup
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created backend/.env file. Please edit it with your credentials."
fi

cd ..

# Frontend setup
echo ""
echo "🔧 Setting up Frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created frontend/.env file. Please edit it with your credentials."
fi

cd ..

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your Spotify credentials"
echo "2. Add firebaseConfig.json to backend directory"
echo "3. Edit frontend/.env with your Firebase and backend URL"
echo "4. Run 'cd backend && source venv/bin/activate && python app.py' to start backend"
echo "5. Run 'cd frontend && npm start' to start frontend"
echo ""
echo "📖 See README.md for detailed instructions"