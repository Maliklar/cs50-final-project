import json
from django.db.models.aggregates import Avg
from django.db.models.query_utils import Q

import numpy
from main.utils import quote_records_plot, user_records_plot
from main.models import Like, Quote, Records, User
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core import serializers
from django.db.models import Max


import  random
# Create your views here.
def index(request):

    ## - Getting Highest recrods
    top_quotes = Records.objects.all().order_by('-best_time')

    ## Getting Top players by average
    top_players = Records.objects.all().values('user').annotate(avg=Avg('best_time'),).order_by('-avg')
    print(top_players)
    tp_dict = {}
    for i in top_players:
        tp_dict[User.objects.get(id=i['user'])] = i['avg']

    ## Geting quotes ordered by date of publication (Recently Added Header)

    recent_quotes = Quote.objects.all().order_by('-date')
    
    print(tp_dict)
    return render(request, 'main/index.html', {
        'top_quotes' : top_quotes,
        'top_players' : tp_dict,
        'recent' : recent_quotes,
    })

def practice_view(request):
    ## Quorying all qoutes
    quotes = Quote.objects.all();
    
    

    return render(request, 'main/practice.html', {
        'quotes' : quotes
    })

def registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main/registration.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password, country=request.POST['country'], date=datetime.now())
            user.save()
        except IntegrityError:
            return render(request, "main/registration.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/registration.html")
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def profile_view(request, username):
    userInfo = User.objects.get(username= username)


    records = Records.objects.filter(user = User(userInfo.id)).order_by('-date')
    best_time = Records.objects.filter(user=User(userInfo.id)).aggregate(Max('best_time'))
    last_time = 0;
    for r in records:
        last_time = r.best_time
        break

    glob_rank = Records.objects.all().order_by('-best_time')
    world_rank = 0
    if(glob_rank.exists()):
        for record in glob_rank:
            world_rank = world_rank + 1
            if(record.user.id == userInfo.id):
                break

    local_rank = Records.objects.filter(country=userInfo.country).order_by("-best_time")
    country_rank = 0
    if(local_rank.exists()):
        for record in local_rank:
            country_rank = country_rank+1
            if(record.user.id == userInfo.id):
                break

    quotes = Quote.objects.filter(user= User(userInfo.id)).count()
    all = []
    for r in records:
        all.append(float(r.best_time))


    ## Getting user statistics graph
    records = Records.objects.filter(user=User(userInfo.id)).order_by('date')
    user_records_list = []
    y = []
    i =0 
    if(records.exists()):
        for record in records:
            i = i+1
            y.append(i)
            user_records_list.append(record.best_time)

        ## Generating a graph
        user_graph = user_records_plot(y, user_records_list, username)
    else:
        user_graph  = user_records_plot(y, user_records_list, username)

    user_graph = user_graph[len('static/'):]

    
    return render(request, 'main/profile.html', {
        'userInfo' : userInfo,
        'records' : records,
        'best_time' : best_time['best_time__max'],
        'last_time' : last_time,
        'world_rank'  : world_rank,
        'country_rank'  : country_rank,
        'games_num' : len(records),
        'publish_num' : quotes,
        'avg_speed' : round(numpy.average(all), 2),
        'graph_path' : user_graph
        
    })


@csrf_exempt
@login_required
def post_quote(request):
    if request.method != 'POST':
        return JsonResponse({"error" : "POST request is required."}, status=400)
    data = json.loads(request.body)
    print(data)
    title = data['title']
    auther = data['auther']
    content = data['content']

    insert = Quote(user=User(request.user.id), date=datetime.now(),
                   best_time=0, quote=content, auther=auther, title=title)
    insert.save()


    return JsonResponse({"result": 'True'}, status=201)

