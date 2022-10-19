from django.shortcuts import render


def ex00View(request):
    return render(request, "index.html")