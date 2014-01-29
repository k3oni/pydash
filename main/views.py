from datetime import timedelta

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson

def getuptime():
    """
    Get uptime
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    try:            
	with open('/proc/uptime', 'r') as f:
    	    uptime_seconds = float(f.readline().split()[0])
    	    uptime_time = str(timedelta(seconds = uptime_seconds))
	    data = simplejson.dumps(uptime_time)
    
    except Exception,err: 
	    data = simplejson.dumps(str(err))

    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response
    
