import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

ZOOM_OAUTH_URL = "https://zoom.us/oauth/token"
ZOOM_API_BASE_URL = "https://api.zoom.us/v2"

def get_zoom_access_token(code):
    """Exchange authorization code for access token."""
    url = f"{ZOOM_OAUTH_URL}?grant_type=authorization_code&code={code}&redirect_uri={settings.ZOOM_REDIRECT_URI}"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET),
    )
    return response.json()

def refresh_zoom_access_token(refresh_token):
    """Refresh access token using the refresh token."""
    url = f"{ZOOM_OAUTH_URL}?grant_type=refresh_token&refresh_token={refresh_token}"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET),
    )
    return response.json()

def create_zoom_meeting(access_token, topic, start_time, duration):
    """Create a Zoom meeting using the API."""
    url = f"{ZOOM_API_BASE_URL}/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time.isoformat(),  # ISO format
        "duration": duration,  # Duration in minutes
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "approval_type": 0,
            "waiting_room": True,
        },
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
