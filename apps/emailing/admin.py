from django.contrib import admin
from .models import ExtendUser, EmailConfiguration


admin.site.register(ExtendUser)
admin.site.register(EmailConfiguration)

