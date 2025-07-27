from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
import csv
import json
from datetime import datetime

def home_view(request):
    """Home page view with track functionality."""
    limit = request.GET.get("limit", 10)
    export_format = request.GET.get("format", "")
    
    try:
        limit = int(limit)
        if not (1 <= limit <= 50):
            raise ValueError("Limit must be between 1 and 50")
    except ValueError as e:
        if export_format:
            return JsonResponse({"error": str(e)}, status=400)
        return render(request, 'home.html', {
            'error': str(e),
            'limit': 10
        })

    try:
        from rb.services.spotify_client import SpotifyClient
        client = SpotifyClient()
        tracks = client.get_recent_tracks(limit=limit)
        
        # Handle export formats
        if export_format == "json":
            return JsonResponse({"tracks": tracks})
        elif export_format == "csv":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="recent_tracks_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Track', 'Artist', 'Played At'])
            for track in tracks:
                writer.writerow([track['track'], track['artist'], track['played_at']])
            return response
        
        # Render template for web view
        return render(request, 'home.html', {
            'tracks': tracks,
            'limit': limit,
            'error': None
        })
        
    except Exception as e:
        if export_format:
            return JsonResponse({"error": str(e)}, status=500)
        return render(request, 'home.html', {
            'error': str(e),
            'limit': limit,
            'tracks': None
        })

def test_env_view(request):
    """Test view to check environment variables."""
    return JsonResponse({
        "spotify_client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "spotify_client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "spotify_refresh_token": os.getenv("SPOTIFY_REFRESH_TOKEN"),
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
    })

def recent_tracks_view(request):
    """Legacy view for recent tracks - redirects to home."""
    return home_view(request) 