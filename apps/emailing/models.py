from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models
from graphene_django.types import DjangoObjectType


class EmailConfiguration(models.Model):
    name = models.CharField(max_length=255)
    # New fields for outgoing mail server
    smtp_server = models.CharField(max_length=255, blank=True)
    smtp_port = models.PositiveIntegerField(blank=True, null=True)
    # New fields for incoming mail server
    incoming_server = models.CharField(max_length=255, blank=True)
    incoming_port = models.PositiveIntegerField(blank=True, null=True)
    incoming_type = models.CharField(max_length=10, blank=True,
        choices=[('POP', 'POP'),('IMAP', 'IMAP'),('Local', 'Local'),])
    incoming_ssl = models.BooleanField(default=False)
    incoming_tls = models.BooleanField(default=False)

    def __str__(self, *args: Any, **kwargs: Any) -> None:
        super().__str__(*args, **kwargs)
        return f"{self.name}"




class EmailConfigurationType(DjangoObjectType):
    class Meta:
        model = EmailConfiguration
        fields = '__all__'



class ExtendUser(AbstractUser):
    email_conf = models.ForeignKey(EmailConfiguration, 
        on_delete=models.SET_NULL, related_name='ExtendUser', null=True)
    app_password = models.CharField(max_length=255)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'