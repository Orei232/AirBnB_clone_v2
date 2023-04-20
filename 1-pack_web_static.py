#!/usr/bin/env python3

import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Create a tar gzipped archive of the directory web_static.
    """
    if not os.path.exists("versions"):
        os.mkdir("versions")
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive_path = f"versions/web_static_{now}.tgz"
    result = local(f"tar -czvf {archive_path} web_static")
    if result.failed:
        return None
    return archive_path

