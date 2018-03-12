from django.contrib import admin
from django.contrib.auth.models import Group, User
from accreditation_app.models import AccreditatonApplication


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(AccreditatonApplication)
class AccreditatonApplicationAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = ('last_name', 'first_name', 'applied', 'type_of_accreditation', 'granted',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'last_name',
                'first_name',
                'type_of_accreditation',
                'application',
                'email')
        return self.readonly_fields
