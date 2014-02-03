from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import simplejson

from main.views import *
from pydash.settings import TIME_JS_REFRESH

time_refresh = TIME_JS_REFRESH

def uptime(request):
    """
    Return uptime
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    
    try:
	up_time = get_uptime()
    except Exception:
	up_time = None
	
    data = simplejson.dumps(up_time)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response
    
def getusers(request):
    """
    Return uptime
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    
    try:
	online_users = get_users()
    except Exception:
	online_users = None
	
    data = simplejson.dumps(online_users)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

def cpuusage(request):
    """
    Return CPU Usage in %
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    datasets = []

    try:
        cpu_usage = get_cpu_usage()
    except Exception:
        cpu_usage = 0

    try:
        cookies = request._cookies['cpu_usage']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = eval(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(int(cpu_usage['usage']))
    if len(datasets) == 10:
        datasets.append(int(cpu_usage['usage']))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    cpu = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(241,72,70,0.5)",
                "strokeColor": "rgba(241,72,70,1)",
                "pointColor": "rgba(241,72,70,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }

    data = simplejson.dumps(cpu)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['cpu_usage'] = datasets
    response.write(data)
    return response

def memusage(request):
    """
    Return Memory Usage in % and numeric
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
        
    datasets = []

    try:
        mem_usage = get_mem()
    except Exception:
        mem_usage = 0

    try:
        cookies = request._cookies['memory_usage']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = eval(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(int(mem_usage['usage']))
    if len(datasets) == 10:
        datasets.append(int(mem_usage['usage']))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    memory = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor": "rgba(249,134,33,0.5)",
                "strokeColor": "rgba(249,134,33,1)",
                "pointColor": "rgba(249,134,33,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }
    
    data = simplejson.dumps(memory)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['memory_usage'] = datasets
    response.write(data)
    return response
    
def loadaverage(request):
    """
    Return Load Average numeric
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
        
    datasets = []

    try:
        load_average = get_load()
    except Exception:
        load_average = 0

    try:
        cookies = request._cookies['load_average']
    except Exception:
        cookies = None

    if not cookies:
        datasets.append(0)
    else:
        datasets = eval(cookies)
    if len(datasets) > 10:
        while datasets:
            del datasets[0]
            if len(datasets) == 10:
                break
    if len(datasets) <= 9:
        datasets.append(int(load_average))
    if len(datasets) == 10:
        datasets.append(int(load_average))
        del datasets[0]

    # Some fix division by 0 Chart.js
    if len(datasets) == 10:
        if sum(datasets) == 0:
            datasets[9] += 0.1
        if sum(datasets) / 10 == datasets[0]:
            datasets[9] += 0.1

    load = {
        'labels': [""] * 10,
        'datasets': [
            {
                "fillColor" : "rgba(151,187,205,0.5)",
            	"strokeColor" : "rgba(151,187,205,1)",
        	"pointColor" : "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "data": datasets
            }
        ]
    }
    
    data = simplejson.dumps(load)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['load_average'] = datasets
    response.write(data)
    return response

