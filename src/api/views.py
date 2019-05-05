from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import get_multiple_leaders, get_leaders_with_score


class RiderCountAPIView(APIView):
    """
    Using Strava API (https://strava.github.io/api/), find the most popular 10 cycling segments in Istanbul,
    and check their leaderboards (First 50). Return a dictionary of riders only in multiple leaderboards,
    and how many time they are listed in those leaderboards. (Endpoint 1)

    """

    def get(self, request):
        get_leaders = get_multiple_leaders()

        return Response(get_leaders)


class LeaderBoardsAPIView(APIView):
    """
    Calculate a score for each rider listed in those segments and return your highscore list. (Endpoint 2).
    Be creative and try to be fair with score calculation. Document which variables you are using for score
    calculation and the score formula.
    """

    def get(self, request):
        get_score = get_leaders_with_score()

        return Response(get_score)
