from accreditation_app.models import AccreditatonApplication
from django.core.exceptions import ValidationError
from django.shortcuts import render
from postmark.core import PMMail, PMMailSendException

from accreditation.settings import (
    POSTMARK_APPLICATION_SENT_TEMPLATE,
    POSTMARK_SENDER,
)


def accreditation_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        type_of_accreditation = request.POST['type_of_accreditation']
        application_text = request.POST['application']

        application = AccreditatonApplication.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            type_of_accreditation=type_of_accreditation,
            application=application_text
        )
        try:
            application.full_clean()
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
            pm = PMMail(
                to=email,
                sender=POSTMARK_SENDER,
                template_id=POSTMARK_APPLICATION_SENT_TEMPLATE,
                template_model=data
            )
            pm.send()
        except ValidationError as e:
            application.delete()
            data = {
                'error': e
            }
        except PMMailSendException as e:
            application.delete()
            data = {
                'error': e
            }
        data['application'] = application_text
        data['type_of_accreditation'] = type_of_accreditation
        return render(request, 'application_accepted.html', data)
    else:
        return render(request, 'accreditation.html')


def terms_conditons_page(request):
    return render(request, 'terms_conditons.html')
