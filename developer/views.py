#from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import MyUser
from authority.forms import AlgoDetailsForm
from authority.models import AlgoDetails
from django.db.models import Avg, Count
from .models import ratingAlgs
from django.db.models import Q

# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1==password2:
            if MyUser.objects.filter(email=email).exists():
                messages.info(request,"Already Registered with this email")
                return redirect("signup_page")
            else:
                user = MyUser.objects.create_user(email=email,username=username,password=password1)
                user.save()
                return redirect("signin_page")
        else:
            messages.info(request,"Please re-enter correct password")
            return redirect("signup_page")    
    else:
            return render(request,'signup.html')
 

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            #request.session['um'] = email
            return redirect("home_page")
        else:
            messages.info(request,"invalid credentials")
            return redirect("signin_page")

    else:
        return render(request,'login.html')


@login_required
def home(request):
    det = ratingAlgs.objects.filter(Q(algs__requestStatus='accepted')|Q(algs__requestStatus='admin')).filter(~Q(algs__userId=request.user.id)).values('algs__algorithmUsed','algs__resourceType','algs__resourceTitle','algs__author','algs__algorithmUsed','algs__id','algs__techniqueDescription','algs__techniqueUsed').annotate(dcount=Avg('ratings',filter=~Q(Rateduser=0))).order_by('-dcount')
    return render(request, 'home.html',{'det':det})

@login_required
def logout(request):
    auth.logout(request)
    return redirect("signin_page")


def uploads(request):
    if request.method == 'POST':
        form = AlgoDetailsForm(request.POST,request.FILES)
        if form.is_valid():
            dets = form.save(commit=False)
            dets.userId = request.user.id
            dets.requestStatus = 'pending'
            dets.save()
            ra = ratingAlgs.objects.create(Rateduser=0,algs=dets,ratings=0,review="")
            ra.save()
            
            return redirect('home_page')
    else:
        form = AlgoDetailsForm()
    return render(request, 'uploads.html', {'form':form} )


def myuploads(request):
    det = AlgoDetails.objects.filter(userId = request.user.id,requestStatus='accepted')
    return render(request, 'myuploads.html', {'det':det} )


def uploadstatus(request):
    det = AlgoDetails.objects.filter(userId = request.user.id)
    return render(request, 'uploadstatus.html', {'det':det} )

def rate(request,pk):
    det = get_object_or_404(AlgoDetails,pk=pk)
    if request.method == 'POST':
        ratings = request.POST.get('ratings','')
        review = request.POST.get('review','')
        if ratingAlgs.objects.create(Rateduser=request.user.id,algs=det,ratings=ratings,review=review):
            return redirect('home_page')
    return render(request, 'rate.html',{'det':det})

@login_required
def yourratings(request):  #ratings given by user
    ratn = ratingAlgs.objects.filter(Rateduser=request.user.id)
    return render(request,'yourratings.html',{'ratings':ratn})

@login_required
def ratings(request): #ratings to user's uploads
    d = ratingAlgs.objects.filter(algs__userId=request.user.id).filter(~Q(Rateduser=0)).values('algs__algorithmUsed','algs__resourceType','algs__resourceTitle','algs__techniqueUsed','review','ratings').annotate(dcount=Avg('ratings'))
    return render(request, 'ratings.html',{'ratings':d})

@login_required
def graphs(request,chart_type):
    det = ratingAlgs.objects.values('algs__algorithmUsed').annotate(dcount=Avg('ratings'))
    #det = ratingAlgs.objects.all().values('algs__resourceTitle').group_by('algs__resourceTitle')
    template_here = 'graph.html'
    if chart_type=='bar':
        template_here = 'graph1.html'
    elif chart_type=='pie':
        template_here = 'graph2.html'
    elif chart_type=='spline':
        template_here = 'graph3.html'
    elif chart_type=='line':
        template_here = 'graph4.html'
    elif chart_type=='column':
        template_here = 'graph.html'
    return render(request,template_here,{'det':det})
