import requests
import base64
import time
from rb.utils.env import get_env_variable

class SpotifyClient:
    def __init__(self):
        self.client_id = get_env_variable("SPOTIFY_CLIENT_ID")
        self.client_secret = get_env_variable("SPOTIFY_CLIENT_SECRET")
        self.refresh_token = get_env_variable("SPOTIFY_REFRESH_TOKEN")
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_url = "https://api.spotify.com/v1/me/player/recently-played"
        self.access_token = None
        self.token_expires_at = 0

    def _is_token_expired(self):
        return time.time() >= self.token_expires_at

    def _refresh_access_token(self):
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        response = requests.post(
            self.token_url,
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
            headers={"Authorization": f"Basic {auth_header}"},
        )

        if response.status_code != 200:
            raise Exception("Failed to refresh access token.")

        data = response.json()
        self.access_token = data["access_token"]
        self.token_expires_at = time.time() + data.get("expires_in", 3600)

    def _get_access_token(self):
        if self.access_token is None or self._is_token_expired():
            self._refresh_access_token()
        return self.access_token

    def get_recent_tracks(self, limit=10):
        access_token = self._get_access_token()

        response = requests.get(
            self.api_url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": limit},
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch recent tracks.")

        data = response.json()

        return [
            {
                "track": item["track"]["name"],
                "artist": item["track"]["artists"][0]["name"],
                "played_at": item["played_at"],
            }
            for item in data.get("items", [])
        ] 