from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect #need to know
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



# Create your views here.

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at') #ye kya hota hai
    #print("Mere Tweets",tweets)
    return render(request,'tweet-list.html',{
        'tweets':tweets
    })


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES) #need to know whst is this
        if form.is_valid():
            tweet = form.save(commit=False) #iska kya mtlab hai
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})


@login_required
def tweet_edit(request, tweet_id):
    tweet=get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST,request.FILES, instance=tweet) # ye kya krta hai
        if form.is_valid():
            tweet = form.save(commit=False) #iska kya mtlab hai
            tweet.user = request.user #need to know
            tweet.save()
            return redirect('tweet_list')                   
    else:
        form= TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id,user = request.user)
    if request.method =='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save() 
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    
    return render(request,'registration/register.html',{'form':form})

