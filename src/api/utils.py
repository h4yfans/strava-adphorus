import asyncio
import itertools
import logging

import requests
import aiohttp

from .strava_config import (
    STRAVA_API_ENDPOINTS,
    STRAVA_TOKEN,
    BOUNDS
)


def get_multiple_leaders():
    segments = get_segments()
    segment_ids = [segment['id'] for segment in segments]
    leaderboards = get_leaderboards_by_segment_id(segment_ids)

    merged_leaderboard_list = (list(
        (itertools.chain.from_iterable
         (leaderboard.result()['entries'] for leaderboard in leaderboards[0]))))

    athletes = {}
    for athlete in merged_leaderboard_list:
        if athlete['athlete_name'] not in athletes:
            athletes[athlete['athlete_name']] = {
                'athlete_name': athlete['athlete_name'],
                'count': 1,
            }
        else:
            athletes[athlete['athlete_name']]['count'] += 1

    multiple_riders = {k: v for k, v in athletes.items() if v['count'] > 1}
    multiple_riders = sorted(multiple_riders.values(), key=lambda x: x['count'], reverse=True)

    return multiple_riders


def get_segments():
    endpoint = STRAVA_API_ENDPOINTS.get('segments_explore')
    payload = {
        'access_token': STRAVA_TOKEN,
        'bounds': BOUNDS.get('istanbul'),
        'activity_type': 'riding',
    }
    try:
        response = requests.get(endpoint, params=payload)
        if response.ok:
            return response.json().get('segments', [])

        return []
    except Exception as e:
        raise Exception(f'Strava not responding {e}')


def get_leaderboards_by_segment_id(segment_ids):
    endpoint = STRAVA_API_ENDPOINTS.get('leaderboards')
    payload = {
        'access_token': STRAVA_TOKEN,
        'per_page': 50
    }
    urls = [endpoint.format(segment_id=segment_id) for segment_id in segment_ids]
    futures = [_call_url(url, payload) for url in urls]
    leaderboards = asyncio.run(asyncio.wait(futures))
    return leaderboards


def get_leaders_with_score():
    endpoint = STRAVA_API_ENDPOINTS.get('leaderboards')
    segments = get_segments()
    payload = {
        'access_token': STRAVA_TOKEN,
        'per_page': 50
    }

    athletes_dict = {}
    for segment in segments:
        athletes = requests.get(endpoint.format(segment_id=segment['id']), params=payload).json().get('entries')
        for athlete in athletes:
            rank = athlete['rank']
            elev_diff = segment['elev_difference']
            if athlete['athlete_name'] not in athletes_dict:
                athletes_dict[athlete['athlete_name']] = {
                    'athlete_name': athlete['athlete_name'],
                    'total_distance': segment['distance'],
                    'total_moving_time': athlete['moving_time'],
                    'count': 1,
                    'rank': [rank],
                    'elev_diff': [elev_diff],
                }
            else:
                athletes_dict[athlete['athlete_name']]['total_distance'] += segment['distance']
                athletes_dict[athlete['athlete_name']]['total_moving_time'] += athlete['moving_time']
                athletes_dict[athlete['athlete_name']]['count'] += 1
                athletes_dict[athlete['athlete_name']]['rank'].append(rank)
                athletes_dict[athlete['athlete_name']]['elev_diff'].append(elev_diff)

    for _, v in enumerate(athletes_dict):
        athletes_dict[v]['avg_speed'] = int(athletes_dict[v]['total_distance'] / athletes_dict[v]['total_moving_time'])
        elev_diff = athletes_dict[v]['elev_diff']
        athletes_dict[v]['avg_elev_diff'] = int(sum(elev_diff) / float(len(elev_diff)))

    return calculate_score(athletes_dict)


def calculate_score(athletes):
    """
        Calculation:
        - avg_speed:        The average riding speed for all the distance travelled
                            within the given boundaries. If riders too slow or too fast
                            it's impact their score
        - avg_elev_diff:    The average of the segments's elevation difference
        - count:            This displays the how many time they are listed in those leaderboards
        - rank:             Contains all the rank that riders won Example: [3,5,10,1]
        - rank_score:       If the rider's rank in certain range, rider gets extra points

        formula: (avg_speed * avg_elev_diff * rank_score * count) /1000
    """

    for athlete in athletes:
        athlete = athletes.get(athlete)
        avg_speed = athlete['avg_speed']
        avg_elev_diff = athlete['avg_elev_diff']
        count = athlete['count']
        rank = athlete['rank']

        first_three = list(range(1, 4))
        four_ten = list(range(4, 11))

        if any(elem in first_three for elem in rank):
            rank_score = 50
        elif any(elem in four_ten for elem in rank):
            rank_score = 30
        else:
            rank_score = 10

        athlete['score'] = (avg_speed * avg_elev_diff * rank_score * count) / 1000

        _create_score_dict(athlete)

    athletes = sorted(athletes.values(), key=lambda x: x['score'], reverse=True)

    return athletes


async def _call_url(url, payload):
    print('Starting {}'.format(url))
    try:
        response = await aiohttp.ClientSession().get(url, params=payload, verify_ssl=False)
        data = await response.json()
        if response.status is not 200:
            logging.error(f'Leaderboard status code {response.status}')
        return data
    except Exception as e:
        raise Exception(f'Strava not responding {e}')


def _create_score_dict(athlete):
    athlete.pop('total_distance', 'total_moving_time')
    athlete.pop('total_moving_time')
    athlete.pop('count')
    athlete.pop('elev_diff')
    athlete.pop('avg_speed')
    athlete.pop('avg_elev_diff')
    athlete.pop('rank')

    return athlete
