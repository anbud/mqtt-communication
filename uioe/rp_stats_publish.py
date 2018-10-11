import json
import ConfigParser
import paho.mqtt.client as mqtt
from time import sleep
import requests
import device_stats as ds
import uuid

def onConnect(client, userdata, rc, self):
    """MQTT onConnect handler"""
    print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    client = mqtt.Client()
    client.on_connect = onConnect
    try:
        client.connect(url, port, keepalive)
        client.loop_start()
        return client
    except Exception, e:
        print(e)
        return None


def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    ret["url"]       = config.get('MQTT', 'url')
    ret["port"]      = int(config.get('MQTT', 'port'))
    ret["keepalive"] = int(config.get('MQTT', 'keepalive'))
    return ret

if __name__ == '__main__':
    conf = init()
    clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    while True:
            sleep(5)
	    cpu_stats = json.loads(ds.get_cpustats())
            mem_stats = json.loads(ds.get_memstats())
	    clnt.loop_start()
	    perc = (int(mem_stats['Used']) * 100) / int(mem_stats['Total'])
	    clnt.publish('cpu_regular', cpu_stats['Average'])
            clnt.publish('ram_regular', str(perc))
	    if (cpu_stats['Average']>70):
		print('cpu peak')
            	clnt.publish('cpu_peak', cpu_stats['Average'])
	    if (perc>50):
		print('mem peak')
		clnt.publish('memmory_peak', str(perc))
