from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.chat.models import Message


def login_page(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            error_message = "Invalid username or password."
            return render(request, "registration/login.html", {"error_message": error_message})
    return render(request, "registration/login.html")

@login_required
def sell_item_view(request):
    return render(request, 'sell_item.html')

@login_required
def chat_page(request):
    return render(request, "chat.html")

@login_required
def account_page(request):
    return render(request, 'account.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def homepage(request):
    return render(request, 'index.html',{'user': request.user})

@login_required
def index_view(request):
    recent_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')[:5]
    return render(request, 'index.html', {'user': request.user, 'recent_messages': recent_messages})

@login_required
def transaction_confirmation_view(request, transaction_id):
    return render(request, "transactions/confirmation.html", {
        "transaction_id": transaction_id
    })