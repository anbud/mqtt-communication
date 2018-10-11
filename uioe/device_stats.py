import time
import psutil
import datetime
import json

def bytes_to_string(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def get_memstats():
    dict_help = {}
    nt = psutil.virtual_memory()
    for name in nt._fields:
        value = getattr(nt, name)
        dict_help[name.capitalize()] = float(value/1048576)
    mem_stats = json.dumps(dict_help,
                           sort_keys=True,
                           indent=4, separators=(',', ': '))
    return mem_stats

def get_netstats():
    tot = psutil.net_io_counters()
    net_stats = json.dumps({'Bytes_sent':tot.bytes_sent,
                            'Bytes_recv': tot.bytes_recv,
                            'Packets_sent': tot.packets_sent,
                            'Packets_recv' : tot.packets_recv},
                             sort_keys=True,
                             indent=4, separators=(',', ': '))
    return net_stats

def get_cpustats():
    cpus_percent = psutil.cpu_percent(percpu=True)
    i = 1
    dict_help = {}
    for percent in cpus_percent:
        key = "CPU-"+str(i)
        value = percent
        dict_help[key] =  value
        i+=1
    dict_help['Average'] = psutil.cpu_percent(percpu=False)
    cpu_stats = json.dumps(dict_help,
                           sort_keys=True,
                           indent=4, separators=(',', ':'))
    return cpu_stats
    
def get_procstats():
    # sleep some time
    time.sleep(3)
    procs = []
    procs_status = {}
    for p in psutil.process_iter():
        try:
            p.dict = p.as_dict(['username', 'nice', 'memory_info',
                                'memory_percent', 'cpu_percent',
                                'cpu_times', 'name', 'status'])
            try:
                procs_status[p.dict['status']] += 1
            except KeyError:
                procs_status[p.dict['status']] = 1
        except psutil.NoSuchProcess:
            pass
        else:
            if p.name() == 'python':
		procs.append(p)

    # return processes sorted by CPU percent usage
    processes = sorted(procs, key=lambda p: p.dict['cpu_percent'],
                       reverse=True)

    uptime  = datetime.datetime.now() - \
    datetime.datetime.fromtimestamp(psutil.boot_time())
    seconds_since = int(uptime.total_seconds())
    procs_status['Uptime'] = str(seconds_since)
    procs_status['Scripts_running'] = len(processes)
    proc_stats = json.dumps(procs_status, sort_keys=True,
                           indent=4, separators=(',', ':'))
    return proc_stats

def get_users():
	return psutil.users()



