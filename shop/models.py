
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.html import format_html
from django.conf import settings
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _


#todo IMPORTANT: REMEMBER THAT THIS APP IS JUST IN PERSION


# TODO: BOX ro tasmim begir chejoori neshoon bedi
# class ProductAccessory(models.Model):
#     box=models.BooleanField(default=False)
#     price=models.DecimalField()
#

class Category(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(allow_unicode=True)
    cover = models.ImageField(
        upload_to='covers/shop/category', blank=True, null=True) #todo doesnt it better to not be null true

    class Meta:
        verbose_name = 'Shop Category'
        verbose_name_plural = 'Shop Categories'

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(allow_unicode=True)
    category=models.ForeignKey(Category,related_name="sub_category",on_delete=models.PROTECT)
    def __str__(self):
        return self.category.title+"__"+self.title


# class SubcategorySpecifications(models.Model):
#     specification_key = models.CharField(max_length=128)
#     specification_value = models.CharField(max_length=128)
#     promotional_gift=models.ForeignKey(Subcategory,related_name="specifications",on_delete=models.CASCADE)
#     class Meta(object):
#         ordering = ['specification_key']
#
#     def __str__(self):
#         return self.specification_key


class Product(models.Model):
    #todo rating
    cover = models.ImageField(
        upload_to='covers/shop/product', blank=True, null=True)
    title=models.CharField(max_length=200)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.PROTECT) #todo on_delete casacade? agar subcategory eshtebahi hazf she koli mahsool hazf mishan! che konim?
    #GALLERY HAS FK TO PRODUCT
    description=models.TextField()
    #Review HAS FK TO PRODUCT
    related_products = models.ManyToManyField('self',blank=True,null=True, symmetrical=True)#, related_name='+' #if i used through it wasn't bi-directional and i had to do symmetrical=False
    #Product variations has FK to product
    def __str__(self):
        return self.title

#todo alan hame aks haye gallery mahsool bedoon dar nazar gereftan size yekjast. ok hast?
class ProductGalleryImage(models.Model):
    product=models.ForeignKey(Product,related_name="product_images",on_delete=models.CASCADE)
    caption = models.CharField(max_length=128)
    image = models.ImageField(upload_to='tours/gallery')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return None
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.caption

    class Meta(object):
        ordering = ['order']

class ProductAttribute(models.Model):
    title=models.CharField(max_length=150)
    def __str__(self):
        return self.title

