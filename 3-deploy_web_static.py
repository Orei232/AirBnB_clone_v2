#!/usr/bin/python3

import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["54.160.85.72", "35.175.132.106"]


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.

    Returns:
        (str): The path of the created archive on success, None on failure.
    """
    dt = datetime.utcnow()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, 
            dt.hour, dt.minute, dt.second)
    file_path = "versions/{}".format(file_name)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file_path)).failed is True:
        return None
    return file_path
def do_deploy(archive_path):
    """
    Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        (bool): True on success, False on failure.
    """
    if not os.path.isfile(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    name = file_name.split(".")[0]
    if put(archive_path, "/tmp/{}".format(file_name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed 
    is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format
            (file_name, name))
    .failed is True:
        return False
    if run("rm /tmp/{}".format(file_name)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* 
            /data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name))
    .failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ 
            /data/web_static/current".format(name)).failed is True:
        return False
    return True
def deploy():
    """
    Create and distribute an archive to a web server.
    Returns:
        (bool): True on success, False on failure.
    """
    file_path = do_pack()
    if file_path is None:
        return False
    return do_deploy(file_path)
