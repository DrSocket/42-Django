from django.shortcuts import render

# Create your views here.
def index(request):
    step = 255 / 50
    context = {
        "range": [
            "{:02X}".format(int(i * step)) for i in range(51)
        ]
    }
    return render(request, 'ex03/index.html', context)