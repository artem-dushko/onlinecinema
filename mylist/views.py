from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import WatchList
from cinema.models import Video

def toggle_watch_list(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    watch_list, created = WatchList.objects.get_or_create(user=request.user)
    if video in watch_list.videos.all():
        watch_list.videos.remove(video)
        added = False
    else:
        watch_list.videos.add(video)
        added = True
    return JsonResponse({'added': added})

@login_required
def mylist(request):
    user = request.user
    try:
        watch_list = WatchList.objects.get(user=user)
        videos = watch_list.videos.all()
    except WatchList.DoesNotExist:
        videos = []
    return render(request, 'mylist/mylist.html', {'watch_list': videos})