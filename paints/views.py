from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Paint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import uuid

# Create your views here.
def index(request):
    paints = Paint.objects.order_by('-pk')
    page = request.GET.get('page', '1')
    per_page = 6
    paginator = Paginator(paints, per_page)
    page_obj = paginator.get_page(page)
    POSITIONS = [
        {'top': '20%', 'left': '8%'},
        {'top': '45%', 'left': '9%'},
        {'top': '6%', 'left': '28%'},
        {'top': '26%', 'left': '40%'},
        {'top': '32%', 'left': '80%'},
        {'top': '10%', 'left': '50%'},
    ]
    paint_positions = list(zip(page_obj, POSITIONS))
    context = {
        'paint_positions' : paint_positions,
        'paints': page_obj,
    }
    return render(request, 'paints/index.html', context)


@csrf_exempt
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
    

def detail(request, paint_pk):
    paint = Paint.objects.get(pk=paint_pk)
    return render(request, 'paints/detail.html', { 'paint': paint })


def delete(request, paint_pk):
    paint = Paint.objects.get(pk=paint_pk)
    if request.user == paint.user:
        paint.delete()
    return redirect('paints:index')

def likes(request, paint_pk):
    paint = paint.objects.get(pk=paint_pk)
    if paint.like_users.filter(pk=request.user.pk).exists():
        paint.like_users.remove(request.user)
    else:
        paint.like_users.add(request.user)

    return redirect('paints:index')
