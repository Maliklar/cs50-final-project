from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('practice', views.practice_view, name="practice"),
    path('registration', views.registration, name="registration"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('profile/<str:username>', views.profile_view, name="profile"),
    path('quotes', views.quotes, name="quotes"),
    path('quotes/<int:id>', views.view_quote, name="view_quote"),
    path('players', views.players, name="players"),

    ## APIs
    path('post_quote', views.post_quote, name="post_quote"),
    path('rand_quote', views.rand_quote, name='rand_quote'), ## This API is for retriving a random quote for practice page
    path('new_record', views.new_record, name="new_record"), ## After user finish typing a new record will be stored in a database
    path('like', views.like_quote, name="like"), ## User likes the quote
    path('dislike', views.dislike_quote, name="dislike"), ## User dislikes quote
]
