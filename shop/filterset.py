import decimal

import rest_framework_filters as filters
from django.db.models import Min, F, Count, Q, Value,Max, query
from django.db.models.functions import Least, Coalesce
from django.utils.datetime_safe import date,datetime
from rest_framework_filters.backends import RestFrameworkFilterBackend
# from tours.models import Tour, TourCategory, City, TourVariation, Currency, TourGuide, TourGalleryImage, TourTime
# from tours.utils import convert, deconvert
from shop.models import ChoiceAttribute, Product, ProductVariation, ProductVariationAttribute

#
class ProductOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('price', ' Var price'),
            ('-price', ' Var price (descending)'),
            ('most_popular', ' most popular'),
            ('created_at',"created_at"),
              ('-created_at',"-created_at")
        ]

    def filter(self, qs, value):
        # OrderingFilter is CSV-based, so `value` is a list
        if any(v in ['price', '-price','most_popular',"created_at","-created_at"] for v in value):
            today = date.today()
            today_str = datetime.today().strftime("%A")
            if 'price' in value:
                # Query = Q(variations__special_dates__start_date__gte=today)|Q(variations__special_dates__end_date__gte=today)|Q(variations__special_dates__day=today_str.lower())
                qs = qs.annotate(price_min =Min("variations__price"))\
                    .annotate(discount_price_min =Min("variations__discount_price")) \
                    .annotate(final_price=Least("price_min", Coalesce("discount_price_min", Value(1000000000000000))))\
                    .order_by( "final_price")
                    # .annotate(special_price_min= Min('variations__special_price',
                    #     filter=Query
                    # ))\

                i = value.index("price")
                del value[i]
            elif '-price' in value:
                # Query = Q(variations__special_dates__start_date__gte=today)|Q(variations__special_dates__end_date__gte=today)|Q(variations__special_dates__day=today_str.lower())
                qs = qs.annotate(price_min =Min("variations__price"))\
                    .annotate(discount_price_min =Min("variations__discount_price")) \
                    .annotate(final_price=Least("price_min", Coalesce("discount_price_min", Value(10000000000000000)))) \
                    .order_by("-final_price")

                # .annotate(special_price_min= Min('variations__special_price')) \

                # .annotate(special_price_min=Min('variations__special_price',
                    #     filter=Query
                    # )) \
                i = value.index("-price")
                del value[i]
            elif '-created_at' in value:
               
                qs = qs.annotate(created_at_min = Min("variations__created_at"))\
                    .order_by("-created_at_min")
                # for i in qs:
                #     print(i)
                # qs = qs.order_by("-variations__created_at").distinct()
                for i in qs:
                    print(i)
                i = value.index("-created_at")
                del value[i]
            elif 'created_at' in value:
                qs = qs.annotate(created_at_max = Max("variations__created_at"))\
                    .order_by("created_at_max")
                # qs = qs.order_by("variations__created_at").distinct()
                for i in qs:
                    print(i)
                i = value.index("created_at")
                del value[i]
            # elif 'most_popular' in value :
            #     qs = qs.annotate(most_popular=Count("variations__tourpayment__paid")).order_by("most_popular")
            #     # ss = qs.aggregate(most_popular=Count("variations__tourpayment__paid"))
            #     # Tour.objects.filter(variations__tourpayment__paid)
            #     i = value.index("most_popular")
            #     del value[i]

        return super().filter(qs, value)

class MyFilterBackend(RestFrameworkFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class ChoiceAttributeFilter(filters.FilterSet):
    class Meta:
        model = ChoiceAttribute
        fields = {
            'title': ['exact', 'in', 'startswith'],
            'id': [ 'in'],
        }
class ProductVariationAttributeFilter(filters.FilterSet):
    choice_attribute = filters.RelatedFilter(ChoiceAttributeFilter,field_name='choice_attribute',queryset = ChoiceAttribute.objects.all())

    class Meta:
        model = ProductVariationAttribute
        fields = {
            'attribute_value': ['exact', 'in', 'startswith'],
            'id': [ 'in'],
        }

# class CityFilter(filters.FilterSet):
#     class Meta:
#         model = City
#         fields = {'name': ['exact', 'in', 'startswith']}
#
#
# class TourGuideFilter(filters.FilterSet):
#     class Meta:
#         model = TourGuide
#         fields = {'language': ['exact', 'in', 'startswith']}
#
#
class VariationFilter(filters.FilterSet):
    # max_price = filters.NumberFilter(field_name="price",method="get_price_max")
    # min_price = filters.NumberFilter(field_name="price",method="get_price_min")
    specifications = filters.RelatedFilter(ProductVariationAttributeFilter,field_name='specifications',queryset = ProductVariationAttribute.objects.all())
    class Meta:
        model = ProductVariation
        fields = {
        }


    # def get_price_max(self, qs, name, value):
    #     return qs.filter(price__lte=value)

    # def get_price_min(self, qs, name, value):
    #     return qs.filter(price__gte=value)

class GalleryFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('caption','caption')
        )
    )
