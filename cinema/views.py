from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# from django.db.models import Q, Avg
from django.db.models import Avg
from .models import Video
from rating.models import Rating
from django.shortcuts import redirect

@login_required
def home(request):
    if request.user.profile.is_expired:
        return redirect('profile')
    selected_genre = request.GET.get('genre', '')
    title = request.GET.get('title', '')
    videos = Video.objects.all()

    if selected_genre:
        videos = videos.filter(genre=selected_genre)

    if title and len(title) >= 3:
        # videos = videos.filter(Q(title__icontains=title))
        videos = videos.filter(title__icontains=title)

    genres = Video.objects.values_list('genre', flat=True).distinct()
    return render(request, 'cinema/home.html', {'videos': videos, 'genres': genres, 'selected_genre': selected_genre, 'title': title})

@login_required
def detail(request, video_id):
    if request.user.profile.is_expired:
        return redirect('profile')
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        Rating.objects.update_or_create(user=request.user, video=video, defaults={'rating': rating})
    user_has_voted = Rating.objects.filter(user=request.user, video=video).exists()
    average_rating = Rating.objects.filter(video=video).aggregate(Avg('rating'))['rating__avg']
    votes = Rating.objects.filter(video=video).count()
    return render(request, 'cinema/detail.html', {'video': video, 'average_rating': average_rating, 'votes': votes, 'user_has_voted': user_has_voted})