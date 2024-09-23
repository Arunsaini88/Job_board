from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import User
from .models import Resume
from .form import UpdateResumeForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def create_resume(request):
    try:
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
                    messages.info(request, 'Your resume has been created/updated successfully.')
                    return redirect('resume-details' , pk=resume.pk)
                else:
                    messages.warning(request, 'Something want wrong')
            else:
                form = UpdateResumeForm(instance=resume)
                context = {'form':form}
                return render(request, 'resume/create_resume.html', context)
        else:
            messages.warning(request, 'Permession denied')
            return redirect('dashboard')
    except Exception as e:
        messages.warning(request, f'{e}.please try latter.')
        return redirect('dashboard')
# Resume Details

def resume_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to be logged in to view this page.')
        return redirect('login')
    try:
        resume = Resume.objects.get(pk=int(pk)-1, user=request.user)
        context = {'resume': resume}
        return render(request, 'resume/resume_details.html', context)
    except Exception as e:
        messages.warning(request, 'The requested resume does not exist or you do not have access to it.')
        print(f'Error{e}')
        return redirect('dashboard')

