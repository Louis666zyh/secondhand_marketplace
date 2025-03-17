from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    """Render the main homepage."""
    return render(request, "index.html")


def login_page(request):
    return render(request, "login.html")


def chat_page(request):
    return render(request, "chat.html")


@login_required
def sell_item_view(request):
    return render(request, 'frontend/sell_item.html')
