#!/usr/bin/python3
# Fabfile to delete out-of-date archives.

import os
from fabric import Connection

env = {
    'hosts': ["54.160.85.72", "35.175.132.106"]
}

def do_clean(number=1):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep. If number is 0 or 1,
            keeps only the most recent archive. If number is 2, keeps the most
            and second-most recent archives, etc.
    """
    number = max(1, int(number))
    with Connection(env.hosts[0]) as conn:
        archives = conn.run("ls -t /data/web_static/releases/").stdout.split()
        archives = [a for a in archives if "web_static_" in a]
        [conn.run("rm -rf /data/web_static/releases/{}".format(a)) for a in archives[number:]]

    with Connection(env.hosts[0]) as conn:
        archives = sorted(os.listdir("versions"))
        [os.remove(os.path.join("versions", a)) for a in archives[number:]]