class ProductVariation(models.Model):

    title_size=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations")
    specifications = models.ManyToManyField(ProductAttribute, blank=True, through='ProductVariationAttribute',related_name='specifications_to_person')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    # discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    occasional_discount= models.ForeignKey("OccasionalDiscount",related_name="occasional_discount_set",blank=True,null=True,on_delete=models.SET_NULL) #this parametere makes impact on discount price
    discount_price =models.DecimalField(max_digits=10, decimal_places=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # @property
    # def discount_price(self):
    #     discount = int(self.price)
    #     if self.occasional_discount:
    #         percentage=self.occasional_discount.percentage
    #         discount = int(float(self.price) - round((float(percentage) / 100.0) * float(self.base_price)))
    #     return discount

    def __str__(self):
        return self.product.title + " __ " +self.title_size


class ProductVariationAttribute(models.Model):
    product_variation=models.ForeignKey(ProductVariation,on_delete=models.CASCADE) #agar khode product nabashe. vojood attribute bi manie
    attribute=models.ForeignKey(ProductAttribute,on_delete=models.PROTECT) #agar attribute ro bekhaym pak konim injoori mifahmim ke oon attribute baraye baghie estefade shode
    attribute_value=models.CharField(max_length=150)

#todo rating is connected to reviews??????
class ProductReview(models.Model):
    product=models.ForeignKey(Product,related_name="product_reviews",on_delete=models.CASCADE)
    #todo USER ro moshakhas kon bepors ke daghighan modele user chejoorie ke fk be oon chejoori bashe
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    #todo? rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    confirmed=models.BooleanField(default=False)
    #todo write afte cheking USER: def __str__(self):
    #     return "User: {username} | Tour: {id}".format(username=self.user.username, id=self.tour.id)
    def __str__(self):
        return self.product.title +"__"+str(self.created_at.date())



#todo#################################################################



class Invoice(models.Model):
    #list of status choices :paid _ unsuccessful paiment-> in transactions. deliverd
    DRAFT='dr'
    PAYED='pa'
    PENDING='pe'
    CONFIRMED='co'
    DELIVERED='de'

    ORDER_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PAYED,'Payed'),
    )

    DELIVER_STATUS_CHOICES = (
        # todo azashoon bepors confirm ro fiziki daran ya na
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (DELIVERED, 'Delivered'),
    )

    order_status=models.CharField(verbose_name=_("pay_status"),max_length=4,choices=ORDER_STATUS_CHOICES,default=DRAFT)
    deliver_status = models.CharField(verbose_name=_("deliver_status"), max_length=4, choices=DELIVER_STATUS_CHOICES, default=PENDING)
    #TODO shange shipping_number into u_id (ask erfan)
    shipping_number=models.CharField(max_length=24,null=True,blank=True) #POSTAL TRACKING CODE

    # seller = models.ForeignKey(Seller,verbose_name=_("seller"), on_delete=models.SET_NULL, null=True) #from seller you can also undrestand which restaurant it is
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("customer"), null=True,blank=True, on_delete=models.SET_NULL)
    # u can search usage of through in here:https://docs.djangoproject.com/en/2.2/topics/db/models/
    product_items = models.ManyToManyField(ProductVariation,verbose_name=_("product items"), through="OrderedItem")  #
    total_price=models.DecimalField(verbose_name=_("total price"),default=Decimal('0.00'),max_digits=19, decimal_places=0,null=True,blank=True)  # totalCost #todo #decimal 2 or 3?)
    #serial_number (is it secure if i use id for each invoice??? or should i make serial number myself?)
    description=models.CharField(verbose_name=_("description"),max_length=200 , null=True, blank=True)
    date=models.DateTimeField(verbose_name=_("date"),auto_now_add=True ,null=True) #todo how to make this automatic and JALALI
    # address = models.TextField(verbose_name=_("address"),null=True,default="-1")
    address = models.ForeignKey("users.Address",on_delete=models.PROTECT,default="-1") #if a user has address in inovice I dont let the user to delete
    #todo what about default and on_delete? talk to erfan
    discount_code = models.ForeignKey("DiscountCode" ,on_delete=models.SET("deleted"), related_name="payments", null=True) #It's first model of discounting

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


    def __str__(self):
        return str(self.id)+"_"+self.customer.user.username

    # def get_absolute_url(self):
    #     return reverse('app_name_invoice_detail', args=(self.pk,))
    #
    #
    # def get_update_url(self):
    #     return reverse('app_name_invoice_update', args=(self.pk,))

class OrderedItem(models.Model):
    product_variation_item=models.ForeignKey(ProductVariation,verbose_name=_("product item"),null=True,blank=True, on_delete=models.SET_NULL,related_name="products") #,related_query_name="products"
    invoice=models.ForeignKey(Invoice,verbose_name=_("invoice"),on_delete=models.SET_NULL, null=True,related_name="orders")
    #todo what about on_delete???

    qty = models.IntegerField(verbose_name=_("quantity"),null=True)
    #IMP: I  use unit price so your previous invoices won't be incorrect after you changed a food's price.
    unit_base_price=models.DecimalField(verbose_name=_("unit base price"),max_digits=19, decimal_places=0) #ino az roye gheymat e product variation mirizi tooye in todo: where?
    unit_discount_price = models.DecimalField(verbose_name=_("unit discount price"),null=True,blank=True, max_digits=19, decimal_places=0)
    # todo #decimal 2 or 3?


    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Ordered Item')
        verbose_name_plural = _('Ordered Items')

    def __str__(self):
        return str(self.id)+"_"+self.product_variation_item.product.title+"_"+self.product_variation_item.title_size #todo name or first+last name  +"_"+self.invoice.costumer.name

    # def get_absolute_url(self):
    #     return reverse('app_name_ordereditem_detail', args=(self.pk,))
    #
    # def get_update_url(self):
    #     return reverse('app_name_ordereditem_update', args=(self.pk,))
    #

