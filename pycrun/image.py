import os
import shutil
import hashlib
import requests
from tempfile import NamedTemporaryFile
from tqdm import tqdm
from hashlib import sha256
from os.path import expanduser, join, exists, basename
from .utils import HumanSize
from .colorhelper import print_info, print_error, print_warn
from dateutil.parser import parse as parsedate
from datetime import datetime

CACHE_PATH = join(expanduser("~"), ".pycrun", "images_cache")


class Cache(object):
    cache_dir = CACHE_PATH

    """ Provides an image caching mechanism on disk """

    def __init__(self):
        if not exists(CACHE_PATH):
            os.makedirs(CACHE_PATH, 0o700)

    def get(self, cache_key, default=None):
        """return info for cached file"""
        cache_hash = sha256(cache_key.encode()).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)

        if exists(cache_fn):
            file_stat = os.stat(cache_fn)
            last_modified = datetime.fromtimestamp(file_stat.st_mtime)
            file_size = file_stat.st_size
            return cache_fn, cache_hash, last_modified, file_size

        return default

    def put(self, filename, cache_key):
        """put a file into cache"""
        cache_hash = sha256(cache_key.encode()).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)
        shutil.move(filename, cache_fn)
        return cache_hash, cache_fn


def download(image_url):
    """Download image (if not found in cache) and return it's filename"""

    response = requests.head(image_url)
    response.raise_for_status()
    file_size = remote_file_size = int(response.headers.get("Content-Length"))
    remote_last_modified = parsedate(response.headers.get("Last-Modified")).replace(
        tzinfo=None
    )
    remote_is_valid = response.status_code == 200 and file_size and remote_last_modified

    # Check if image is on cache
    cache = Cache()
    cached_image = cache.get(image_url)
    if cached_image:
        if remote_is_valid:
            cache_fn, cache_hash, last_modified, file_size = cached_image
            if remote_file_size == file_size and remote_last_modified < last_modified:
                print_info("Using file from cache", CACHE_PATH)
                return cache_hash, cache_fn
            print_info("Downloading new remote file because an update was found")
        else:
            print_warn("Unable to check the status for " + image_url)
            print_warn("Assuming local cache is valid")

    # Not cached, and no valid remote information was found
    if not remote_is_valid:
        print_error(
            "Unable to get file, http_code=%s, size=%s, last_modified=%s"
            % (response.status_code, remote_file_size, remote_last_modified)
        )
        exit(2)

    # Dowload image
    print_info(
        "Downloading image... ",
        "{0} [{1:.2S}]".format(basename(image_url), HumanSize(remote_file_size)),
    )
    remote_sha256 = hashlib.sha256()
    response = requests.get(image_url, stream=True)
    progress_bar = tqdm(total=remote_file_size, unit="iB", unit_scale=True)
    with NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in response.iter_content(chunk_size=1024):
            progress_bar.update(len(chunk))
            remote_sha256.update(chunk)
            tmp_file.write(chunk)
            tmp_file.flush()

    return cache.put(tmp_file.name, image_url)
