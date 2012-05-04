from django.http import HttpResponse
from django.shortcuts import render_to_response
from commands import getoutput

def mainpage(request):
    if request.method == 'POST':
        search_output = getoutput('echo "' + request.POST.get('query', '') + '" | oberon search')
    else:
        search_output = ''
    return render_to_response('index.html', {'search_output': search_output})