def rand_quote(request):
    query = Quote.objects.all()
    random_quote = random.choice(query)
    
    ## Getting the user the got the best record
    try:
        best_record = Records.objects.filter(
            quote=random_quote.id).aggregate(Max('best_time'))
        best_temp = Records.objects.get(
        quote=random_quote.id, best_time=best_record['best_time__max'])
        best_time = best_record['best_time__max']
        best_username = best_temp.user.username
        best_user_id = best_temp.user.id
    
    except:
        best_time = 0
        best_username = 0
        best_user_id= 0


    ## Getting the current user's best time
    try:
        your_best = Records.objects.filter(quote=random_quote.id, user=User(request.user.id)).aggregate(Max('best_time'))
        your_temp = Records.objects.get(quote=random_quote.id, best_time=your_best['best_time__max'])
        your_best_time = your_temp.best_time

    except:
        your_best_time = 0

    

    ## Getting user's ranking globally
    glob_rank = Records.objects.filter(quote=random_quote.id).order_by('-best_time')
    world_rank = 0
    if(glob_rank.exists()):
        for record in glob_rank:
            world_rank = world_rank + 1
            if(record.user.id == request.user.id):
                break

    
    ## Getting user's ranking country
    local_rank = Records.objects.filter(quote=random_quote.id, country=request.user.country).order_by("-best_time")
    country_rank = 0
    if(local_rank.exists()):
        for record in local_rank:
            country_rank = country_rank+1
            if(record.user.id == request.user.id):
                break


    ## Getting all the user's records
    records = Records.objects.filter(user=request.user.id).order_by('date')
    user_records_list = []
    y = []
    i =0 
    if(records.exists()):
        for record in records:
            i = i+1
            y.append(i)
            user_records_list.append(record.best_time)

        ## Generating a graph
        user_graph = user_records_plot(y, user_records_list, request.user.username)
    else:
        user_graph  = user_records_plot(y, user_records_list, request.user.username)

    
    ## Getting the top 20 countries for this quote
    top_countries = Records.objects.filter(quote=Quote(random_quote.id)).values('country').annotate(top=Max('best_time')).order_by('-top')
    top_country = {}
    for t in top_countries:
        top_country[t['country']] = round(t['top'], 2)


    ## Getting likes and dislikes of the quote
    likes = Like.objects.filter(quote=Quote(random_quote.id),type=True).count()
    dislikes = Like.objects.filter(quote=Quote(random_quote.id),type=False).count()

    return JsonResponse({
        'quote' : random_quote.quote,
        'id' : random_quote.id,
        'username' : random_quote.user.username,
        'user_id' : random_quote.user.id,
        'date' : random_quote.date,
        'auther' : random_quote.auther,
        'title' : random_quote.title,
        'best_user_time' : round(best_time, 2),
        'best_username' : best_username,
        'best_user_id' : best_user_id,
        'your_best_time': round(your_best_time,2),
        'your_world_rank' : world_rank,
        'your_country_rank' : country_rank,
        'user_records' : user_records_list,
        'user_graph' : user_graph,
        'top_countries' : top_country,
        'likes' : likes,
        'dislikes' : dislikes,
    })

@csrf_exempt
def new_record(request):
    if request.method != "POST":
        return JsonResponse({"notgood" : 'notgood'}, status=401)
    
    data = json.loads(request.body)    ## REMEMBER THIS LIKE TO NOT WAIST TIME IN THE FUTURE TODO:
    quote_id = data['quote_id']
    best_time = data['best_time']
    print(request.user)

    insert = Records(user=User(request.user.id), quote=Quote(quote_id), country=request.user.country, best_time=best_time, date=datetime.now())
    insert.save()
    return JsonResponse({"good" : "good"}, status=201)