#
# class TourPayment(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     day = models.DateField()
#     paid = models.BooleanField(default=False)
#     tour_price = models.DecimalField(max_digits=12, decimal_places=2)
#
#     name = models.CharField(max_length=32)
#     email = models.EmailField()
#     phone = models.CharField(max_length=32)
#     email_notif = models.BooleanField(default=False)
#     # tour = models.ForeignKey('Tour', on_delete=models.CASCADE,
#     #                          related_name="payments")
#     user = models.ForeignKey(User, on_delete=models.SET_NULL,
#                              related_name="payments", null=True, blank=True)
#     variation = models.ForeignKey(TourVariation,related_name="payments",on_delete=models.DO_NOTHING)
#     pickup_point = models.CharField(max_length=32,null=True,blank=True) #todo
#     promotion_code = models.ForeignKey("PromotionalCode",on_delete=models.DO_NOTHING ,related_name="payments", null=True) #todo
#     discount_code = models.ForeignKey("DiscountCode" ,on_delete=models.DO_NOTHING, related_name="payments", null=True)
#     def __str__(self):
#         return str(self.id)
#



class Transactions(models.Model):
    SATAUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending',"Pending")
    )
    # amount and date #todo I have total price and date in invoice and I have a fk to invoice , should i use "amount" and "date" here too?
    invoice=models.ForeignKey(Invoice,verbose_name=_("invoice"), on_delete=models.PROTECT,related_name="transaction")
    refId = models.CharField(_("trackingCode"), max_length=100) #todo BIG_TODO what about verbose name
    bankRefId = models.CharField(verbose_name=_("bankRefId"),max_length=100)
    status = models.CharField(verbose_name=_("status"),max_length=10, choices=SATAUS_CHOICES)
    statusNum = models.IntegerField(verbose_name=_("status number"))
    # gateway = models.ForeignKey(Gateway,verbose_name=_("gateway"), on_delete=models.PROTECT)
    authority = models.CharField(verbose_name=_("authority"),max_length=20)
    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return str(self.pk)+"_"+self.invoice.seller.branch_name.branch_name

    # def get_absolute_url(self):
    #     return reverse('app_name_transactions_detail', args=(self.pk,))
    #



class DiscountCode(models.Model): #FIRST MODEL OF DISCOUNTING we use it in invoice
    # is_used = models.BooleanField(default=False)
    code = models.CharField(max_length=64, db_index=True, unique=True, blank=True,
                            help_text='It will be fill, if you leave it empty. ex: cz6nX')
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    maximum_value = models.IntegerField(default=0) #TODO needed?
    expire_at = models.DateField()
    # inventory = models.IntegerField(default=1)
    # one_time = models.BooleanField(default=False) #todo ??????
    def __str__(self):
        return self.code


class OccasionalDiscount(models.Model): #Second way of discounting : it makes impact in product variation discount price
    title=models.CharField(max_length=200)
    # product_variation=models.ForeignKey(ProductVariation)
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    #TODO BIG todo : make sure just related items see this

    def __str__(self):
        return self.title  #+"_"+str(self.id)

class PromotionCodeStrategy(models.Model):
    # minimum_expendable_value = models.IntegerField(default=0)
    # maximum_expendable_value = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0) #todo ??????????
    expire_time = models.IntegerField(default=5)
    is_for_first_order = models.BooleanField(default=False)
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    maximum_value = models.IntegerField(default=0)

class PromotionalCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, db_index=True, unique=True, blank=True,
                            help_text='It will be fill, if you leave it empty. ex: cz6nX')
    # inventory = models.IntegerField() #todo ??????????????
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    # minimum_expendable_value = models.IntegerField(default=0)
    maximum_value = models.IntegerField(default=0)
    num_of_used = models.IntegerField(default=0, editable=False) # ye adad bezar va har dafe tyeki azash kam kon

    expire_at = models.DateField()
    disable =  models.BooleanField(default=False)

    # strategy = models.ForeignKey(PromotionCodeStrategy,on_delete=models.DO_NOTHING,null=True)