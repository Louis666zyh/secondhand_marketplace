from django.urls import path
from .views import login_page, chat_page, homepage, sell_item_view

urlpatterns = [
    path("login/", login_page, name="login"),
    path("chat/", chat_page, name="chat"),
    path("", homepage, name="homepage"),
    path('sell-item/', sell_item_view, name='sell_item'),
]
