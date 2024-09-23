from django.shortcuts import render, get_object_or_404
from django.http import Http404
from job.models import Job, ApplyJob, State, Industry
from .filter import JobFilter
from django.core.paginator import Paginator


def home(request):
    filter = JobFilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter':filter}
    return render(request, 'website/home.html',context)


def job_listing(request):

    job_filter = JobFilter(request.GET)
    if not request.GET:
        jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    else:
      
        jobs = job_filter.qs.filter(is_available=True).order_by('-timestamp')
    paginator = Paginator(jobs, 10)  
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    context = {
        'jobs': jobs,
        'states': State.objects.all(),
        'industries': Industry.objects.all(), 
        'filter': job_filter,
    }
    return render(request, 'website/job_listing.html', context)



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