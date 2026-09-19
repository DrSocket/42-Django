"""
ex00 - a login/logout system that talks to the server only through AJAX.

The page at /account renders one of two states. Both states also exist as
partial templates so that the AJAX endpoints can return the *same* markup the
initial page render used; that is what lets the page swap states without ever
being refreshed, while a manual refresh still lands on the correct state.
"""

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST


def _logged_in_html(request):
    """Markup for the 'Logged as <user>' state."""
    return render_to_string("account/_logged_in.html", request=request)


def _logged_out_html(request, form=None):
    """Markup for the login form state, optionally carrying form errors."""
    return render_to_string(
        "account/_logged_out.html",
        {"form": form if form is not None else AuthenticationForm()},
        request=request,
    )


def _register_html(request, form=None, success=None):
    """Markup for the create-account form, with errors or a success message."""
    return render_to_string(
        "account/_register.html",
        {"reg_form": form if form is not None else UserCreationForm(), "reg_success": success},
        request=request,
    )


@require_GET
def account(request):
    """
    The /account page.

    Rendered server-side so that a manual refresh returns to the behaviour the
    page had before refreshing, without replaying any error state.
    """
    return render(request, "account/account.html", {"form": AuthenticationForm()})


@require_POST
def login(request):
    """Log a user in. Reached only by an AJAX POST."""
    form = AuthenticationForm(request, data=request.POST)
    if not form.is_valid():
        # Re-render the form bound to the submitted data so its errors show.
        return JsonResponse(
            {"authenticated": False, "html": _logged_out_html(request, form)}
        )

    auth_login(request, form.get_user())
    return JsonResponse({"authenticated": True, "html": _logged_in_html(request)})


@require_POST
def logout(request):
    """Log the current user out. Reached only by an AJAX POST."""
    auth_logout(request)
    return JsonResponse({"authenticated": False, "html": _logged_out_html(request)})


@require_POST
def register(request):
    """
    Create a user from the page, over AJAX (not part of the subject).

    Uses Django's UserCreationForm, so the password validators apply and any
    errors come back rendered into the same form, exactly like login does.
    """
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"created": False, "html": _register_html(request, form)})

    user = form.save()
    return JsonResponse(
        {
            "created": True,
            "html": _register_html(
                request,
                success=f"User '{user.get_username()}' created — you can now log in.",
            ),
        }
    )
