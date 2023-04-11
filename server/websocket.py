'''
Websocket server example for short connections
'''

import asyncio
import websockets
import multiprocessing

import numpy as np


def deal_msg(msg):
    mat = np.frombuffer(msg, dtype=np.uint8)
    shape = mat.shape
    max = np.max(mat)
    min = np.min(mat)
    mean = np.mean(mat)
    median = np.median(mat)

    response = f"Received: {len(msg)}, {shape}, {max}, {min}, {mean}, {median}"

    print(f"> {response}")
    return


async def handle(websocket, path):
    '''
    Handle message from the client

    Args:
        :param:websocket: The websocket connection
        :param:path: The path of the client connection
    '''
    print('Client connects', websocket, path)

    msg = await websocket.recv()
    print(f"< {len(msg)}, {msg[:8]}")

    p = multiprocessing.Process(target=deal_msg, args=(msg,))
    p.start()

    response = f'Received: {len(msg)}'

    # mat = np.frombuffer(msg, dtype=np.uint8)
    # shape = mat.shape
    # max = np.max(mat)
    # min = np.min(mat)
    # mean = np.mean(mat)
    # median = np.median(mat)

    # response = f"Received: {len(msg)}, {shape}, {max}, {min}, {mean}, {median}"

    await websocket.send(response)
    print(f"> {response}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help="host of the websocket connection", default='localhost')
    parser.add_argument(
        "--port", help="port of the websocket connection", default=7788)
    args = parser.parse_args()

    host = args.host
    port = args.port

    start_server = websockets.serve(handle, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
