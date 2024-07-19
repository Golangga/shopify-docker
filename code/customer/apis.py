from datetime import datetime
from tokenize import Single
from typing import List
from urllib import response
from typing import Optional
from urllib.error import HTTPError
# from urllib import response
from ninja import NinjaAPI, Query

from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from django.contrib.auth.hashers import make_password

from .models import User,Customer,Address
from .schema import CustomerOut, CustomerResp, AddressIn, AddressResp, AddressOut, CustomerIn

api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.get("hello")
def helloWorld(request):
    return{'hello':'world'}

@api.get("customers.json", auth=apiAuth, response=CustomerResp)
def getAllCustomers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers': customers}

# Searches for customers that match a supplied query
@api.get('customers/search.json', auth=apiAuth, response=CustomerResp)
def searchCustomers(request, query: str = Query(...)):
    # Extract email,etc from query string
    email_query = query.split(':')[1] if 'email:' in query else None
    fisrt_name_query = query.split(':')[1] if 'fisrt_name:' in query else None
    last_name_query = query.split(':')[1] if 'last_name:' in query else None
    if email_query:
        customers = Customer.objects.filter(user__email=email_query)
    elif fisrt_name_query:
        customers = Customer.objects.filter(user__first_name=fisrt_name_query)
    elif last_name_query:
        customers = Customer.objects.filter(user__last_name=last_name_query)
    return {'customers': customers}

# Count all Customers
@api.get('customers/count.json', auth=apiAuth)
def getCustomerCount(request):
    customer_count = Customer.objects.count()
    return {"customer_count": customer_count}

# Single Customer
@api.get('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def getCustomerById(request, id_cust: int):
    customer = Customer.objects.get(pk=id_cust)
    return customer


# Create Customer
@api.post('customers.json', auth=apiAuth, response=CustomerOut)
def createCustomer(request, data: CustomerIn):
    user, created = User.objects.get_or_create(
        email=data.email,
        defaults={'first_name': data.first_name, 'last_name': data.last_name, 'username': data.username, 'password': make_password(data.password)}
    )

    if created:
        new_customer = Customer.objects.create(
            user=user,
            phone=data.phone,
            state=data.state,
            currency=data.currency
        )
        return new_customer
    else:
        return api.create_response(request, {"detail": "User already exists"}, status=400)


# Update Customer
@api.put('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def updateCustomer(request, id_cust: int, data: CustomerIn):
    customer = Customer.objects.get(pk=id_cust)
    user = customer.user
    
    if data.email:
        user.email = data.email
    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    user.save()
    
    if data.phone:
        customer.phone = data.phone
    if data.state:
        customer.state = data.state
    if data.currency:
        customer.currency = data.currency
    customer.save()
    
    return customer


    
# Delete Customers
@api.delete('customers/{id_cust}.json')
def deleteCust(request, id_cust:int):
    Customer.objects.get(pk=id_cust).delete()
    return {}