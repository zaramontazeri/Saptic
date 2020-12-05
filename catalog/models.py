from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Catalog (models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"), upload_to="catalog/",
                              height_field=None, width_field=None, max_length=None)


class PageLayout (models.Model):
    page_number = models.IntegerField()
    title = models.CharField(_("title"), max_length=50)


class LayoutCatalog(models.Model):
    catalog = models.ForeignKey("catalog.Catalog", related_name="layoutcatalog", verbose_name=_(
        "catalog"), on_delete=models.CASCADE)
    page = models.ForeignKey("catalog.PageLayout", related_name="layoutpage", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    x = models.IntegerField(_("X"))
    y = models.IntegerField(_("Y"))
    w = models.IntegerField(_("H"))
    h = models.IntegerField(_("H"))
    el_id = models.CharField(_(""), max_length=50)


class Slider(models.Model):
    description = models.TextField()
    image = models.ImageField(_("slider"), upload_to="sliders")