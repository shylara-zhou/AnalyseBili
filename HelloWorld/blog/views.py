from django.shortcuts import render
from django.http import HttpResponse
from blog import draw


from blog import analyse

# Create your views here.
def hello(request):
    return HttpResponse("Hello world !	This is my first app! ")


def drawcipin(request):
    try:
        # if request.method == 'POST':
        analyse.drawcipin()
        return render(request, 'bvid.html')
    except KeyError:
        return render(request, 'error.html')
    except MemoryError:
        return render(request, 'MemoryError.html')
    except IndexError:
        return render(request, 'error.html')

def tryit(request):
    try:
        if request.method == 'POST':
            bvid = request.POST['bvid']
            draw.draw(bvid)
        return render(request, 'bvid.html')
    except IndexError:
        return render(request, 'error.html')


def getdata(request):
    with open('./blog/favorite.txt', 'r', encoding='utf8') as fp:
        str = fp.read()
        return HttpResponse(str)

