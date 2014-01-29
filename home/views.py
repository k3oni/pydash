from main.views import *

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.datastructures import SortedDict

def index(request):
    """

    Index page.

    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/home')

    