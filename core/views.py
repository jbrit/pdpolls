from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
import string

from .models import Category, VoteItem, Profile

class HomePage(TemplateView):
    template_name = "core/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({ "categories": Category.objects.all() })
        return context
    


# Non View Functions
def send_password(user, password, request):
    message = render_to_string('core/password_sent_email.txt', {
        'password': password,
        'domain': get_current_site(request).domain
        })
    user.email_user("Password Mail", message)


def random_string_digits(string_length=6):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))



def detail(request, slug):
    context = {}
    category = get_object_or_404(Category, slug=slug)
    category_list = Category.objects.order_by('id')
    p = Paginator(category_list, 1)
    for i in p.page_range:
        if category in p.page(i).object_list:
            page = p.page(i)
            if page.has_next():
                next_slug = p.page(i+1).object_list[0].slug
                context["next_slug"] = next_slug
            if page.has_previous():
                prev_slug = p.page(i-1).object_list[0].slug
                context["prev_slug"] = prev_slug
            break
    context.update({
        "category": category,
        "page": page,
    })
    return render(request, 'core/detail.html', context)


def login_view(request):
    alert = None
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        email = request.POST.get("login-email")
        password = request.POST.get("login-password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            alert = {
                'text': 'Invalid Login Details!',
                'class': 'danger'
            }
    context = {
        "login": True,
        "register": False,
        "alert": alert
    }
    return render(request, 'core/auth.html', context)


def register(request):
    alert = None
    User = get_user_model()
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            context = {
                "login": False,
                "register": True,
                "alert": {
                    'text': 'Email exists!',
                    'class': 'danger'
                }
            }
            return render(request, 'core/auth.html', context)

        password = f"lmu-{random_string_digits()}"
        try:
            u = User.objects.create_user(email=email, password=password)
        except Exception:
            return redirect("/login")
        u.save()
        send_password(u, password, request)
        alert = {
            'text': 'The Password has been sent to your email!',
            'class': 'success'
        }

    context = {
        "login": False,
        "register": True,
        "alert": alert
    }
    return render(request, 'core/auth.html', context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")

@login_required
def vote(request, id):
    if request.method == "POST":
        user = request.user
        profile = get_object_or_404(Profile, person=user)
        item = get_object_or_404(VoteItem, id=id)
        if user.is_staff:
            raise Http404("No admin can vote")
        if item.category in profile.categories_voted.all():
            raise Http404("No more votes for this category")
        profile.votes.add(item)
        profile.categories_voted.add(item.category)
        profile.save()
        return redirect("/%s"%item.category.slug)
    else:
        raise Http404("Invalid Vote Request Type")