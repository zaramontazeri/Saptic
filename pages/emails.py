# from templated_mail.mail import BaseEmailMessage
#
#
# class NewsLetterEmail(BaseEmailMessage):
#     template_name = "news_letter_blog_type1"
#     def __init__(self, request=None, context=None, template_name=None,
#                  *args, **kwargs):
#         super(NewsLetterEmail, self).__init__(request, context, template_name,*args, **kwargs)
#     def get_context_data(self):
#         context = super().get_context_data()
#         # user = context.get("user")
#         return context
#     def get_connection(self, fail_silently=False):
#         from django.core.mail import get_connection
#         if not self.connection:
#             self.connection = get_connection(fail_silently=fail_silently)
#         return self.connection
#
