# RB Project - Spotify Recent Tracks

A Django application for fetching and displaying recent Spotify tracks.

## Project Structure

```
rb_project/              # Django project root
├── manage.py
├── rb_project/          # Django settings module
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── rb/                  # Core app (your main app)
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── services/         # Spotify service logic
    │   └── spotify_client.py
    ├── urls.py           # App-level routing
    ├── views.py          # Main views for Spotify
    ├── utils/            # Shared helper functions
    │   └── env.py
    └── templates/        # (optional for future UI)
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file:
   ```bash
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REFRESH_TOKEN=your_spotify_refresh_token
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Getting Spotify Credentials

### Step 1: Create a Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - **App name**: `RB Project` (or any name you prefer)
   - **App description**: `Django app for recent tracks`
   - **Redirect URI**: `http://localhost:8888/callback`
   - **Website**: `http://localhost:8000`
5. Accept the terms and create the app

### Step 2: Get Client ID and Secret

1. In your app dashboard, you'll see:
   - **Client ID**: Copy this to your `.env` file
   - **Client Secret**: Click "Show Client Secret" and copy to `.env` file

### Step 3: Get Refresh Token

#### Option A: Automated Script (Recommended)
```bash
python get_spotify_token.py
```

This script will:
- Open your browser to Spotify authorization
- Guide you through the OAuth flow
- Automatically save the refresh token to your `.env` file

#### Option B: Manual Method

1. **Create Authorization URL**:
   ```
   https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:8888/callback&scope=user-read-recently-played%20user-read-private%20user-read-email&show_dialog=true
   ```
   (Replace `YOUR_CLIENT_ID` with your actual client ID)

2. **Open the URL** in your browser and authorize the app

3. **Copy the authorization code** from the URL (it will look like: `http://localhost:8888/callback?code=AQD...`)

4. **Exchange code for tokens** using curl:
   ```bash
   curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \
        -H "Authorization: Basic $(echo -n 'YOUR_CLIENT_ID:YOUR_CLIENT_SECRET' | base64)" \
        -d "grant_type=authorization_code&code=AUTHORIZATION_CODE&redirect_uri=http://localhost:8888/callback" \
        https://accounts.spotify.com/api/token
   ```

5. **Copy the refresh_token** from the response and add it to your `.env` file

## API Endpoints

- `GET /recent-tracks/` - Get recent Spotify tracks
  - Query parameter: `limit` (1-50, default: 10)
- `GET /test-env/` - Test environment variables (debug endpoint)

## Testing

1. **Test environment variables**:
   ```bash
   curl http://localhost:8000/test-env/
   ```

2. **Test recent tracks**:
   ```bash
   curl http://localhost:8000/recent-tracks/
   curl http://localhost:8000/recent-tracks/?limit=5
   ```

## Environment Variables

- `SPOTIFY_CLIENT_ID` - Your Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` - Your Spotify API client secret  
- `SPOTIFY_REFRESH_TOKEN` - Your Spotify refresh token
- `DEBUG` - Django debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts 