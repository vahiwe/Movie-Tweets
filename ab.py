import requests

def valBVN(bvnNumber):
    bvnNumber= str(bvnNumber)
    tokenKey= 'FLWSECK-af1ff421c70907112ba55815f89710ea-X'
    api= 'https://ravesandboxapi.flutterwave.com/v2/kyc/bvn/'+ bvnNumber+'?seckey='+ tokenKey

    r= requests.get(api)

    print(r.json())

valBVN(22354525949)