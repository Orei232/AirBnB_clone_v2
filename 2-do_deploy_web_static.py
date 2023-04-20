#!/usr/bin/env python3

import os
from fabric.api import env, put, run

env.hosts = ["54.160.85.72", "35.175.132.106"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False

    # Get the name of the archive file without the extension
    filename = os.path.basename(archive_path)
    name = os.path.splitext(filename)[0]

    # Upload the archive to the server's /tmp directory
    put(archive_path, f"/tmp/{filename}")

    # Create the release directory and extract the archive
    run(f"mkdir -p /data/web_static/releases/{name}")
    run(f"tar -xzf /tmp/{filename} -C /data/web_static/releases/{name}")

    # Delete the archive from the server
    run(f"rm /tmp/{filename}")

    # Move the extracted files to the correct directory
    run(f"mv /data/web_static/releases/{name}/web_static/* "
        f"/data/web_static/releases/{name}/")

    # Delete the now-empty web_static directory
    run(f"rm -rf /data/web_static/releases/{name}/web_static")

    # Update the symbolic link to point to the new release directory
    run(f"rm -rf /data/web_static/current")
    run(f"ln -s /data/web_static/releases/{name}/ "
        f"/data/web_static/current")

    return True

