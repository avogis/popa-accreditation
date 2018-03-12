from django.shortcuts import render


def accreditation_page(request):
    return render(request, 'accreditation.html')


def application_accepted(request):
    return render(request, 'application_accepted.html')
