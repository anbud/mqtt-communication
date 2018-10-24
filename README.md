# MQTT communication module

A simple module that stores selected events from Raspberry Pi IoT machines. It uses MQTT to communicate between Python scripts used for data collection and NodeJS scripts used for data storage on the blockchain.

It stores *important* events (`usb_inserted`, `usb_removed`) on the `shared` channel that's shared across all devices.
Less important events (`cpu_peak`, `memory_peak`, `cpu_regular`, `memory_regular`) are stored on the local (`agile`) channel.

## Chaincode
The chaincode used for data storage is available [here](https://github.com/anbud/chaincodes).
