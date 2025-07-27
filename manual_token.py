#!/usr/bin/env python3
"""
Manual Spotify Token Exchange
Use this script to exchange your authorization code for tokens.
"""

import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def exchange_code_for_tokens(auth_code):
    """Exchange authorization code for tokens."""
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Error: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in .env file")
        return None
    
    token_url = "https://accounts.spotify.com/api/token"
    redirect_uri = "http://127.0.0.1:8888/callback"
    
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }
    
    # Create Basic auth header
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        response.raise_for_status()
        
        tokens = response.json()
        
        print("✅ Successfully obtained tokens!")
        print(f"📝 Access Token: {tokens.get('access_token', 'N/A')[:20]}...")
        print(f"🔄 Refresh Token: {tokens.get('refresh_token', 'N/A')[:20]}...")
        print(f"⏰ Expires In: {tokens.get('expires_in', 'N/A')} seconds")
        
        return tokens.get('refresh_token')
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error exchanging code for tokens: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def update_env_file(refresh_token):
    """Update the .env file with the new refresh token."""
    env_file = ".env"
    
    # Read current .env file
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ {env_file} file not found")
        return False
    
    # Update or add SPOTIFY_REFRESH_TOKEN
    updated = False
    for i, line in enumerate(lines):
        if line.startswith("SPOTIFY_REFRESH_TOKEN="):
            lines[i] = f"SPOTIFY_REFRESH_TOKEN={refresh_token}\n"
            updated = True
            break
    
    if not updated:
        lines.append(f"SPOTIFY_REFRESH_TOKEN={refresh_token}\n")
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            f.writelines(lines)
        print(f"✅ Updated {env_file} with new refresh token")
        return True
    except Exception as e:
        print(f"❌ Error updating {env_file}: {e}")
        return False

def main():
    """Main function."""
    print("🎵 Manual Spotify Token Exchange")
    print("=" * 35)
    
    print("📋 Instructions:")
    print("1. Go to this URL in your browser:")
    print("   https://accounts.spotify.com/authorize?client_id=9c5cdedcada4430d9d4eea1fb0894a66&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8888%2Fcallback&scope=user-read-recently-played%20user-read-private%20user-read-email&show_dialog=true")
    print("2. Authorize the app")
    print("3. Copy the authorization code from the URL")
    print("4. Paste it here (you can paste the full URL or just the code)")
    
    auth_input = input("\n🔑 Enter the authorization code or URL: ").strip()
    
    if not auth_input:
        print("❌ No authorization code provided")
        return
    
    # Extract code from URL if full URL was pasted
    if auth_input.startswith("http"):
        # Extract code from URL like: http://127.0.0.1:8888/callback?code=AQD...
        if "code=" in auth_input:
            auth_code = auth_input.split("code=")[1].split("&")[0]
            print(f"✅ Extracted code: {auth_code[:20]}...")
        else:
            print("❌ No authorization code found in URL")
            return
    else:
        auth_code = auth_input
    
    # Exchange code for tokens
    refresh_token = exchange_code_for_tokens(auth_code)
    
    if refresh_token:
        # Update .env file
        if update_env_file(refresh_token):
            print("\n🎉 Success! Your refresh token has been saved to .env file")
            print("🚀 You can now test your Spotify API:")
            print("   curl http://localhost:8000/recent-tracks/")
        else:
            print(f"\n📝 Please manually add this to your .env file:")
            print(f"SPOTIFY_REFRESH_TOKEN={refresh_token}")
    else:
        print("\n❌ Failed to get refresh token. Please try again.")

if __name__ == "__main__":
    main() 