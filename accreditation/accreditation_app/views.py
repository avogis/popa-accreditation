from django.shortcuts import render


def accreditation_page(request):
    if request.method == 'POST':
        data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
        }
        return render(request, 'application_accepted.html', data)
    else:
        return render(request, 'accreditation.html')
