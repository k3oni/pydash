import socket, platform, os

from datetime import timedelta

from django.core import serializers
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from pydash.settings import TIME_JS_REFRESH

time_refresh = TIME_JS_REFRESH

def index(request):
    """

    Index page.

    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/main')


def chunks(get, n):
    #for i in xrange(0, len(get), n):
	#yield l[i:i+n]
    return [get[i:i+n] for i in range(0, len(get), n)]

def get_uptime():
    """
    Get uptime
    """
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect('/login')

    try:            
	with open('/proc/uptime', 'r') as f:
    	    uptime_seconds = float(f.readline().split()[0])
    	    uptime_time = str(timedelta(seconds = uptime_seconds))
	    #return uptime_time
	    data = uptime_time.split('.', 1)[0]
    
    except Exception,err: 
	    data =  str(err)
	    
    #response = HttpResponse()
    #response['Content-Type'] = "text/javascript"
    #response.write(data)
    return data
    #print data
    #return render_to_response('main.html', {'getuptime': data, 'time_refresh': time_refresh}, context_instance=RequestContext(request))

def get_hostname():
    """
    Get the hostname
    """
    #if not request.user.is_authenticated():
    #    return HttpResponseRedirect('/login')
    
    try:
	data = socket.gethostname()
	
    except Exception,err: 
	    data =  str(err)
    
    #response = HttpResponse()
    #response['Content-Type'] = "text/javascript"
    #response.write(data)
    return data
    #return render_to_response('main.html', {'gethostname': data}, context_instance=RequestContext(request))

def get_ipaddress():
    """
    Get the IP Address
    """
    try:
	pipe = os.popen("/sbin/ifconfig |" + "grep -B1 'inet addr' |" + "awk '{ if ( $1 == \"inet\" ) { print $2 } else if ( $2 == \"Link\" ) { printf \"%s:\",$1 } }' |" + "awk -F: '{ print $1, $3 }'")
	data = pipe.read().strip().split()
	pipe.close()

	data = [n for n in data if not n.startswith(('lo', '127'))] 
	#x=len(data)
	    
	#data1 = list(range(x))
	
	#data = dict(zip(data1,data))
	#data = data1
	
	#data = chunks(data, 2)
	
	
	itf = dict(zip(*[iter(data)] * 2))
	ips = {'interface': itf, 'itfip': data}
	
	data = ips
	
    except Exception,err: 
	data =  str(err)
    
    return data
    
def get_traffic(request):
    """
    Get the traffic for the specified interface
    """
    try:
	pipe = os.popen("cat /proc/net/dev |" + "grep " + request +  "| awk {'print $1, $9'}")
	data = pipe.read().strip().split(':',1)[-1]
	pipe.close()

	#data = [n for n in data if not n.startswith(('lo'))] 
	data = data.split()
	
	traffic_in = int(data[0])
	traffic_out = int(data[1])
	
	#percent = (100 - ((freemem * 100) / allmem))
	#usage = (allmem - freemem)
	
	all_traffic = {'traffic_in': traffic_in, 'traffic_out': traffic_out}
	
	data = all_traffic
	
    except Exception,err: 
	data =  str(err)
    
    return data

def get_platform():
    """
    Get the OS name
    """
    try:
	data = " ".join(platform.linux_distribution())
	# + " " + platform.system() + " " + platform.release()
    
    except Exception,err: 
	data =  str(err)

    return data
    
def get_disk():
    """
    Get disk usage
    """
    try:
	#data = commands.getoutput("df -Ph | column -t")
	pipe = os.popen("df -Ph | " + "grep -v Filesystem | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
	data = pipe.read().strip().split()
	pipe.close()
	
	#x=len(data)
	    
	#data1 = list(range(x))
	
	#data = dict(zip(data1,data))
	#data = data1
	
	#data = chunks(data, 1)
	#data = simplejson.dumps(data)
	#data = serializers.serialize('json', data)
	
    except Exception,err: 
	data =  str(err)
    
    #eturn HttpResponse(data, mimetype="application/json")	
    return data

def get_mem():
    try:
	pipe = os.popen("free -tmo | " + "grep 'Mem' | " + "awk '{print $2,$4}'")
	data = pipe.read().strip().split()
	pipe.close()
	
	allmem = int(data[0])
	freemem = int(data[1])
	
	percent = (100 - ((freemem * 100) / allmem))
	usage = (allmem - freemem)
	
	mem_usage = {'usage': usage, 'percent': percent}
	
	data = mem_usage
	
    except Exception,err: 
	data =  str(err)
    
    return data

def get_load():
    try:
	data = os.getloadavg()[0]
    except Exception, err:
	data = str(err)

    return data
    
def getall(request):
    if not request.user.is_authenticated():
	return HttpResponseRedirect('/login')
	
	#getuptime = get_uptime()
	#global getuptime
	
	#gethostname = get_hostname(request)
	
    return render_to_response('main.html', {'getuptime': get_uptime(), 
					    'gethostname': get_hostname(),
					    'getplatform': get_platform(),
					    'getdisk': get_disk(),
					    'getip': get_ipaddress(),
					    #'gettraffic': get_traffic(),
					    'time_refresh': time_refresh
					    }, context_instance=RequestContext(request))
