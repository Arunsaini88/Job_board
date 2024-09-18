from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import User
from .models import Resume
from .form import UpdateResumeForm


# Create your views here.
def create_resume(request):
    if request.user.is_applicant:
        resume = Resume.objects.get(user=request.user)
        if request.method == 'POST':
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(pk=request.user.id)
                user.has_resume = True
                user.save()
                var.save()
                messages.info(request, 'Your resume info has been created')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something want wrong')
        else:
            form = UpdateResumeForm(instance=resume)
            context = {'form':form}
            return render(request, 'resume/create_resume.html', context)
    else:
        messages.warning(request, 'Permession denied')
        return redirect('dashboard')
# Resume Details

def resume_details(request, pk):
    resume = Resume.objects.get(pk=pk)
    context = {'resume':resume}
    return render(request, 'resume/resume_details.html', context)