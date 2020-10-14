from .models import EmailVerifyToken
import random
from string import ascii_letters, digits
from bs4 import BeautifulSoup
import requests

def sendEmail(user):
    print (user.__dict__)
    token = ''.join([random.choice(digits+ascii_letters) for _ in range(150)])    
    token_obj = EmailVerifyToken(token = token, user = user) 
    token_obj.save()
    link = "https://sablekh.com/verify-email/"+token
    file = open("email_verify.html") 
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    soup.select("#token_link")[0]["href"] = link 
    response = requests.post(
        "https://api.mailgun.net/v3/sablekh.com/messages",
        auth=("api", "f746c538cfc2aa48e43c3ae39bddb827-f7d0b107-ca20f738"),
        data={"from": "Sablekh <noreply@sablekh.com>",
              "to": [user.email],
              "subject": "Sablekh Verify Email",
              "text": "Hi, {} please click on the link below to verify email".format(user.username),
              "html": str(soup)})


