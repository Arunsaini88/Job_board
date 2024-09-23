from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Job, ApplyJob
from .form import CreateJobForm, UpdateJobForm
# from .utils import send_email
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def create_job(request):
    if request.user.is_recruiter and request.user.has_comapny:
        if request.method == 'POST': 
            form = CreateJobForm(request.POST)
            if form.is_valid():
                try:
                    var = form.save(commit=False)
                    var.user = request.user
                    var.company = request.user.company
                    var.save()
                    messages.info(request, 'Your New job has been created.')

                    # subject = 'Job Posted Successfully'
                    # message = f'Your job "{var.title}" has been posted successfully.'
                    # send_email(subject, message, [request.user.email])
                    
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, 'An error occurred while creating the job. Please try again.')
                    return redirect('create-job')
            else:
                messages.warning(request, 'Somethig want wrong')
                return redirect('create-job')
        else:
            form = CreateJobForm()
            context = {'form':form}
            return render(request, 'job/create_job.html', context)
    else:
        messages.warning(request, 'Premession Denied')
        return redirect('dashboard')
    

def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            try:
                form.save()
                messages.info(request, 'Your job has been updated.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while updating the job. Please try again.')
                print(f'Error: {e}')  # Log the error
        else:
            messages.warning(request, 'Something went wrong with the form.')
    else:
        form = UpdateJobForm(instance=job)
        context = {'form': form}
        return render(request, 'job/update_job.html', context)

def manage_jobs(request):
    try:
        jobs = Job.objects.filter(user=request.user, company=request.user.company)
        context = {'jobs': jobs}
        return render(request, 'job/manage_jobs.html', context)
    except Exception as e:
        messages.warning(request, f'There are an error {e}')
        return redirect('dashboard')

def apply_to_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        try:
            job = get_object_or_404(Job, pk=pk)
            if ApplyJob.objects.filter(user=request.user, job=job).exists():
                messages.warning(request, 'You have already applied for this job.')
                return redirect('dashboard')

            ApplyJob.objects.create(
                job=job,
                user=request.user,
                status='Pending',
            )

            # recruiter_email = job.user.email  # Assuming the recruiter is the job's user
            # subject = 'New Job Application'
            # message = f'Applicant {request.user.username} has applied for the job "{job.title}".'
            # send_email(subject, message, [recruiter_email])

            messages.info(request, 'You have successfully applied! Please see your dashboard.')

            # subject_applicant = 'Job Application Confirmation'
            # message_applicant = f'You have successfully applied for "{job.title}".'
            # send_email(subject_applicant, message_applicant, [request.user.email])
            return redirect('job-listing')
        except ObjectDoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('job-listing')
        except Exception as e:
            messages.error(request, 'An error occurred while applying for the job. Please try again.')
            print(f'Error: {e}')  # Log the error
            return redirect('dashboard')
    else:
        messages.info(request, 'Please login to continue.')
        return redirect('login')

def all_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applicants = job.applyjob_set.all()
    context = {'job': job, 'applicants': applicants}
    return render(request, 'job/all_applicants.html', context)

def applied_jobs(request):
    jobs = ApplyJob.objects.filter(user=request.user)
    context = {'jobs': jobs}
    return render(request, 'job/applied_jobs.html', context)
