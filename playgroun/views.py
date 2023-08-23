from django.core import mail
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


# Create your views here.

# def playground(request):
#     message = "this mail is sent from django"
#     mail = EmailMessage("Welcome",message, "support@library.com",
#               ['cashmoney@gmail.com'],)
#
#     mail.attach_file("playgroun\static\images\TodoHomepagePic.jpg")
#     mail.send()
#     return HttpResponse("This is a playground")

def playground(request):
    message = BaseEmailMessage(template_name='email\email.html', context={'name': 'Gudnez'})
    message.send(['goodness@gmail.com'])
    return HttpResponse("This is a playground")
