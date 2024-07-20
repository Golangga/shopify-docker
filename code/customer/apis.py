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
from discount.models import PriceRule
from .schema import CustomerOut, CustomerResp, AddressIn, AddressResp, AddressOut, CustomerIn
from discount.schema import PriceRuleIn, PriceRuleOut, PriceRuleResp

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

@api.post('customers/{id_cust}/addresses.json', auth=apiAuth, response=AddressResp)
def addCustomer(request, id_cust:int, data:AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    newAddr = Address.objects.create(
                customer=cust,
                address1=data.address1,
                address2=data.address2,
                city=data.city,
                province=data.province,
                company=data.company,
                phone=data.phone,
                zip=data.zip
            )
    return {"customer_address": newAddr}

# Retrieves a list of addresses for a customer
@api.get('customers/{id_cust}/addresses.json', auth=apiAuth, response=List[AddressOut])
def getCustomerAddresses(request, id_cust: int):
    addresses = Address.objects.filter(customer_id=id_cust)
    return addresses

# Retrieves details for a single customer address
@api.get('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressResp)
def getCustomerAddress(request, id_cust: int, id_addr: int):
    try:
        address = Address.objects.get(customer_id=id_cust, id=id_addr)
        return {"customer_address": address}
    except Address.DoesNotExist:
        return api.create_response(status=404, content={"detail": "Address not found"})

# Set Default Address
@api.put('customers/{id_cust}/addresses/{id_addr}/default.json', auth=apiAuth, response=AddressResp)
def setDefaultAddr(request, id_cust:int, id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default =True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()

    return {"customer_address": addr}

# Delete Address
@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def deleteAddr(request, id_cust:int, id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

# Update Address
@api.put('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressOut)
def updateCustomerAddress(request, id_cust: int, id_addr: int, data: AddressIn):
    address = Address.objects.get(pk=id_addr, customer_id=id_cust)
    address.address1 = data.address1
    address.address2 = data.address2
    address.city = data.city
    address.province = data.province
    address.company = data.company
    address.phone = data.phone
    address.zip = data.zip
    address.first_name = data.first_name
    address.last_name = data.last_name
    address.save()
    return address

#All PriceRules  
@api.get("price_rules.json", auth=apiAuth, response=List[PriceRuleOut])  
def get_price_rules(request):  
    price_rules = PriceRule.objects.all()  
    return price_rules

#Count PriceRules
@api.get("price_rules/count.json", auth=apiAuth)  
def get_price_rule_count(request):  
    count = PriceRule.objects.count()  
    return {"count": count}  

#Single PriceRule
@api.get("price_rules/{id}.json", auth=apiAuth, response=PriceRuleOut)  
def get_price_rule(request, id: int):  
    price_rule = PriceRule.objects.get(pk=id)  
    return price_rule  

#Create PriceRule  
@api.post("price_rules.json", auth=apiAuth, response=PriceRuleResp)
def create_price_rule(request, payload: PriceRuleIn):
    try:
        price_rule = PriceRule(
            title=payload.title,
            target_type=payload.target_type,
            target_selection=payload.target_selection,
            allocation_method=payload.allocation_method,
            value_type=payload.value_type,
            value=payload.value,
            starts_at=datetime.now()  
        )
        price_rule.save()
        return {"price_rule": price_rule}
    except Exception as e:
        raise HTTPError(400, str(e))

# Update PriceRule
@api.put("price_rules/{id}.json", auth=apiAuth, response=PriceRuleResp)
def update_price_rule(request, id: int, payload: PriceRuleIn):
    try:
        price_rule = PriceRule.objects.get(id=id)
        price_rule.title = payload.title
        price_rule.target_type = payload.target_type
        price_rule.target_selection = payload.target_selection
        price_rule.allocation_method = payload.allocation_method
        price_rule.value_type = payload.value_type
        price_rule.value = payload.value
        price_rule.updated_at = datetime.now()
        price_rule.save()
        return {"price_rule": price_rule}
    except PriceRule.DoesNotExist:
        raise HTTPError(404, "PriceRule not found")
    except Exception as e:
        raise HTTPError(400, str(e))
  
# Delete PriceRule
@api.delete("price_rules/{id}.json", auth=apiAuth)
def delete_price_rule(request, id: int):
    try:
        price_rule = PriceRule.objects.get(id=id)
        price_rule.delete()
        return {"message": "PriceRule deleted successfully"}
    except PriceRule.DoesNotExist:
        raise HTTPError(404, "PriceRule not found")
    except Exception as e:
        raise HTTPError(400, str(e))