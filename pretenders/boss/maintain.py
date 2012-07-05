import os
import time

from pretenders.boss.client import BossClient

STALE_DELETE_FREQUENCY = 5


def run(host, port):
    """
    Run the maintainer.

    Which regularly triggers the boss to delete stale Mock servers.
    """
    boss_client = BossClient(host, port)
    while True:
        time.sleep(STALE_DELETE_FREQUENCY)
        boss_client.boss_access.http('DELETE', url='/mock_server?stale=1')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Start the server')
    parser.add_argument('-H', '--host', dest='host', default='localhost',
                help='host/IP to run the server on (default: localhost)')
    parser.add_argument('-p', '--port', dest='port', type=int, default=8000,
                help='port number to run the server on (default: 8000)')

    args = parser.parse_args()
    pid = os.getpid()
    with open('maintain-boss.pid', 'w') as f:
        f.write(str(pid))
    # bottle.debug(True)
    run(args.host, args.port)
