import time
from random import choice

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission

from .forms import MsgForm, TipForm
from .models import TipDay

SESSION_TIME = 42
# Create your views here.
def index(request):
    form = None


    if not request.user.is_authenticated:
        print (request.session.get('anon_user'))
        if request.session.get('anon_user') == None:
            request.session["anon_user"] = choice(settings.ANONYMOUS_NAME)
        if request.session.get("last_change_nick") is None:
            request.session["last_change_nick"] = time.time()
        if time.time() - request.session.get("last_change_nick") >= SESSION_TIME:
            request.session["last_change_nick"] = time.time()
            old_username = request.session.get("anon_user")
            while True:
                new_username = choice(settings.ANONYMOUS_NAME)
                if old_username != new_username:
                    break
            request.session["anon_user"] = new_username

    else:
        if request.method == "POST":
            form = TipForm(request.POST)
            if form.is_valid():
                TipDay.objects.create(author=request.user, content=form.cleaned_data['content'])
                # load page with new tweet
                return redirect("ex:index")
        else:
            form = TipForm()
    tips = TipDay.objects.all() # ordered by date via meta
    return render(request, "ex/index.html", {"form": form, "tips": tips})


def register(request):
    if request.user.is_authenticated:
        return redirect("ex:index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            raw_password2 = form.cleaned_data.get("password2")
            if raw_password != raw_password2:
                return render(
                    request, "ex/register.html", {"message": "Passwords must match."}
                )
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("ex:index")
    else:
        form = UserCreationForm()
    return render(request, "ex/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("ex:index")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("ex:index")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return redirect("ex:index")
            else:
                form = AuthenticationForm()
                return render(
                    request,
                    "ex/login.html",
                    {"message": "Invalid username and/or password.", "form": form},
                )
    else:
        form = AuthenticationForm()
    return render(request, "ex/login.html", {"form": form})


@login_required
def like(request, tip_id):
    tip = get_object_or_404(TipDay, pk=tip_id)

    if request.user in tip.likes.all():
        tip.likes.remove(request.user)
    else:
        tip.likes.add(request.user)
        if request.user in tip.dislikes.all():
            tip.dislikes.remove(request.user)

    return redirect("ex:index")

@login_required(login_url='/login/')
def dislike(request, tip_id):
    tip = get_object_or_404(TipDay, pk=tip_id)

    if request.user in tip.dislikes.all():
        tip.dislikes.remove(request.user)
    else:
        tip.dislikes.add(request.user)
        if request.user in tip.likes.all():
            tip.likes.remove(request.user)

    return redirect("ex:index")

@login_required(login_url='/login/')
def del_view(request, tip_id):
    tip = get_object_or_404(TipDay, pk=tip_id)

    if tip.author != request.user:
        if not request.user.is_authenticated: 
            raise PermissionDenied()
    tip.delete()

    return redirect("ex:index")