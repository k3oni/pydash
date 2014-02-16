#The MIT License (MIT)
#
#Copyright (c) 2014 Florian Neagu - michaelneagu@gmail.com - https://github.com/k3oni/
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import platform, os, multiprocessing, json

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from pydash.settings import TIME_JS_REFRESH, TIME_JS_REFRESH_LONG, TIME_JS_REFRESH_NET, VERSION

time_refresh = TIME_JS_REFRESH
time_refresh_long = TIME_JS_REFRESH_LONG
time_refresh_net = TIME_JS_REFRESH_NET
version = VERSION

@login_required(login_url='/login/')
def index(request):
    """

    Index page.

    """
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


def get_ipaddress():
    """
    Get the IP Address
    """
    try:
	pipe = os.popen(" ip addr | grep -A3 'state UP' | awk '{printf \"%s,\",$2}'|awk -F, '{print $1, $2, $3}'")
	data = pipe.read().strip().split('\n')
	pipe.close()

	data = [i.split(None, 3) for i in data]
	for e in data:
	    if len(e) > 3:
		itf = dict(zip([iter(e[0].strip(':'))]))
	    else:
		itf = [e[0].strip(':')]
		
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
	data = pipe.read().strip().split(':')[-1]
	pipe.close()

	if not data:
	    pipe = os.popen("cat /proc/cpuinfo |" + "grep 'Processor'")
	    data = pipe.read().strip().split(':')[-1]
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
	data = pipe.read().strip().split('\n')
	pipe.close()
	
	data = [i.split(None, 3) for i in data]

    except Exception, err:
	data = str(err)
    
    if data[0] == []:
	data = [['No', 'data', 'available']]
    
    return data
	
def get_traffic(request):
    """
    Get the traffic for the specified interface
    """
    try:
	pipe = os.popen("cat /proc/net/dev |" + "grep " + request +  "| awk '{print $1, $9}'")
	data = pipe.read().strip().split(':',1)[-1]
	pipe.close()

	if data == ' 0':
	    pipe = os.popen("cat /proc/net/dev |" + "grep " + request +  "| awk '{print $2, $10}'")
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
    Get the OS name, hostname and kernel
    """
    try:
	osname = " ".join(platform.linux_distribution())
	uname = platform.uname()
	
	data = {'osname': osname, 'hostname': uname[1], 'kernel': uname[2] }
    
    except Exception,err: 
	data =  str(err)

    return data
    
def get_disk():
    """
    Get disk usage
    """
    try:
	pipe = os.popen("df -Ph | " + "grep -v Filesystem | " + "awk '{print $1, $2, $3, $4, $5, $6}'")
	data = pipe.read().strip().split('\n')
	pipe.close()
	
	data = [i.split(None, 6) for i in data]

    except Exception,err: 
	data =  str(err)
    
    return data

def get_disk_rw():
    """
    Get the disk reads and writes
    """
    try:
	pipe = os.popen("cat /proc/partitions | grep -v 'major' | awk '{print $4}'")
	data = pipe.read().strip().split('\n')
	pipe.close()
	
	rws = []
	for i in data:
	    if i.isalpha():
		pipe = os.popen("cat /proc/diskstats | grep -w '" + i + "'|awk '{print $4, $8}'")
		rw = pipe.read().strip().split()
		pipe.close()
		
		rws.append([i, rw[0], rw[1]])
		
	if not rws:
	    pipe = os.popen("cat /proc/diskstats | grep -w '" + data[0] + "'|awk '{print $4, $8}'")
	    rw = pipe.read().strip().split()
	    pipe.close()
		
	    rws.append([data[0], rw[0], rw[1]])
	
	data = rws
	    
    except Exception,err: 
	data =  str(err)
    
    return data

def get_mem():
    """
    Get memory usage
    """
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
    """
    Get the CPU usage and running processes
    """
    try:
	pipe = os.popen("ps aux --sort -%cpu,-rss")
	data = pipe.read().strip().split('\n')
	pipe.close()
	
	usage = [i.split(None, 10) for i in data]
	del usage[0]
	
	total_usage = []
	
	for element in usage:
	    usage_cpu = element[2]
	    total_usage.append(usage_cpu)
	
	total_usage = sum(float(i) for i in total_usage)
	
	total_free = ((100 * int(get_cpus()['cpus'])) - float(total_usage))
	
	cpu_used = {'free': total_free, 'used': float(total_usage), 'all': usage}
	
	data = cpu_used
	
    except Exception,err:
	data = str(err)

    return data

def get_load():
    """
    Get load average
    """
    try:
	data = os.getloadavg()[0]
    except Exception, err:
	data = str(err)

    return data
    
@login_required(login_url='/login/')
def getall(request):
	
    return render_to_response('main.html', {'gethostname': get_platform()['hostname'],
					    'getplatform': get_platform()['osname'],
					    'getkernel': get_platform()['kernel'],
					    'getcpus': get_cpus(),
					    'time_refresh': time_refresh,
					    'time_refresh_long': time_refresh_long,
					    'time_refresh_net': time_refresh_net,
					    'version': version
					    }, context_instance=RequestContext(request))
