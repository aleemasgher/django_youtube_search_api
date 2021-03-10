import requests

from django.conf import settings
from django.http import JsonResponse
from django.utils.dateparse import parse_duration
from django.views.generic import TemplateView
from rest_framework.views import APIView


class Index(TemplateView):
    template_name = 'search_yt/index.html'


class GetSearchResults(APIView):

    def post(self, request, *args, **kwargs):

        if request.data.get('search'):
            videos = []
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'

            search_params = {
                'part': 'snippet',
                'q': request.data.get('search'),
                'key': settings.YT_API_KEY,
                'maxResults': 9,
                'type': 'video'
            }

            r = requests.get(search_url, params=search_params)

            results = r.json()['items']

            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

            video_params = {
                'key': settings.YT_API_KEY,
                'part': 'snippet,contentDetails',
                'id': ','.join(video_ids),
                'maxResults': 9
            }

            r = requests.get(video_url, params=video_params)

            results = r.json()['items']

            for result in results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']
                }

                videos.append(video_data)

            return JsonResponse({'data': videos})
        else:
            return JsonResponse({'error': 'Please search something.'})
