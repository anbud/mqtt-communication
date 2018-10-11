import glib
import os
import sys
from pyudev import Context, Monitor
from pyudev.glib import GUDevMonitorObserver as MonitorObserver
import json
import ConfigParser
import paho.mqtt.client as mqtt
from time import sleep


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

def device_event(observer, device):
	if device.device_type=='usb_interface':
	    if device.action == 'add':
        	print('{} connected'.format(device))
                clnt.publish('usb_inserted', str(device))
            if device.action == 'remove':
                print('{} disconnected'.format(device))
                clnt.publish('usb_removed', str(device))

if __name__ == '__main__':
    	conf = init()
    	clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
	context = Context()
	monitor = Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	observer = MonitorObserver(monitor)
	observer.connect('device-added', device_event)
        observer.connect('device-removed', device_event)
	monitor.start()
	glib.MainLoop().run()

