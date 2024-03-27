import base64
import os
import datetime as dt
import json
import time
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

from app.schema import *
from app.service.auth import AuthService
from app.service.user import UserService
from app.service.feature_engineering import *



load_dotenv()


# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'auth').split(',')

# PLAID_COUNTRY_CODES is a comma-separated list of countries for which users
# will be able to select institutions from.
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')



def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value

host = plaid.Environment.Sandbox

if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox

if PLAID_ENV == 'development':
    host = plaid.Environment.Development

if PLAID_ENV == 'production':
    host = plaid.Environment.Production

# Parameters used for the OAuth redirect Link flow.
#
# Set PLAID_REDIRECT_URI to 'http://localhost:3000/'
# The OAuth redirect flow requires an endpoint on the developer's website
# that the bank website should redirect to. You will need to configure
# this redirect URI for your client ID through the Plaid developer dashboard
# at https://dashboard.plaid.com/team/api.
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))


# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_id is only relevant for the UK Payment Initiation product.
# We store the payment_id in memory - in production, store it in a secure
# persistent data store.
payment_id = None
# The transfer_id is only relevant for Transfer ACH product.
# We store the transfer_id in memory - in production, store it in a secure
# persistent data store.
transfer_id = None

item_id = None

router = APIRouter(
    prefix="/api/plaid",
    tags=['plaid']
)

# current_user: UserInDB = Depends(AuthService.get_current_user)
@router.get("/create_link_token", response_model=None, response_model_exclude_none=True)
def create_link_token():
    print("products ==================================")
    print(products)
    try:
        request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Quickstart",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        if PLAID_REDIRECT_URI!=None:
            request['redirect_uri']=PLAID_REDIRECT_URI
    # create link token
        response = client.link_token_create(request)
        print("response ==================================")
        print(response.to_dict())
        return JSONResponse({"link_token": response.to_dict()["link_token"]})
    except plaid.ApiException as e:
        print("e.body ==================================")
        print(e.body)
        return json.loads(e.body)


# Exchange token flow - exchange a Link public_token for
# an API access_token
# https://plaid.com/docs/#exchange-token-flow


# , current_user: UserInDB = Depends(AuthService.get_current_user)
@router.post("/exchange_public_token", response_model=None, response_model_exclude_none=True)
async def get_access_token(request: PlaidPublicTokenIn, current_user: UserInDB = Depends(AuthService.get_current_user)):
    global access_token
    global item_id
    global transfer_id
    public_token = request.public_token
    print("exchange_public_token start")
    print(public_token)
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token)
        exchange_response = await client.item_public_token_exchange(exchange_request)
        plaid_access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        
        # Update user data here
        await UserService.set_plaid_access_token(current_user.id, plaid_access_token, item_id)
        
        print("exchange_public_token response ==================================")
        print(exchange_response.to_dict())
        return JSONResponse(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)

@router.get("/transactions", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_transactions(current_user: UserInDB = Depends(AuthService.get_current_user)):
    print(current_user)
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")
    
    # Set cursor to empty to receive all historical updates
    cursor = ''

    # New transaction updates since "cursor"
    added = []
    modified = []
    removed = [] # Removed transaction ids
    has_more = True
    try:
        # Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
                access_token=current_user.plaid_access_token,
                cursor=cursor,
            )
            response = client.transactions_sync(request).to_dict()
            # Add this page of results
            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']
            # Update cursor to the next cursor
            cursor = response['next_cursor']
            

        # Return the 8 most recent transactions
        formatted_trans = extract_data_from_transactions(added)
        
        # pretty_print_response(formatted_trans)
        return ResponseSchema(detail="Successfully received transactions data", result={'latest_transactions': formatted_trans})

    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)
    
    
@router.get('/balance', response_model=ResponseSchema, response_model_exclude_none=True)
async def get_balance(current_user: UserInDB = Depends(AuthService.get_current_user)):
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")
    
    try:
        request = AccountsBalanceGetRequest(
            access_token=current_user.plaid_access_token
        )
        response = await client.accounts_balance_get(request).to_dict()
        pretty_print_response(response['accounts'])
        return ResponseSchema(detail="Successfully received balance data", result={'balance': extract_data_from_balance(response['accounts'])})
    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)



@router.get("/networth-line-chart", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_networth_line(current_user: UserInDB = Depends(AuthService.get_current_user)):
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")

    try:
        # Iterate through each page of new transaction updates for item
        start_date = (dt.datetime.now() - dt.timedelta(days=(720))).date()
        end_date = dt.datetime.now().date()
        print(start_date, end_date)

        request = TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = await client.transactions_get(request).to_dict()

        # Return the 8 most recent transactions
        trans = extract_data_from_transactions(response['transactions'])
        formatted_networth_df = format_net_worth_by_day(trans)
        
        # pretty_print_response(df.to_json(orient='records'))
        return ResponseSchema(detail="Successfully received line chart data", result=prepare_networth_line_chart(formatted_networth_df))

    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)
    
@router.get("/spending-line-chart", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_spending_line(current_user: UserInDB = Depends(AuthService.get_current_user)):    
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")

    try:
        # Iterate through each page of new transaction updates for item
        start_date = (dt.datetime.now() - dt.timedelta(days=(720))).date()
        end_date = dt.datetime.now().date()
        print(start_date, end_date)

        request = TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = await client.transactions_get(request).to_dict()

        # Return the 8 most recent transactions
        trans = extract_data_from_transactions(response['transactions'])
        formatted_spending_df = format_spends_by_date(trans)
        return ResponseSchema(detail="Successfully received line chart data", result=prepare_spends_line_chart(formatted_spending_df))
    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)
    return

@router.get("/networth-column-chart", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_networth_column(current_user: UserInDB = Depends(AuthService.get_current_user)):
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")

    try:
        # Iterate through each page of new transaction updates for item
        start_date = (dt.datetime.now() - dt.timedelta(days=(720))).date()
        end_date = dt.datetime.now().date()
        print(start_date, end_date)

        request = TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = await client.transactions_get(request).to_dict()
            
        # Return the 8 most recent transactions
        trans = extract_data_from_transactions(response['transactions'])
        formatted_networth_df = format_net_worth_by_month(trans)
        
        # pretty_print_response(df.to_json(orient='records'))
        return ResponseSchema(detail="Successfully received column chart data", result=prepare_spends_column_chart(formatted_networth_df))

    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)
       
    
 

@router.get("/spends-polar-chart", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_spends_polar(current_user: UserInDB = Depends(AuthService.get_current_user)):
    if not current_user.plaid_access_token:
        raise HTTPException(status_code=404, detail="Plaid access token is null")

    try:
        # Iterate through each page of new transaction updates for item
        start_date = (dt.datetime.now() - dt.timedelta(days=(720))).date()
        end_date = dt.datetime.now().date()
        print(start_date, end_date)

        request = TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = await client.transactions_get(request).to_dict()
            
        # Return the 8 most recent transactions
        trans = extract_data_from_transactions(response['transactions'])
        formatted_spends_df = format_spends_by_name(trans)
        
        # pretty_print_response(df.to_json(orient='records'))
        return ResponseSchema(detail="Successfully received spends polar data", result=prepare_spends_polar_chart_by_name(formatted_spends_df))

    except plaid.ApiException as e:
        error_response = format_error(e)
        return JSONResponse(error_response)
       
       
    
    
    
def pretty_print_response(response):
    print(json.dumps(response, indent=2, sort_keys=True, default=str))
    
def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}
