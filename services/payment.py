# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.conf import settings
# from burger.models import Gateway
def send_request(request,branch_id,request_data):
    client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

    # try:
    #     gateway = Gateway.objects.get(branch__id = branch_id)
    # except:
    #     return "id_not_found"
    # MERCHANT = 
    MERCHANT = settings.ZARINPAL_MERCHANT
    CallbackURL ="http://"+ request.domain.domain+'/payment/verify/'  # Important: need to edit for realy server.
    print(CallbackURL)
    # result = client.service.PaymentRequest(MERCHANT, request_data["amount"], request_data["description"], request_data["email"], request_data["mobile"], CallbackURL)
    result = client.service.PaymentRequest(MERCHANT, request_data["amount"], request_data["description"],'root@root.com','09132222222' ,CallbackURL)
    if result.Status == 100:
        return ("success" , 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority),result.Authority)
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return ("failed", result.Status,'0')
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request,branch_id,amount):
    # try:
    #     gateway = Gateway.objects.get(branch__id=branch_id)
    # except:
    #     return "id_not_found"
    MERCHANT = settings.ZARINPAL_MERCHANT
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return ("success",result.RefID)
        elif result.Status == 101:
            return ("submitted", result.Status)
        else:
            return ("failed", result.Status)

    else:
        return ("cancel", 0)