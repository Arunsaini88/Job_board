from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .form import UpdateCompanyForm
from user.models import User
from django.http import Http404

# Create your views here.

def update_company(request):
    if request.user.is_recruiter:
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            messages.warning(request, "No company found for your account.")
            return redirect('dashboard')

        if request.method == 'POST':
            form = UpdateCompanyForm(request.POST, instance=company)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                user.has_comapny = True
                var.save()
                user.save()
                messages.success(request, 'Your company info has been updated!')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong, please check the form.')
        else:
            form = UpdateCompanyForm(instance=company)
        context = {'form': form}
        return render(request, 'company/update_company.html', context)
    else:
        messages.warning(request, 'Permission denied.')
        return redirect('dashboard')

# views company details

def company_details(request, pk):
    try:
        company = Company.objects.get(pk=int(pk)-2)
        print(company)
        context = {'company':company}
        return render(request,'company/company_details.html', context)
    except Exception as e:
        print(pk)
        messages.warning(request,f'Company does not exist.{e}')
        return redirect('dashboard')


    


