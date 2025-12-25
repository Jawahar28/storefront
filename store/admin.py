from django.contrib import admin, messages
from . import models
from django.db.models import Count, QuerySet
from django.http import HttpResponse
from django.utils.html import format_html, urlencode, format_html_join
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem


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

'''@admin.register(models.Product)
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
        return "OK"'''

'''@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 20'''

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
    search_fields = ['title']

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


'''@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'total_orders' ,'orders']
    list_editable = ['membership']
    # ordering = ['first_name', 'last_name'] 
    list_per_page = 20

    # Total number of Orders
    @admin.display(ordering='total_orders',description='Orders')
    def total_orders(self, customer):
        if customer.total_orders == 0:
            return 0
        
        url = (
            reverse('admin:store_order_changelist') +
            '?' +
            urlencode(
                {
                    'customer__id' : customer.id
                }
            )
        )

        return format_html('<a href="{}"> {}</a>', url, customer.total_orders)

    # Each Orders ordered by the customer
    @admin.display(description = 'Orders')
    def orders(self, customer):
        ordered = customer.order_set.all()

        if not ordered:
            return '-' 
        return format_html_join(
        ', ',
        '<a href="{}">{}</a>',
        (
            (
                reverse('admin:store_order_change', args=[order.id]),
                order.id
            )
            for order in ordered
        )
    )

    def get_queryset(self, request:HttpResponse) -> QuerySet:
        return (
        super()
        .get_queryset(request)
        .annotate(total_orders = Count('order'))
        .prefetch_related('order_set')
        )'''
        

#<------------------------------------------------------------------------------------------------------------------->

# Adding Search to the List Page

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'total_orders' ,'orders']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name'] 
    list_per_page = 20
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # Total number of Orders
    @admin.display(ordering='total_orders',description='Orders')
    def total_orders(self, customer):
        if customer.total_orders == 0:
            return 0
        
        url = (
            reverse('admin:store_order_changelist') +
            '?' +
            urlencode(
                {
                    'customer__id' : customer.id
                }
            )
        )

        return format_html('<a href="{}"> {}</a>', url, customer.total_orders)

    # Each Orders ordered by the customer
    @admin.display(description = 'Orders')
    def orders(self, customer):
        ordered = customer.order_set.all()

        if not ordered:
            return '-' 
        return format_html_join(
        ', ',
        '<a href="{}">{}</a>',
        (
            (
                reverse('admin:store_order_change', args=[order.id]),
                order.id
            )
            for order in ordered
        )
    )

    def get_queryset(self, request:HttpResponse) -> QuerySet:
        return (
        super()
        .get_queryset(request)
        .annotate(total_orders = Count('order'))
        .prefetch_related('order_set')
        )


#<------------------------------------------------------------------------------------------------------------------->

# Adding Filtering to the page

# Customizing the filter results
'''class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
           return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): 
    list_display = ['title', 'unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price'] 
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 100 # pagination
    list_select_related = ['collection']

    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return "OK"'''

#<------------------------------------------------------------------------------------------------------------------->

# Adding Custom Actions

'''class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
           return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): 
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price'] 
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 100 # pagination
    list_select_related = ['collection']

    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return "OK"

    @admin.action(description='clear_inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f"{updated_count} products were updated successfully",
            messages.ERROR
        )'''

#<------------------------------------------------------------------------------------------------------------------->

# Customizing Forms : Adding or Updating models.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
           return queryset.filter(inventory__lt=10)



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin): 
    # fields = ['title','slug'] # It helps to show the presented fields only
    # exclude = ['promotions'] # It excludes the presented field in the list
    # readonly_fields = ['title'] # It reads only the presented fields in the list
    
    # Setting Slug field automatically
    prepopulated_fields = {
        'slug': ['title']
    } 

    # Making selection easily
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price'] 
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 100 # pagination
    list_select_related = ['collection']
    search_fields = ['title']
    # inlines = [TagInline]

    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return "OK"

    @admin.action(description='clear_inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f"{updated_count} products were updated successfully",
            messages.ERROR
        )


#<------------------------------------------------------------------------------------------------------------------->

# Editing children using inlines

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_per_page = 20