from django.http import HttpResponse


def accreditation_page(request):
    return HttpResponse('<html><title>Popaganda Accreditation</title></html>')
