from django.contrib import admin
from . import models
from django.db.models import Count, QuerySet
from django.http import HttpResponse
from django.utils.html import format_html, urlencode
from django.urls import reverse


# Register your models here.


# Registering the models in the admin page
'''admin.site.register(models.Collection)

admin.site.register(models.Product)

admin.site.register(models.Customer)'''

#<------------------------------------------------------------------------------------------------------------------->


# Customizing the list page
'''@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): # With this class we can specify how we want to view or edit our model classes
    list_display = ['title', 'unit_price'] # Helps to display the fields
    list_editable = ['unit_price'] # Helps to edit the values/ make changes
    list_per_page = 10 # pagination'''

# If we dont want to use decorator then we need to pass the adminclass to the register
# admin.site.register(models.Product, ProductAdmin)

'''@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    # ordering = ['first_name', 'last_name'] 
    list_per_page = 20'''

#<------------------------------------------------------------------------------------------------------------------->

# Adding Computed Columns

'''@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): # With this class we can specify how we want to view or edit our model classes
    list_display = ['title', 'unit_price', 'inventory_status'] # Helps to display the fields
    list_editable = ['unit_price'] # Helps to edit the values/ make changes
    list_per_page = 100 # pagination
    
    # To sort the created column we need to use decorator
    @admin.display(ordering = 'inventory')
    # To add a new column in the admin we need to create this type of function
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return "OK"'''

#<------------------------------------------------------------------------------------------------------------------->

# Loading Related Objects

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): 
    list_display = ['title', 'unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price'] 
    list_per_page = 100 # pagination
    list_select_related = ['collection']

    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return "OK"

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 20

#<------------------------------------------------------------------------------------------------------------------->

# Overriding the base queryset

'''@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request: HttpResponse) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )'''


#<------------------------------------------------------------------------------------------------------------------->

# Providing Links to Other pages
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        #reverse('admin:app_model_page')
        url = (
            reverse('admin:store_product_changelist') + 
            '?' +
            urlencode({
                'collection__id' : str(collection.id)
            })
        )

        return format_html('<a href="{}"> {}</a>',url, collection.products_count)
        
    
    def get_queryset(self, request: HttpResponse) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'ordered_id']
    list_editable = ['membership']
    # ordering = ['first_name', 'last_name'] 
    list_per_page = 20

    @admin.display(ordering='first_name')
    def ordered_id(self, order):
        

