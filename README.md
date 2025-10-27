# 🎵 AI Music Recommendation System

An intelligent music recommendation system that uses emotion detection through facial recognition to suggest personalized music from Spotify. Built with React frontend and Flask backend.

## 🚀 Features

- **Emotion Detection**: AI-powered facial emotion recognition using TensorFlow
- **Music Recommendations**: Spotify integration for personalized song suggestions
- **User Authentication**: Firebase-based user management
- **Real-time Processing**: Live emotion detection and instant music recommendations
- **Multi-language Support**: Support for different language preferences
- **Responsive Design**: Modern UI built with React and Tailwind CSS

## 🏗️ Project Structure

```
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── emotion_model.keras # Pre-trained emotion detection model
│   ├── firebaseConfig.json # Firebase service account key
│   └── .env               # Environment variables
├── frontend/               # React application
│   ├── src/               # Source code
│   ├── public/            # Static files
│   ├── package.json       # Node.js dependencies
│   └── .env              # Frontend environment variables
└── README.md             # This file
```

## 📋 Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **npm or yarn** (package manager)
- **Spotify Developer Account** (for API access)
- **Firebase Project** (for authentication and database)

## 🛠️ Installation & Setup

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

5. **Set up Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Generate a service account key (JSON file)
   - Rename it to `firebaseConfig.json` and place in backend directory
   - Enable Authentication and Firestore in your Firebase project

6. **Run the backend server**
   ```bash
   python app.py
   ```
   
   The backend will start on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8000
   REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
   REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   REACT_APP_FIREBASE_PROJECT_ID=your_project_id
   ```

4. **Run the frontend development server**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

## 🔧 Configuration

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy the Client ID and Client Secret
4. Add them to your backend `.env` file

### Firebase Setup

1. Create a Firebase project
2. Enable Authentication (Email/Password)
3. Enable Firestore Database
4. Generate service account key
5. Download and rename to `firebaseConfig.json`
6. Get your web app config for frontend `.env`

## 🚀 Running the Application

1. **Start the backend server** (in backend directory):
   ```bash
   source venv/bin/activate  # Activate virtual environment
   python app.py
   ```

2. **Start the frontend server** (in frontend directory):
   ```bash
   npm start
   ```

3. **Access the application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## 📡 API Endpoints

- `GET /` - Health check
- `POST /detect` - Emotion detection from uploaded image
- `POST /recommend` - Get music recommendations based on emotion
- `POST /signup` - User registration
- `POST /forgot-password` - Password reset
- `GET /health` - Server health status

## 🧪 Testing

### Backend Testing
```bash
cd backend
# Test emotion detection endpoint
curl -X POST http://localhost:8000/detect -F "image=@test_image.jpg"

# Test recommendations endpoint
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"emotion": "Happy", "language": "english"}'
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Production Deployment

### Backend (Render/Heroku)
1. Create `Procfile.txt`:
   ```
   web: gunicorn app:app
   ```
2. Set environment variables in your hosting platform
3. Deploy the backend directory

### Frontend (Netlify/Vercel)
1. Build the project:
   ```bash
   npm run build
   ```
2. Deploy the `build` directory
3. Set environment variables in your hosting platform

## 🔒 Environment Variables

### Backend (.env)
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
PORT=8000
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Module not found errors**:
   - Ensure virtual environment is activated for backend
   - Run `pip install -r requirements.txt` again

2. **Firebase connection issues**:
   - Verify `firebaseConfig.json` is in the correct location
   - Check Firebase project settings

3. **Spotify API errors**:
   - Verify your Spotify credentials in `.env`
   - Ensure your Spotify app is properly configured

4. **CORS errors**:
   - Check that backend CORS is properly configured
   - Verify frontend is making requests to correct backend URL

### Getting Help

- Check the [Issues](../../issues) page for known problems
- Create a new issue if you encounter a bug
- Refer to the documentation for [Flask](https://flask.palletsprojects.com/), [React](https://reactjs.org/), and [Firebase](https://firebase.google.com/docs)

## 🎯 Future Enhancements

- [ ] Real-time emotion detection via webcam
- [ ] Playlist creation and management
- [ ] Social features and music sharing
- [ ] Advanced emotion analysis
- [ ] Mobile app development
- [ ] Integration with more music platforms

---

Made with ❤️ by [Your Name]