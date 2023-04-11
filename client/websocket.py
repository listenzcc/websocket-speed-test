'''
Websocket client example of short connection
'''

# %%
import time
import logging
import asyncio
import websockets
import multiprocessing

import numpy as np
import pandas as pd

# %%


DEFAULT_LOGGING_KWARGS = dict(
    name='websocket',
    filepath='websocket.log',
    level_file=logging.DEBUG,
    level_console=logging.DEBUG,
    format_file='%(asctime)s %(name)s %(levelname)-8s %(message)-40s {{%(filename)s:%(lineno)s:%(module)s:%(funcName)s}}',
    format_console='%(asctime)s %(name)s %(levelname)-8s %(message)-40s {{%(filename)s:%(lineno)s}}'
)


def GENERATE_LOGGER(name, filepath, level_file, level_console, format_file, format_console):
    '''
    Generate logger from inputs,
    the logger prints message both on the console and into the logging file.
    The DEFAULT_LOGGING_KWARGS is provided to automatically startup

    Args:
        :param:name: The name of the logger
        :param:filepath: The logging filepath
        :param:level_file: The level of logging into the file
        :param:level_console: The level of logging on the console
        :param:format_file: The format when logging on the console
        :param:format_console: The format when logging into the file
    '''

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(logging.Formatter(format_file))
    file_handler.setLevel(level_file)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(format_console))
    console_handler.setLevel(level_console)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = GENERATE_LOGGER(**DEFAULT_LOGGING_KWARGS)

# %%


async def short_connect(url, msg='', idx=0):
    '''
    Send msg to url and close the connection

    Args:
        :param: url: The url of the websocket connection
        :param: msg: The message to be sent, if it is empty, it waits for console input, default is ''
    '''

    async with websockets.connect(url) as websocket:

        if not msg:
            msg = input("Send message to {}\n>> ".format(url))

        print(f"< {len(msg)}, {msg[:8]}")

        t = time.time()
        await websocket.send(msg)
        t1 = time.time()
        response = await websocket.recv()
        t2 = time.time()

        print(f"< {response}")

        print(f'Web socket costs {t2 - t} seconds')
        time_costs = dict(
            time=t,
            send=t1-t,
            recv=t2-t1,
            total=t2-t,
            idx=idx
        )

        logger.debug(time_costs)


# %%
if __name__ == '__main__':
    host = 'localhost'
    port = 7788
    path = ''
    msg = np.random.randint(0, 255, (800, 600)).astype(np.uint8).tobytes()

    url = 'ws://{}:{}/{}'.format(host, port, path)

    for idx in range(1000):
        def target(url, msg, idx):
            asyncio.get_event_loop().run_until_complete(short_connect(url, msg, idx))

        target(url, msg, idx)

        # p = multiprocessing.Process(
        #     target=target, args=(url, msg, idx), daemon=True)
        # p.start()

    input('Enter to leave')

# %%
