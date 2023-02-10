# ThingSet Serial to WebSocket

This is a simple script to forward ThingSet statements received on a serial interface to the cloud via WebSockets.

See https://thingset.io for the ThingSet protocol specification.

## Usage

Print published data from ThingSet node connected at the serial port `/dev/ttyACM0`:

```
./thingset-serial2websocket.py -s /dev/ttyACM0
```

For forwarding data to the cloud, the websocket server URL and an authorization token have to be specified. The authorization token is usually specific for one device (i.e. ThingSet node ID). The node ID of the connected device is printed after start of the script.

Here is an example:

```
./thingset-serial2websocket.py -s /dev/ttyACM0 -w wss://cloud.yourserver.io -a THISISYOURTOKEN1234
```

## License

This software is released under the [Apache-2.0 License](LICENSE).
