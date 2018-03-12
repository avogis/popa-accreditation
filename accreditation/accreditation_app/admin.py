from django.contrib import admin
from django.contrib.auth.models import Group, User
from accreditation_app.models import AccreditatonApplication


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(AccreditatonApplication)
class AccreditatonApplicationAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
