# from celery import shared_task
# from celery.utils.log import get_task_logger
# from django.contrib.auth import get_user_model
#
# from pages.emails import NewsLetterEmail
# from pages.models import Subscription
#
# logger = get_task_logger(__name__)
# import time
#
# @shared_task
# def send_newsletter_email_task(letters):
#     """sends an email when feedback form is filled successfully"""
#     # time.sleep(5)
#     UserModel = get_user_model()
#     emails_user = UserModel.objects.values_list('email', flat=True).all()
#     emails_subscription = Subscription.objects.values_list("email", flat=True).all()
#     emails = list(set(list(emails_user) + list(emails_subscription)))
#     while ("" in emails):
#         emails.remove("")
#     to = [*emails]
#     for letter in letters :
#         letter_context = {
#             "letter":letter,
#         }
#
#         NewsLetterEmail(context=letter_context,template_name="email/news_letter_blog_type1").send(to)
#     return "ok"
#
#
# @shared_task
# def send_notification():
#      print("eeeee")