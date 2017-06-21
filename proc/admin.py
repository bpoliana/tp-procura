from django.contrib import admin
from .models import HealthCenterOk, n_User,Medicine, Patient


#class UsersAdmin(admin.ModelAdmin):
		#pass
#admin.site.register(n_User, UsersAdmin)
admin.site.register(n_User)
#class HealthCentersAdmin(admin.ModelAdmin):
#	model = HealthCenter
#	list_display = ['name', 'center_type']
admin.site.register(HealthCenterOk)
#admin.site.register(HealthCenter, HealthCentersAdmin)
admin.site.register(Medicine)
# Register your models here.
admin.site.register(Patient)
