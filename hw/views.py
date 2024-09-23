from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def main(request):
    '''A function to respod to the /hw url'''

    response_text = '''
    Hello World 
    '''
    template_name = "hw/home.html"

    return HttpResponse(response_text)
