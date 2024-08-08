from django.db import models


class TgUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    language_code = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UserMessage(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    message_text = models.TextField()
    date_received = models.DateTimeField(auto_now_add=True)



