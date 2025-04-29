from django.db import models
from django.forms import IntegerField


class SMSCode(models.Model):
    code = models.CharField(max_length=10)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='sms_code')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.code} - {self.user.username}'
