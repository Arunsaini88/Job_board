from django.shortcuts import render, get_object_or_404
from django.http import Http404
from job.models import Job, ApplyJob
from .filter import JobFilter
# Create your views here.
def home(request):
    filter = JobFilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter':filter}
    return render(request, 'website/home.html',context)

def job_listing(request):
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    context = {'jobs':jobs}
    return render(request, 'website/job_listing.html',context)

# def job_details(request, pk):
#     if ApplyJob.objects.filter(user = request.user, job=pk).exists():
#         has_applied = True
#     else:
#         has_applied = False
#     job = Job.objects.get(pk=pk)
#     context ={'job':job, 'has_applied':has_applied}
#     return render(request, 'website/job_details.html', context) 
def job_details(request, pk):
    try:
        job = get_object_or_404(Job, pk=pk)
    except Http404:
        return render(request, 'website/404.html', status=404) 
    has_applied = False

    try:
        if request.user.is_authenticated:
            if ApplyJob.objects.filter(user=request.user, job=job).exists():
                has_applied = True
    except Exception as e:
        print(f"An error occurred while checking application status: {e}")
    context = {
        'job': job,
        'has_applied': has_applied
    }
    return render(request, 'website/job_details.html', context)