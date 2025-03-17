from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def homepage(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, "login.html")

@login_required
def chat_page(request):
    return render(request, "chat.html")

@login_required
def sell_item_view(request):
    return render(request, 'sell_item.html')

@login_required
def account_page(request):
    return render(request, 'account.html')

def logout_view(request):
    logout(request)
    return redirect('home')