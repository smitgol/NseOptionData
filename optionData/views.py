from django.shortcuts import render
from django.http import HttpResponse
from .optionApi import getNiftyData, getBankNiftyData
# Create your views here.

def index(request):
    nifty_market_data = getNiftyData()
    bank_market_data = getBankNiftyData()
    return render(request, 'index.html', {'nifty_market_data':nifty_market_data,'bank_market_data': bank_market_data})