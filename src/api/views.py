from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import asyncio
from aiohttp import ClientSession

from .strava_config import STRAVA_API_ENDPOINTS, BOUNDS, STRAVA_TOKEN

import sys

sys.setrecursionlimit(10000)  # 10000 is an example, try with different values

"""
Using Strava API (https://strava.github.io/api/), find the most popular 10 cycling segments in Istanbul,
and check their leaderboards (First 50). Return a dictionary of riders only in multiple leaderboards,
and how many time they are listed in those leaderboards. (Endpoint 1)

"""


class SegmentLeaderboardRiderCountAPIView(APIView):
    def get(self, request):
        segment_ids = self.get_segments_ids()
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.get_leaderboards(segment_ids))
        loop.run_until_complete(future)

        return Response(future)

    def get_segments_ids(self):
        ENDPOINT = STRAVA_API_ENDPOINTS.get('segments_explore')
        payload = {
            'access_token': STRAVA_TOKEN,
            'bounds': BOUNDS.get('istanbul'),
            'activity_type': 'riding',
        }

        response = requests.get(ENDPOINT, params=payload)
        return [segment['id'] for segment in response.json().get('segments', [])]

    async def get_leaderboards(self, segment_ids):
        ENDPOINT = STRAVA_API_ENDPOINTS.get('leaderboards')
        payload = {
            'access_token': STRAVA_TOKEN,
            'per_page': 50
        }
        tasks = []
        async with ClientSession() as session:
            for segment_id in segment_ids:
                task = asyncio.ensure_future(self.fetch(ENDPOINT.format(segment_id), session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

        return responses

    async def fetch(self, url, session):
        async with session.get(url) as response:
            return await response.read()


class LeaderBoardsAPIView(APIView):
    def get(self, request):
        params = {
            'id': '2260881',
            'access_token': '3896fd10e37dcef3bfa4108866caf1e14f1c0ebc'
        }

        response = requests.get(f"https://www.strava.com/api/v3/segments/{params.get('id')}/leaderboard",
                                params={
                                    'access_token': '3896fd10e37dcef3bfa4108866caf1e14f1c0ebc'
                                })

        return Response(response.json())