# class TourTimeFilter(filters.FilterSet):
#     class Meta:
#         model = TourTime
#         fields = {'title': ['exact', 'in', 'startswith']}


#
class ProductListFilter(filters.FilterSet):
    # menuitem = filters.RelatedFilter(MenuItemFilter, field_name='menuitem', queryset=Menuitem.objects.all())
#     city = filters.RelatedFilter(CityFilter, field_name='city', queryset=City.objects.all())
    variations = filters.RelatedFilter(VariationFilter, queryset=ProductVariation.objects.all())
#     guide = filters.RelatedFilter(TourGuideFilter,field_name="guide_languages", queryset=TourGuide.objects.all())
    top_deals = filters.BooleanFilter(label='top_deals', method='get_top_deals')
#     gallery = filters.RelatedFilter(GalleryFilter,field_name="gallery", queryset=TourGalleryImage.objects.all())
#     time = filters.RelatedFilter(TourTimeFilter,field_name='time',queryset=TourTime.objects.all())
    max_price = filters.NumberFilter(field_name="price",method="get_price_max")
    min_price = filters.NumberFilter(field_name="price",method="get_price_min")
    category = filters.CharFilter(field_name='subcategory__category__slug',lookup_expr='iexact')
    subcategory = filters.CharFilter(field_name='subcategory__slug',lookup_expr='iexact')
    test_in_place = filters.BooleanFilter(field_name='variations__test_in_place')
    attribute = filters.CharFilter(field_name='variations__attributes__attribute__slug',lookup_expr='iexact')
    attribute_value = filters.CharFilter(field_name='variations__attributes__choice_attribute__slug',lookup_expr='iexact')
    color = filters.CharFilter(label='color', method='get_colors')

    ordering = ProductOrderingFilter(
    fields=(
            # ('created_at', 'created_at'),
            # ('priority', 'priority'),
            # ("duration",'duration')
        ),
    )
    class Meta:
        model = Product
        fields={
            "title":["lte",'gte',"contains"],
            "description":["lte",'gte',"exact"],
        }
    def get_top_deals(self, qs, name, value):
        if value:
            varss = []
            for item in qs:
                try:
                    # min_variations = tour.variations.all().order_by('discount_price','price')[0]
                    min_variations = item.variations.all().annotate(
                        final_price=Least("price", Coalesce("discount_price", Value(1000000)))).order_by(
                        "final_price")[0]

                    if (min_variations.discount_price is not None):
                        varss.append(min_variations.id)
                except Exception as ex:
                    print(ex)
            qs = qs.filter(variations__in=varss).annotate(Min('variations__price')).annotate(distance=F('variations__price')-F('variations__discount_price')).order_by('-distance')
            return qs
        else:
            return qs
#
    def get_price_max(self, qs, name, value):
        # currency = self.data.get('currency', 'aed')
        if value:
            # price =deconvert(currency, value)
            price = value
            varss = []
            for tour in qs:
                try:
                    min_variations = tour.variations.all().annotate(
                        final_price=Least("price", Coalesce("discount_price", Value(10000000000000)))).order_by(
                        "final_price")[0]

                    if (min_variations.final_price <= price):
                        varss.append(min_variations.id)
                    print(tour)
                except Exception as ex:
                    print(ex)
            qs = qs.filter(variations__in=varss)
        return qs

    def get_price_min(self, qs, name, value):
        # currency = self.data.get('currency', 'aed')
        if value:
            # price = deconvert(currency, value)
            price = value
            varss = []
            for tour in qs:
                try:
                    min_variations = tour.variations.all().annotate(
                        final_price=Least("price", Coalesce("discount_price", Value(10000000000000)))).order_by(
                        "final_price")[0]

                    if (min_variations.final_price >= price):
                        varss.append(min_variations.id)
                    print(tour)
                except Exception as ex:
                    print(ex)
            qs = qs.filter(variations__in=varss)
        return qs
    def get_attibutes(self, qs, name, value):
        # currency = self.data.get('currency', 'aed')
        if value:
           print(qs , name , value)
        return qs
    def get_colors(self, qs, name, value):
        # currency = self.data.get('currency', 'aed')
        colors = value.split("~")
        qs = qs.filter(variations__color__slug__in=colors)
        return qs
