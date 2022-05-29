from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import AlgoDetails
from .forms import AlgoDetailsForm
from developer.models import ratingAlgs
from django.http import FileResponse,Http404
from django.conf import settings
from django.db.models import Q
from django.db.models import Avg, Count

# Create your views here.
def adsignin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                request.session['um'] = email
                return redirect("adhome")
            else:
                messages.info(request,"invalid credentials")
        else:
            messages.info(request,"invalid credentials")
        return redirect("adsignin")

    else:
        return render(request,'adlogin.html')

def adhome(request):
    det = AlgoDetails.objects.all()
    return render(request, 'adhome.html',{'det':det} )

def developerrequests(request):
    det = AlgoDetails.objects.exclude(requestStatus='admin')
    return render(request, 'uploadstatusdetails.html', {'det':det} )
    
def updatestatus(request,updatedetail,pk):
    if updatedetail == 'accept':
        details = get_object_or_404(AlgoDetails,pk=pk)
        details.requestStatus = 'accepted'
        details.save()
    elif updatedetail == 'reject':
        details = get_object_or_404(AlgoDetails,pk=pk)
        details.requestStatus = 'rejected'
        details.save()
    elif updatedetail == 'cancel':
        details = get_object_or_404(AlgoDetails,pk=pk)
        details.requestStatus = 'cancel'
        details.save()
    elif updatedetail == 'delete':
        details = get_object_or_404(AlgoDetails,pk=pk)
        details.delete()
    return redirect('developerrequests')

def aduploaddata(request):
    if request.method == "POST":
        form = AlgoDetailsForm(request.POST,request.FILES)
        if form.is_valid():
            det = form.save()
            ra = ratingAlgs.objects.create(Rateduser=0,algs=det,ratings=0,review="")
            ra.save()
            return redirect('adhome')
    else:
        form = AlgoDetailsForm()
    return render(request, 'adupload.html',{'form':form})


# def preview(request,filename):
#     try:
#         filepath = os.path.join(settings.MEDIA_ROOT,filename)
#         print(filepath)
#         return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404()

@login_required
def adlogout(request):
    auth.logout(request)
    return redirect("adsignin")

@login_required
def adratings(request): #ratings to user's uploads
    d = ratingAlgs.objects.filter(~Q(Rateduser=0)).values('algs__algorithmUsed','algs__resourceType','algs__resourceTitle','algs__techniqueUsed','review','ratings').annotate(dcount=Avg('ratings'))
    return render(request, 'adratings.html',{'ratings':d})