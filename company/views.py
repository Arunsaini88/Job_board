from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .form import UpdateCompanyForm
from user.models import User


# Create your views here.
def update_company(request):
    if request.user.is_recruiter:
        company = Company.objects.get(user = request.user)
        if request.method == 'POST':
            form = UpdateCompanyForm(request.POST, instance=company)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(id = request.user.id)
                user.has_comapny =True
                var.save()
                user.save()
                messages.info(request, 'Your company is info has been updated!')
                return redirect('dashboard')
            else:
                messages.warning(request,'Something want wrong')
        else:
            form  = UpdateCompanyForm(instance=company)
            context = {'form':form}
            return render(request, 'company/update_company.html', context)
    else:
        messages.warning(request, 'Permession denied')
        return redirect('dashboard')

# views company details
def company_details(request, pk):
    company = Company.objects.get(pk=pk)
    context = {'company':company}
    return render(request,'company/company_details.html', context)

