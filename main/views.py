import socket, platform, os, multiprocessing

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
    return [get[i:i+n] for i in range(0, len(get), n)]

def get_uptime():
    """
    Get uptime
    """
    try:            
	with open('/proc/uptime', 'r') as f:
    	    uptime_seconds = float(f.readline().split()[0])
    	    uptime_time = str(timedelta(seconds = uptime_seconds))
	    data = uptime_time.split('.', 1)[0]
    
    except Exception,err: 
	    data =  str(err)

    return data

def get_hostname():
    """
    Get the hostname
    """
    
    try:
	data = socket.gethostname()
	
    except Exception,err: 
	    data =  str(err)
    
    return data

def get_ipaddress():
    """
    Get the IP Address
    """
    try:
	pipe = os.popen("/sbin/ifconfig |" + "grep -B1 'inet addr' |" + "awk '{ if ( $1 == \"inet\" ) { print $2 } else if ( $2 == \"Link\" ) { printf \"%s:\",$1 } }' |" + "awk -F: '{ print $1, $3 }'")
	data = pipe.read().strip().split()
	pipe.close()

	data = [n for n in data if not n.startswith(('lo', '127'))] 
	
	itf = dict(zip(*[iter(data)] * 2))
	ips = {'interface': itf, 'itfip': data}
	
	data = ips
	
    except Exception,err: 
	data =  str(err)
    
    return data

def get_cpus():
    """
    Get the number of CPUs and model/type
    """
    try:
	pipe = os.popen("cat /proc/cpuinfo |" + "grep 'model name'")
	data = pipe.read().strip().split(':',2)[-1]
	pipe.close()
	
	cpus = multiprocessing.cpu_count()
	
	data = {'cpus': cpus, 'type': data}
	
    except Exception, err:
	data = str(err)
	
    return data
    
def get_users():
    """
    Get the current logged in users
    """
    try:
	pipe = os.popen("who |" + "awk '{print $1, $2, $6}'")
	data = pipe.read().strip().split()
	pipe.close()

    except Exception, err:
	data = str(err)
    
    return data
	
def get_traffic(request):
    """
    Get the traffic for the specified interface
    """
    try:
	pipe = os.popen("cat /proc/net/dev |" + "grep " + request +  "| awk {'print $1, $9'}")
	data = pipe.read().strip().split(':',1)[-1]
	pipe.close()

	data = data.split()
	
	traffic_in = int(data[0])
	traffic_out = int(data[1])
	
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
    
    except Exception,err: 
	data =  str(err)

    return data
    
def get_disk():
    """
    Get disk usage
    """
    try:
	pipe = os.popen("df -Ph | " + "grep -v Filesystem | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
	data = pipe.read().strip().split()
	pipe.close()
	
    except Exception,err: 
	data =  str(err)
    
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
    
def get_cpu_usage():
    try:
	pipe = os.popen("ps aux |" + "awk {'sum+=$3;print sum'} |" + "tail -n 1")
	data = pipe.read().strip()
	pipe.close()

	cpu_free = (100 - float(data))
	cpu_used = {'free': cpu_free, 'used': float(data)}
	data = cpu_used
	
    except Exception,err:
	data = str(err)

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
	
    return render_to_response('main.html', {'getuptime': get_uptime(), 
					    'gethostname': get_hostname(),
					    'getplatform': get_platform(),
					    'getcpus': get_cpus(),
					    'getdisk': get_disk(),
					    'getip': get_ipaddress(),
					    'getusers': get_users(),
					    'time_refresh': time_refresh
					    }, context_instance=RequestContext(request))