@csrf_exempt
@login_required
def like_quote(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Something went wrong"}, status=205)

    data = json.loads(request.body)
    quote_id = data['quote_id']
 
    ## Check if the user interacted with quote before
    check_like = Like.objects.filter(quote=Quote(quote_id), user=User(request.user.id))
    if(check_like.exists()): ## User already interacted with the quote before
        if(check_like[0].type == True): ## User already liked the quote (no change needed)
            return JsonResponse({'message' : 'user already liked the quote'}, status= 205)
        elif(check_like[0].type == False): ## User didn't like the quote and want to change to like
            check_like.update(quote=Quote(quote_id), user=User(request.user.id), type=True)
            ## Updating the like and dislike counter on the screen 
            likes = Like.objects.filter(quote=Quote(quote_id),type=True).count()
            dislikes = Like.objects.filter(quote=Quote(quote_id),type=False).count()
    else: ## User didn't interact with the quote before and new interaction will be added here
        Like(quote=Quote(quote_id), user=User(request.user.id), type=True).save()
        likes = Like.objects.filter(quote=Quote(quote_id),type=True).count()
        dislikes = Like.objects.filter(quote=Quote(quote_id),type=False).count()

    
    return JsonResponse({
        'like': likes,
        'dislike': dislikes,
    }, status=201)


@csrf_exempt
@login_required
def dislike_quote(request):
    if request.method != "PUT":
        return JsonResponse({"error": "Something went wrong"}, status=205)

    data = json.loads(request.body)
    quote_id = data['quote_id']
    print(quote_id)
    ## Check if the user interacted with quote before
    check_like = Like.objects.filter(quote=Quote(quote_id), user=User(request.user.id))
    if(check_like.exists()): ## User already interacted with the quote before
        print(check_like)
        if(check_like[0].type == False): ## User already disliked the quote (no change needed)
            return JsonResponse({'message' : 'user already disliked the quote'}, status= 205)
        elif(check_like[0].type == True): ## User liked the quote and want to dislike it
            check_like.update(quote=Quote(quote_id), user=User(request.user.id), type=False)
            ## Updating the like and dislike counter on the screen 
            likes = Like.objects.filter(quote=Quote(quote_id),type=True).count()
            dislikes = Like.objects.filter(quote=Quote(quote_id),type=False).count()
    else: ## User didn't interact with the quote before and new interaction will be added here
        Like(quote=Quote(quote_id), user=User(request.user.id), type=False).save()
        likes = Like.objects.filter(quote=Quote(quote_id),type=True).count()
        dislikes = Like.objects.filter(quote=Quote(quote_id),type=False).count()

    return JsonResponse({
        'like' : likes,
        'dislike' : dislikes,
    }, status=201)


def quotes(request):
    if request.method == "POST":
        query = request.POST['query']
        result = Quote.objects.filter(Q(title__contains=query) | Q(auther__contains=query))
        return render(request, 'main/quotes.html', {
            "result" : result
        })
    else:
        random = Quote.objects.all().order_by('?')
        return render(request, 'main/quotes.html', {
            "result" : random
        })

def players(request):
    if request.method == "POST":
        query = request.POST['query']
        result = User.objects.filter(username__contains=query)
        return render(request, 'main/players.html', {
                "result": result
        })
    else:
        random = User.objects.all().order_by('?')
        return render(request, 'main/players.html', {
            "result": random
        })

    
def view_quote(request, id):
    quote = Quote.objects.get(id=id)

    record = Records.objects.filter(quote = Quote(id)).aggregate(Max('best_time'))
    best_wpm = record['best_time__max']

    av = Records.objects.filter(quote = Quote(id)).aggregate(Avg('best_time'))
    best_avg = av['best_time__avg']

    top_countries = Records.objects.filter(quote=Quote(id)).values('country').annotate(top=Max('best_time')).order_by('-top')
    top_country = {}
    for t in top_countries:
        top_country[t['country']] = round(t['top'], 2)

    ## Getting the current user's best time
    try:
        your_best = Records.objects.filter(quote=Quote(id), user=User(request.user.id)).aggregate(Max('best_time'))
        your_temp = Records.objects.get(quote=Quote(id), best_time=your_best['best_time__max'])
        your_best_time = your_temp.best_time

    except:
        your_best_time = 0


    ## Generating a graph for the quote
    graph_query = Records.objects.filter(quote=Quote(id)).order_by('-date')
    x = []
    y = []
    i = 0
    for g in graph_query:
        i = i+1
        x.append(g.best_time)
        y.append(i)

    plot = quote_records_plot(y, x, f"{quote.title}_{quote.id}")

    print(plot)
    
    return render(request, 'main/view_quote.html', {
        'content' : quote.quote,
        'title' : quote.title,
        'auther' : quote.auther,
        'publiher' : quote.user.username,
        'date' : quote.date,
        'best_wpm' : best_wpm,
        'avg_wpm' : best_avg,
        'top_countries' : top_country,
        'your_best_wpm' : your_best_time,
        'graph_path' : plot,


    })
