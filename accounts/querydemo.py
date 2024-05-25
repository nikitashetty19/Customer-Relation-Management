# #1 Returns all customer from customer tables
# customers=Customer.objects.all()
# #2 return fristcustomer
# print(customers.first())
# #3 returns single cust name
# cust1=Customer.objects.get(id=1)
# #4returns customers email
# print(cust1.email)

# #5 return all orders of a specific customer
# method 1:top down approach
# orders=cust2.order_set.all()

# method 2:bottom up
# orders=Order.objects.filter(customer__id="2")

# #6 return using filter and chaining
# products=Product.objects.filter(category="Outdoor",name="Ball")

# #7 sort using order_by using some parameter and reverse
# products=Product.objects.all().order_by("name")
# products=Product.objects.all().order_by("-name")

# #8 many to many relationship
# products=Product.objects.filter(tags__name="Summer")

# #9 returns total count for no of times a ball was ordered by cust2
#  no=cust2.order_set.filter(product__name="Ball").count()

# #10 returns total count for each product  ordered by cust2
# for order in cust2.order_set.all():
# ...     if order.product.name in allOrders:
# ...             allOrders[order.product.name] += 1
# ...     else:
# ...             allOrders[order.product.name] = 1
# ...
# >>> print(allOrders)
# {'Ball': 1, 'BBQ Grill': 1} #output