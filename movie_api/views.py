
from rest_framework.views import APIView
from rest_framework.response import Response
from movie_api.ghibli import GhibliApi as api
from movie_api_project.settings import GHIBILI_KEY
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from functools import wraps
from django.http import JsonResponse

def authenticate_api_key(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        input_key = request.headers.get('ghiblikey')
        if input_key:
            from movie_api_project.settings import GHIBILI_KEY  # Import GHIBILI_KEY here or set it in the settings module
            if input_key in GHIBILI_KEY:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'error': 'Invalid ghibilikey'}, status=401)
        else:
            return JsonResponse({'error': 'ghiblikey not provided'}, status=401)

    return _wrapped_view


# def authenticate_api_key(request):
#     input_key = request.headers.get('ghiblikey')
#     if input_key:
#         if input_key in GHIBILI_KEY:
#             return {'is_auth':True , 'message': 'successfully authenticated'} 
#         else:
#             return  {'is_auth': False , 'message': 'invalid ghibilikey'} 
#     else :
#             return  {'is_auth': False , 'message': 'ghibilikey not provided'} 


@method_decorator(authenticate_api_key, name='get')
@method_decorator(cache_page(60), name='get')
class MoviesListView(APIView):
    def get(self, request):
        print(request)

        return Response(data=api.get_film_list_with_cast(), status=200)

