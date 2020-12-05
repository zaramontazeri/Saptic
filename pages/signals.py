import random, string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

from .models import NewsLetter


# @receiver(post_save, sender=NewsLetter)
# def send_news_letter(instance: NewsLetter, created, **kwargs):
#     if not created:
#         return

    #send email
