const mqtt = require('mqtt')
const client  = mqtt.connect('mqtt://localhost:1883')
const spawn = require('child_process').exec
const got = require('got')

const sensorId = 2

const events = ['usb_inserted', 'usb_removed', 'cpu_peak', 'memmory_peak', 'cpu_regular', 'memmory_regular']

client.on('connect', function () {
    console.log('[INFO] Connected')
    events.forEach(i => client.subscribe(i))
})

got('users', {
    baseUrl: 'http://localhost:4000',
    headers: {
        'content-type': 'application/x-www-form-urlencoded'
    },
    body: {
        username: 'AndrejVLF',
        orgName: 'agileiot'
    },
    form: true
}).then(data => {
    data.body = JSON.parse(data.body)
    
    client.on('message', function (topic, message) {
	    console.log(`[INFO] Message arrived, ${topic}, ${message}`)
	    let payload = {
	        event: topic,
		    message: message.toString()
	    }

        if (!~['usb_inserted', 'usb_removed'].indexOf(topic)) {
      	    got('channels/shared/chaincodes/sensorscc', {
                baseUrl: 'http://localhost:4000',
                headers: {
                    'authorization': `Bearer ${data.body.token}`,
                    'content-type': 'application/json'
                },
                body: JSON.stringify({
                    peers: ['peer0.test.vlf.zx.rs'],
                    fcn: 'changeSensorValue',
                    args: [`Sensor${sensorId}`, JSON.stringify(payload)]
                })
            }).then(data => console.log(`[SHARED] Write - ${JSON.stringify(payload)}`))
        } else {
            got('channels/agile/chaincodes/sensorscc', {
                baseUrl: 'http://localhost:4000',
                headers: {
                    'authorization': `Bearer ${data.body.token}`,
                    'content-type': 'application/json'
                },
                body: JSON.stringify({
                    peers: ['peer0.test.vlf.zx.rs'],
                    fcn: 'changeSensorValue',
                    args: [`Sensor${sensorId}`, JSON.stringify(payload)]
                })
            }).then(data => console.log(`[AGILE] Write - ${JSON.stringify(payload)}`))
        }
})
