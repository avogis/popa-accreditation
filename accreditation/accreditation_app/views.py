from django.shortcuts import render

from accreditation_app.models import AccreditatonApplication
from django.core.exceptions import ValidationError


def accreditation_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        application = AccreditatonApplication.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        try:
            application.full_clean()
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
        except ValidationError as e:
            application.delete()
            data = {
                'error': e
            }
        return render(request, 'application_accepted.html', data)
    else:
        return render(request, 'accreditation.html')
