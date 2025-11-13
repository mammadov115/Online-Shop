from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

# Models for multilingual product catalog (Category and Product)
# The Category model supports translations using django-parler.

class Category(TranslatableModel):
    """
    Represents a product category with multilingual support.
    
    Uses django-parler's TranslatableModel to store translations
    for fields such as `name` and `slug`.
    """
    
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200,unique=True)
        )

    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name'])
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        """
        Returns the string representation of the category.
        """  
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to the list of products filtered by this category.
        """
        return reverse('shop:product_list_by_category',args=[self.slug])


class Product(models.Model):
    """
    Represents a single product in the catalog.

    Each product belongs to a category and contains information such as
    name, slug, image, description, price, and availability.
    """
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id','slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        """
        Returns the string representation of the product.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to the product's detail page.
        """
        return reverse('shop:product_detail',args=[self.id,self.slug])
