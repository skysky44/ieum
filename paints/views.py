from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Paint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
import base64
import uuid

# Create your views here.
@login_required
def index(request):
    paints = Paint.objects.order_by('-pk')
    page = request.GET.get('page', '1')
    per_page = 10
    paginator = Paginator(paints, per_page)
    page_obj = paginator.get_page(page)
    POSITIONS = [
        {'top': '10px', 'left': '200px'},
        {'top': '10px', 'left': '320px'},
        {'top': '100px', 'left': '30px'},
        {'top': '150px', 'left': '150px'},
        {'top': '160px', 'left': '360px'},
        {'top': '200px', 'left': '500px'},
        {'top': '270px', 'left': '30px'},
        {'top': '270px', 'left': '210px'},
        {'top': '400px', 'left': '84px'},
        {'top': '350px', 'left': '500px'},
    ]
    paint_positions = list(zip(page_obj, POSITIONS))
    context = {
        'paint_positions' : paint_positions,
        'paints': page_obj,
    }
    return render(request, 'paints/index.html', context)


@csrf_exempt
@login_required
def create(request):
    if request.method == 'POST':
        image_data = request.POST['image']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        new_paint = Paint(user=request.user)
        new_paint.image.save(f"{uuid.uuid4()}.png", data)
        new_paint.save()

        return JsonResponse({'status': 'success'})
    else:
        return render(request, 'paints/create.html')
    

@login_required
def detail(request, paint_pk):
    paint = Paint.objects.get(pk=paint_pk)

    return render(request, 'paints/detail.html', { 'paint': paint })


@csrf_exempt
@login_required
def update(request, paint_pk):
     
    paint = Paint.objects.get(pk=paint_pk)
    if request.user == paint.user:
        if request.method == 'POST':
            image_data = request.POST['image']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

            # 기존 이미지 삭제
            if paint.image:
                paint.image.delete()

            # 새로운 이미지 저장
            paint.image.save(f"{uuid.uuid4()}.png", data)
            paint.save()

            return JsonResponse({'status': 'success'})
        else:
            context = {
                'paint': paint, 
                'paint_pk': paint_pk
                }
            return render(request, 'paints/update.html', context)
    else:
        return redirect('paints:index')



@login_required
def delete(request, paint_pk):
    paint = Paint.objects.get(pk=paint_pk)
    if request.user == paint.user:
        paint.delete()

    return redirect('paints:index')



@login_required
def like_users(request, paint_pk):
    paint = Paint.objects.get(pk=paint_pk)
    if request.user in paint.like_users.all():
        paint.like_users.remove(request.user)
        is_like = False
    else:
        paint.like_users.add(request.user)
        is_like = True
    context = {
        'is_like': is_like,
        'paint_likes_count': paint.like_users.count()
    }
    return JsonResponse(context)