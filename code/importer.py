import os
import sys
import django
import json

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopify.settings'
print("DJANGO_SETTINGS_MODULE is set to:", os.environ['DJANGO_SETTINGS_MODULE'])

django.setup()
print("Django has been set up.")

from discount.models import PriceRule

filepath = './dummy-data/'

# Import PriceRule data  
with open(filepath+'pricerule.json') as jsonfile:  
    pricerules = json.load(jsonfile)  
for pricerule in pricerules:  
    PriceRule.objects.create(  
        id=pricerule['id'],  
        title=pricerule['title'],  
        target_type=pricerule['target_type'].strip(),  
        target_selection=pricerule['target_selection'].strip(),  
        allocation_method=pricerule['allocation_method'],  
        value_type=pricerule['value_type'],  
        # value_type_list=pricerule['value'],  
        value=pricerule['value'],  
        starts_at=pricerule['starts_at'],  
        ends_at=pricerule['ends_at'],  
        created_at=pricerule['created_at'],  
        updated_at=pricerule['updated_at']  
    )  

# # Import User and Customer Data
# with open(filepath + 'customer.json') as jsonfile:
#     customers = json.load(jsonfile)
#     for cust in customers:
#         exitUser = User.objects.filter(email=cust['email']).first()
#         if exitUser is None:
#             user = User.objects.create_user(username=cust['email'], email=cust['email'],
#                                             password=cust['password'],
#                                             first_name=cust['first_name'],
#                                             last_name=cust['last_name'])

#             exitCust = Customer.objects.filter(user=user).first()
#             if exitCust is None:
#                 Customer.objects.create(user=user,
#                                         created_at=cust['created_at'],
#                                         updated_at=cust['created_at'],
#                                         state=cust['state'],
#                                         verified_email=cust['verified_email'],
#                                         send_email_welcome=cust['send_email_welcome'],
#                                         currency=cust['currency'],
#                                         phone=cust['phone'])

# # Import Address Data
# with open(filepath + 'address.json') as jsonfile:
#     address = json.load(jsonfile)
#     for num, adr in enumerate(address):
#         addrExist = Address.objects.filter(id=num+1).first()
#         if addrExist is None:
#             customer_exists = Customer.objects.filter(id=adr['customer']).exists()
#             if customer_exists:
#                 Address.objects.create(
#                     customer_id=adr['customer'],
#                     address1=adr['address1'],
#                     address2=adr['address2'],
#                     city=adr['city'],
#                     province=adr['province'],
#                     country=adr['country'],
#                     company=adr['company'],
#                     phone=adr['phone'],
#                     zip=adr['zip'],
#                     default=adr['default']
#                 )
#             else:
#                 print(f"Customer with ID {adr['customer']} does not exist. Skipping address entry.")

# # Import Metafields
# with open(filepath + 'metafield.json') as jsonfile:
#     metafields = json.load(jsonfile)
#     for meta in metafields:
#         Metafield.objects.create(
#             description=meta['description'],
#             key=meta['key'],
#             namespace=meta['namespace'],
#             owner_id=meta['owner_id'],
#             owner_resource=meta['owner_resource'],
#             value=meta['value'],
#             type=meta['type']
#         )
