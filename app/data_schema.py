from pydantic import BaseModel
from typing import TypeVar, Optional, List
from datetime import datetime


# [{
#       "account_id": "LDKe37WMRviZdb8NKQqWFNNlKRmbk9FkjWeLo",
#       "account_owner": null,
#       "amount": 5.4,
#       "authorized_date": "2024-01-24",
#       "authorized_datetime": null,
#       "category": [
#         "Travel",
#         "Taxi"
#       ],
#       "category_id": "22016000",
#       "check_number": null,
#       "counterparties": [
#         {
#           "confidence_level": "VERY_HIGH",
#           "entity_id": "eyg8o776k0QmNgVpAmaQj4WgzW9Qzo6O51gdd",
#           "logo_url": "https://plaid-merchant-logos.plaid.com/uber_1060.png",
#           "name": "Uber",
#           "phone_number": null,
#           "type": "merchant",
#           "website": "uber.com"
#         }
#       ],
#       "date": "2024-01-25",
#       "datetime": null,
#       "iso_currency_code": "USD",
#       "location": {
#         "address": null,
#         "city": null,
#         "country": null,
#         "lat": null,
#         "lon": null,
#         "postal_code": null,
#         "region": null,
#         "store_number": null
#       },
#       "logo_url": "https://plaid-merchant-logos.plaid.com/uber_1060.png",
#       "merchant_entity_id": "eyg8o776k0QmNgVpAmaQj4WgzW9Qzo6O51gdd",
#       "merchant_name": "Uber",
#       "name": "Uber 063015 SF**POOL**",
#       "payment_channel": "online",
#       "payment_meta": {
#         "by_order_of": null,
#         "payee": null,
#         "payer": null,
#         "payment_method": null,
#         "payment_processor": null,
#         "ppd_id": null,
#         "reason": null,
#         "reference_number": null
#       },
#       "pending": false,
#       "pending_transaction_id": null,
#       "personal_finance_category": {
#         "confidence_level": "VERY_HIGH",
#         "detailed": "TRANSPORTATION_TAXIS_AND_RIDE_SHARES",
#         "primary": "TRANSPORTATION"
#       },
#       "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_TRANSPORTATION.png",
#       "transaction_code": null,
#       "transaction_id": "3AjEaeqPW4uGoN7a1MrKiyaAmdp6VKUZllZ54",
#       "transaction_type": "special",
#       "unofficial_currency_code": null,
#       "website": "uber.com"
#     }]

[{
    "amount": 89.4,
    "category": ["", ""],
    "date": "2024-03-21",
    "name": "SparkFun"
}]

class Account(BaseModel):
    name: str
    current: float
    type: str
    
class Transaction(BaseModel):
    amount: float
    category: str
    date: datetime
    name: str

class NetWorth(BaseModel):
    date: datetime
    networth: float
    
    
    
    
#  Line Charts > Basic
# [
#     {
#         name: "Desktops",
#         data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
#     }
# ]



# Column with Markers
# [
#       {
#         x: '2011',
#         y: 1292,
#         goals: [
#           {
#             name: 'Expected',
#             value: 1400,
#             strokeHeight: 5,
#             strokeColor: '#775DD0'
#           }
#         ]
#       }
# ]




# Simple Pie
# series: [44, 55, 13, 43, 22],
# chart: {
#     width: 380,
#     type: 'pie',
# },
# labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E']





#  Radar – Multiple Series
# [{
#     name: 'Series 1',
#     data: [80, 50, 30, 40, 100, 20],
# }, 
# {
#     name: 'Series 2',
#     data: [20, 30, 40, 80, 20, 80],
# }, 
# {
#     name: 'Series 3',
#     data: [44, 76, 78, 13, 43, 10],
# }]