import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopify.settings'
import django
django.setup()

import json
from customer.models import User, Customer, Address
# from metafield.models import Metafield

filepath = './dummy-data/'

with open(filepath+'customer.json') as jsonfile:
    customers = json.load(jsonfile)
    for cust in customers:
        exitUser = User.objects.filter(email=cust['email']).first()
        if exitUser == None:
            user = User.objects.create_user(username=cust['email'], email=cust['email'],
                                            password=cust['password'],
                                            first_name=cust['first_name'],
                                            last_name=cust['last_name'])
            
            exitCust = Customer.objects.filter(user=user).first()
            if exitCust == None:
                Customer.objects.create(user=user, 
                                        created_at=cust['created_at'],
                                        updated_at=cust['created_at'],
                                        state=cust['state'],
                                        verified_email=cust['verified_email'],
                                        send_email_welcome=cust['send_email_welcome'],
                                        currency=cust['currency'],
                                        phone=cust['phone'])

with open(filepath+'address.json') as jsonfile:
    address = json.load(jsonfile)
    for num, adr in enumerate(address):
        addrExist = Address.objects.filter(id=num+1).first()
        if addrExist == None:
            Address.objects.create(customer_id=adr['customer'],
                                   address1=adr['address1'],
                                   address2=adr['address2'],
                                   city=adr['city'],
                                   province=adr['province'],
                                   country=adr['country'],
                                   company=adr['company'],
                                   phone=adr['phone'],
                                   zip=adr['zip'], default=adr['default'])

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