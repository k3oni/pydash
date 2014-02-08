import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from main.views import *
from pydash.settings import TIME_JS_REFRESH, TIME_JS_REFRESH_LONG, TIME_JS_REFRESH_NET

time_refresh = TIME_JS_REFRESH
time_refresh_long = TIME_JS_REFRESH_LONG
time_refresh_net = TIME_JS_REFRESH_NET

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
	
    data = json.dumps(up_time)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response

def getdisk(request):
    """
    Return the disk usage
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    
    try:
	getdisk = get_disk()
    except Exception:
	getdisk = None
	
    data = json.dumps(getdisk)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response
    
def getips(request):
    """
    Return the online users
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    
    try:
	get_ips = get_ipaddress()
    except Exception:
	get_ips = None
	
    data = json.dumps(get_ips['itfip'])
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
	
    data = json.dumps(online_users)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(data)
    return response
    
def getproc(request):
    """
    Return uptime
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    
    try:
	processes = get_cpu_usage()
	processes = processes['all']
    except Exception:
	processes = None
	
    data = json.dumps(processes)
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

    try:
        cpu_usage = get_cpu_usage()
        
    except Exception:
        cpu_usage = 0
    
    cpu = [
	    {   	    
        	"value": cpu_usage['free'],
        	"color": "#0AD11B"
    	    },
    	    {
    		"value": cpu_usage['used'],
            	"color": "#F7464A"
    	    }
	]

    data = json.dumps(cpu)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
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
    
    data = json.dumps(memory)
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
    
    data = json.dumps(load)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['load_average'] = datasets
    response.write(data)
    return response


def gettraffic(request):
    """
    Return the traffic for the interface
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    datasets_in = []
    datasets_in_i = []
    datasets_out = []
    datasets_out_o = []
    json_traffic = []
    cookie_traffic = {}

    try:
	intf = get_ipaddress()
	intf = intf['interface'][0]
	
        traffic = get_traffic(intf)
    except Exception:
        traffic = 0

    try:
        cookies = request._cookies['traffic']
    except Exception:
        cookies = None

    if not cookies:
        datasets_in.append(0)
        datasets_in_i.append(0)
        datasets_out.append(0)
        datasets_out_o.append(0)
    else:
        datasets = eval(cookies)
        datasets_in = datasets[0]
        datasets_out = datasets[1]
	datasets_in_i = datasets[2]
	datasets_out_o = datasets[3]

    if len(datasets_in) > 10:
        while datasets_in:
            del datasets_in[0]
            if len(datasets_in) == 10:
                break
    if len(datasets_in_i) > 2:
        while datasets_in_i:
            del datasets_in_i[0]
            if len(datasets_in_i) == 2:
                break
    if len(datasets_out) > 10:
        while datasets_out:
            del datasets_out[0]
            if len(datasets_out) == 10:
                break
    if len(datasets_out_o) > 2:
        while datasets_out_o:
            del datasets_out_o[0]
            if len(datasets_out_o) == 2:
                break

    if len(datasets_in_i) <= 1:
        datasets_in_i.append(float(traffic['traffic_in']))
    if len(datasets_in_i) == 2:
        datasets_in_i.append(float(traffic['traffic_in']))
        del datasets_in_i[0]
    if len(datasets_out_o) <= 1:
        datasets_out_o.append(float(traffic['traffic_out']))
    if len(datasets_out_o) == 2:
        datasets_out_o.append(float(traffic['traffic_out']))
        del datasets_out_o[0]

    if len(datasets_in) <= 9:
        datasets_in.append(float(((datasets_in_i[1] - datasets_in_i[0]) / 1024 ) / ( time_refresh_net / 1000 )))
    if len(datasets_in) == 10:
        datasets_in.append(float(((datasets_in_i[1] - datasets_in_i[0]) / 1024 ) / ( time_refresh_net / 1000 )))
        del datasets_in[0]
    if len(datasets_out) <= 9:
        datasets_out.append(float(((datasets_out_o[1] - datasets_out_o[0]) / 1024 ) / ( time_refresh_net / 1000 )))
    if len(datasets_out) == 10:
        datasets_out.append(float(((datasets_out_o[1] - datasets_out_o[0]) / 1024 ) / ( time_refresh_net / 1000 )))
        del datasets_out[0]


    # Some fix division by 0 Chart.js
    if len(datasets_in) == 10:
        if sum(datasets_in) == 0:
            datasets_in[9] += 0.1
        if sum(datasets_in) / 10 == datasets_in[0]:
            datasets_in[9] += 0.1

    traff = {
        'labels': ["KBps"] * 10,
        'datasets': [
            {
                "fillColor": "rgba(105,210,231,0.5)",
                "strokeColor": "rgba(105,210,231,1)",
                "pointColor": "rgba(105,210,231,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_in
            },
            {
                "fillColor": "rgba(227,48,81,0.5)",
                "strokeColor": "rgba(227,48,81,1)",
                "pointColor": "rgba(227,48,81,1)",
                "pointStrokeColor": "#fff",
                "data": datasets_out
            }
        ]
    }

    cookie_traffic = [datasets_in, datasets_out, datasets_in_i, datasets_out_o]
    data = json.dumps(traff)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.cookies['traffic'] = cookie_traffic
    response.write(data)
    return response

