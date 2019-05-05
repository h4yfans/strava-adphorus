import os

STRAVA_API_ENDPOINTS = {
    'segments_explore': 'https://www.strava.com/api/v3/segments/explore',
    'leaderboards': 'https://www.strava.com/api/v3/segments/{segment_id}/leaderboard'
}

BOUNDS = {
    'istanbul': '40.9040111998,28.5151415569,41.3451551851,29.3212487527'
}

STRAVA_TOKEN = os.environ.get('STRAVA_TOKEN')
