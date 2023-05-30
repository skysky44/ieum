from django.shortcuts import render, redirect
from .models import Paint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import uuid

# Create your views here.
def index(request):
    paints = Paint.objects.all()
    return render(request, 'paints/index.html', { 'paints' : paints })


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