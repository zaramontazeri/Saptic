import requests


def send_sms_pattern(patternName , mobileNumber,token):
    api_key = "903098f0-36df-4068-b87d-d96754e16bc5"
    print(patternName)
    resoponse = requests.post("https://api.smass.ir/fa/service/pattern/send/",{
        "api_key":api_key,
        "template":patternName,
        "recipient":str(mobileNumber),
        "token1":str(token)
    })

    print (resoponse.json())
    return True


