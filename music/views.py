from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Song, Singer, Comment
from .forms import CommentForm
import time

def get_display_pages(current_page, total_pages):
    display_pages = [1]
    
    if current_page > 4:
        display_pages.append(None)  # None表示省略号
    
    for i in range(current_page - 2, current_page + 3):
        if 1 < i < total_pages:
            display_pages.append(i)
    
    if current_page < total_pages - 3:
        display_pages.append(None)  # None表示省略号
    
    if total_pages > 1:
        display_pages.append(total_pages)
    
    return display_pages

def song_list(request):
    query = request.GET.get('q', '')
    song_queryset = Song.objects.filter(song_name__icontains=query)
    paginator = Paginator(song_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    display_pages = get_display_pages(page_obj.number, paginator.num_pages)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'display_pages': display_pages,
    }
    
    return render(request, 'music/song_list.html', context)

def song_detail(request, song_id):
    song = get_object_or_404(Song, song_id=song_id)
    comments = song.comments.order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = song
            comment.save()
            return redirect('song_detail', song_id=song_id)
    else:
        form = CommentForm()
    return render(request, 'music/song_detail.html', {'song': song, 'comments': comments, 'form': form})

def singer_list(request):
    singers = Singer.objects.all()
    paginator = Paginator(singers, 10)  # 每页10位歌手
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    display_pages = get_display_pages(page_obj.number, paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'display_pages': display_pages,
    }
    
    return render(request, 'music/singer_list.html', context)

def singer_detail(request, singer_id):
    singer = get_object_or_404(Singer, singer_id=singer_id)
    return render(request, 'music/singer_detail.html', {'singer': singer})

def search(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type', 'song')  # 默认为'song'
    start_time = time.time()
    
    results = []
    elapsed_time = 0
    result_count = 0

    if query:
        if search_type == 'song':
            query_filter = (
                Q(song_name__icontains=query) |
                Q(lyrics__icontains=query) |
                Q(singer__singer_name__icontains=query)
            )
            results = Song.objects.filter(query_filter).distinct()

            # 计算权重
            for result in results:
                result.weight = 0
                if query in result.song_name:
                    result.weight += 3  # 歌曲名权重最高
                if query in result.singer.singer_name:
                    result.weight += 2  # 歌手名权重次高
                if query in result.lyrics:
                    result.weight += 1  # 歌词权重最低
            results = sorted(results, key=lambda x: x.weight, reverse=True)
        else:
            query_filter = (
                Q(singer_name__icontains=query) |
                Q(bio__icontains=query)
            )
            results = Singer.objects.filter(query_filter).distinct()

            # 计算权重
            for result in results:
                result.weight = 0
                if query in result.singer_name:
                    result.weight += 2  # 歌手名权重较高
                if query in result.bio:
                    result.weight += 1  # 简介权重较低
            results = sorted(results, key=lambda x: x.weight, reverse=True)

        end_time = time.time()
        elapsed_time = end_time - start_time
        result_count = len(results)

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    display_pages = get_display_pages(page_obj.number, paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
        'elapsed_time': elapsed_time,
        'result_count': result_count,
        'display_pages': display_pages,
    }
    
    return render(request, 'music/search_results.html', context)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    song_id = comment.song.song_id
    comment.delete()
    return redirect('song_detail', song_id=song_id)
