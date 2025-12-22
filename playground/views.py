from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer, Collection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction, connection

# Create your views here.
# @transaction.atomic() # Decrator or context manager : This will wrap all the code inside the function
def say_hello(request):
    # return HttpResponse("Hello World!")

    # To see/ use all the data
    '''queryset = Product.objects.all()

    for prod in queryset:
        print(prod)'''
    
    # To Retreive some data 
    '''product = Product.objects.get(pk=1)'''

    # Suppose We try to retreive the data which doesn't exist
    '''try:
        product = Product.objects.get(pk=0)
    except ObjectDoesNotExist:
        pass'''
    
    # Alternative of try-except block : We can use filter
    '''product = Product.objects.filter(pk=0).first()'''

    # To check the existence of object
    '''exists = Product.objects.filter(pk=1).exists()'''

    # Filtering the data
    '''queryset = Product.objects.filter(unit_price__gt = 20)'''

    # Filtering with grouping
    '''queryset = Product.objects.filter(collection__id = 3, unit_price__gt = 20)'''

    # Complex QUery using Q objects
    '''queryset = Product.objects.filter(Q(inventory__lt = 10) | Q(unit_price__lt = 20))'''

    # Referencing Fields using f objects
    '''queryset = Product.objects.filter(inventory = F('unit_price'))'''

    # Sorting Data
    '''queryset = Product.objects.order_by('title') # Ascending Order'''
    '''queryset = Product.objects.order_by('-title') # Descending Order'''

    # Sorting Data with multiple fields
    '''queryset = Product.objects.order_by('unit_price', '-title')'''


    # Accessing the particular object
    '''product = Product.objects.order_by('unit_price')[0]
    product = Product.objects.earliest('unit_price)

    product = Product.objects.latest('unit_price')
    return render(request, 'hello.html', {'name': 'Jawahar', 'product': product})'''


    #Limiting Results
    '''queryset = Product.objects.all()[:5]'''

    # Selecting some particular fields
    '''queryset = Product.objects.values('id', 'title', 'unit_price')[:5]'''
    '''queryset = Product.objects.values('id','title','unit_price','collection__title')[:5]'''

    # Exercise : Select Products that have been ordered and sort them by title
    '''queryset = Product.objects.filter(orderitem__order__isnull = False).order_by('title') # Using only orderitem table

    # Solution using OrderItem Tables
    queryset = Product.objects.filter(id__in = OrderItem.objects.values('product_id').distinct()).order_by('title')'''
    
    # Deferring Fields
    '''queryset = Product.objects.only('id', 'title')
    queryset = Product.objects.defer('description')'''

    # Selecting Related Fields
    '''queryset = Product.objects.select_related('collection').all()'''

    # Prefetching Related Fields
    '''queryset = Product.objects.prefetch_related('promotions').all()'''

    # Combining select_related and prefetch_related
    '''queryset = Product.objects.select_related('collection').prefetch_related('promotions').all()'''
    # return render(request, 'hello.html', {'name': 'Jawahar', 'products' : list(queryset)}) # Here render function is used to render the HTML file


    # Exercise : Get the last 5 orders with their customer and items
    '''queryset = Order.objects.select_related('customer').prefetch_related('items__product').order_by("-placed_at")[:5]
    return render(request, "exercise.html", {'orders' : list(queryset)})
'''
    # Aggregate bjects
    '''result = Product.objects.aggregate(count = Count('id'), min_price = Min('unit_price'))
    return render(request, 'aggregate.html', {'name': 'Jawahar', 'result': result})'''


    # Annotate Objects
    # Value Function :
    '''queryset = Customer.objects.annotate(is_new=Value(True))'''
    # F function
    '''queryset = Customer.objects.annotate(new_id = F('id')+1)'''
    # Func Function
    '''queryset = Customer.objects.annotate(
        full_name = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    )'''

    # Annotate exercise
    # 1. Customer with their last order ID
    '''queryset = Customer.objects.annotate(last_order_id = Max('order__id'))
    return render(request, 'exercise.html', {'customers' : list(queryset)})'''

    # 2. Collections and count of their products
    '''queryset = Collection.objects.annotate(products_count = Count('product__id'))
    return render(request, 'exercise.html', {'result' : list(queryset)})'''

    # 3, Customers with more than 5 orders
    '''customers = Customer.objects.annotate(orders_count = Count('order'))
    return render(request, 'exercise.html', { 'result' : customers.filter(orders_count__gt = 5)})'''

    # 4. Customers and the total amount they've spent
    '''amount_spent = Customer.objects.annotate(
        total_amount = Sum(
            F('order__items__unit_price') * F('order__items__quantity')))
    return render(request, 'exercise.html', {'result' : list(amount_spent)})'''

    #5. Top 5- best selling products and their total sales
    '''products = Product.objects.annotate(
        total_sales = Sum(
            F('orderitem__unit_price') * F('orderitem__quantity'))
    ).order_by('-total_sales')[:5]
    return render(request, 'exercise.html', {'result' : products})'''

    # Exprssion Wrapper
    '''discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field = DecimalField())
    queryset = Product.objects.annotate(discounted_price = discounted_price)
    return render(request, 'hello.html', {'name': 'Jawahar', 'result': list(queryset)})'''

    # Querying Generic Expressions
    '''content_type = ContentType.objects.get_for_model(Product)
    queryset = TaggedItem.objects\
        .select_related('tag')\
            .filter(
                content_type = content_type,
                object_id = 1
    )

    return render(request, 'hello.html', {'name' : 'Jawahar','tags' : list(queryset) })'''

    # Custom Managers
    '''queryset = TaggedItem.objects.get_tags_for(Product,1)

    return render(request, 'hello.html', {'name' : 'Jawahar','tags' : list(queryset) })'''

    # QuerySet Caching
    '''queryset = Product.objects.all()
    list(queryset)
    # list(queryset)
    queryset[0]


    return render(request, 'hello.html', {'name': 'Mosh' })'''

    #<------------------------------------------------------------------------------------------->

    # Creating Objects/ Inserting a record to the database

    '''collection = Collection()
    collection.title = 'Video Games'
    
    collection.featured_product = Product(pk=1) # / collection.featured_product_id = 1

    collection.save()

    # Second way of creating
    # Collection.objects.create(title = 'a' , featured_product_id = 1)

    return render(request, 'hello.html', {'name': 'Jawahar'})'''

    # < ------------------------------------------------------------------------------------------>

    # Updating objects in the database

    # 1. This method might lead to erase of the data , if we miss fields
    '''collection = Collection(pk = 11)
    collection.title = 'Games'
    collection.features_product = None
    collection.save()'''

    # 2. To overcome the method 1 : we use get method to retreive the data
    '''collection = Collection.objects.get(pk=11)
    collection.featured_product = None
    collection.save()'''

    # 3. To avoid the reading of the object we use update method
    '''Collection.objects.filter(pk=11).update(featured_product = None)

    return render(request, 'hello.html' , {'name' : 'Jawahar'})'''

#<------------------------------------------------------------------------------------------>
 
    # Deleting objects

    # Method 1 :
    '''collection = Collection(pk=11)
    Collection.delete()'''

    # Method 2:
    '''Collection.objects.filter(pk=11).delete()'''


#<-------------------------------------------------------------------------------------------->

    # Transactions : @transaction.atomic() -> used at top of the function 
    '''with transaction.atomic(): # With this we can make/see the what we want to be in a transaction
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'hello.html', {'name': 'Jawahar'})'''

#<----------------------------------------------------------------------------------------------------->
    # Executing raw SQL queries
    # 1. We can directly write SQL queries using raw method
    #    Use this only for working on complex queries

    '''queryset = Product.objects.raw('SELECT * FROM store_product')
    return render(request, 'hello.html', {'name':'Jawahar', 'result':list(queryset)})'''

    # 2. We can use connection when we want to retrieve the data that is not present in our database
   ''' with connection.cursor() as cursor:
        cursor.execute('') # Here we can use insert, select, update, delete

    return render(request, 'hello.html', {'name': 'Jawahar', 'result': list(queryset)})'''

    

    


    
