from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

# Defining Many to Many relationships
# Promotion -> Products and Products -> Promotions
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        
    

class Product(models.Model): # Inheriting the model.Model class from Django
    # Feilds of this class
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits = 10, 
                                    decimal_places = 2, 
                                    validators = [MinValueValidator(1)])
    inventory =  models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    collection = models.ForeignKey(Collection, on_delete= models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True) # related_name= 'products' Here related_name is used as alternative name for understanding

    def __str__(self):
        return self.title

    '''class Meta:
        ordering = ['title']  '''  


class Customer(models.Model):
    # These are defined because whenever we want to update the default value it might occurs issues ,
    # To Avoid this, we define these attributes and passed to the choices field
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    # CHOICES 
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(unique= True) # Unique email for each customer
    phone = models.CharField(max_length = 255)
    birth_date = models.DateField(null = True) # Optional Feild
    membership =  models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default = MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name']
    

    '''class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]'''
    
    '''class Meta:
        indexes = [
            models.Index(fields=['given_name'])
        ]'''
class Order(models.Model):

    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
        
    PAYMENT_CHOICES = [
            (PAYMENT_PENDING, 'Pending'),
            (PAYMENT_COMPLETE, 'Complete'),
            (PAYMENT_FAILED, 'Failed'),
        ]
        
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices= PAYMENT_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

# Implementing One to One Relationship
'''class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
'''

# Implementing One to Many Relationship
class Address(models.Model):
    # zip = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


    

