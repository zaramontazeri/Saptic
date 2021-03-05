from rest_framework import serializers


from pages.models import FAQ, Page, ContactMessage, Subscription, CompanyInfo



class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        exclude = ('id', 'active', 'language', 'created_at', 'updated_at')


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        exclude = ('id', 'created_at', 'updated_at', 'active', 'language')


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        exclude = ('id',)


class SubscriptionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Subscription
		exclude = ['id']

# class NewsLetterSerializer(serializers.ModelSerializer):
#     class Meta:
#             model = NewsLetter
#             depth = 2
#             fields='__all__'
#
#

class CompanyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyInfo
        geo_field = 'point'
        fields = '__all__'


class PageContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageContent
        fields = (
            'slug', 
            'page_name', 
            'created', 
            'last_updated', 
            'section', 
            'cover', 
            'title', 
            'content', 
            'actions', 
            'content_type', 
        )

