#!/bin/python
#
# Copyright (c) The Libre Solar Project Contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# This is a simple script to forward ThingSet statements received on a serial interface to the
# cloud via WebSockets.
#
# See https://thingset.io for the ThingSet protocol specification.

import argparse
import asyncio
import json
import re
import serial
import websockets

parser = argparse.ArgumentParser(description="ThingSet Serial Forwarder")
parser.add_argument("-s", "--serial", default="/dev/ttyACM0", help="Serial interface")
parser.add_argument("-w", "--websocket", help="WebSocket server")
parser.add_argument("-a", "--auth", help="Authorization token for the server")
args = parser.parse_args()

async def forwarder():
    ser = serial.Serial(args.serial, 115200, timeout=10, write_timeout=3)
    node_id = None

    # Find out node ID
    for attempt in range(1, 10):
        ser.write(b"?cNodeID\n")
        raw_data = ser.readline().decode("utf-8").strip()
        response = re.match(r"^:85[^.]*. \"*(.*)\"$", raw_data)
        if response:
            node_id = response.group(1)
            print(f"Connected to ThingSet node with ID {node_id}")
            break

    if not node_id:
        print("Could not determine node ID. Is the device connected?")
        ser.close()
        exit(1)

    # Start websocket connection
    websocket = None
    if args.websocket:
        try:
            websocket = await websockets.connect(
                args.websocket + "/node/" + node_id,
                extra_headers={"Authorization": f"Bearer {args.auth}"}
            )
        except Exception as e:
            print("Websocket connection failed. Only printing serial data.")
            print(e)
            pass
    else:
        print("No websocket connection configured. Only printing serial data.")

    while True:
        try:
            # Forward published ThingSet statements to server
            raw_data = ser.readline().decode("utf-8").strip()
            if len(raw_data) > 1 and raw_data[0] == '#':
                print(raw_data)
                if websocket:
                    await websocket.send(raw_data)
        except Exception as e:
            print(e)
            pass

try:
    asyncio.run(forwarder())
except KeyboardInterrupt:
    pass
