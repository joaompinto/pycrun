from ..colorhelper import print_info, print_error, print_success
from typing import Optional
import typer
from pycrun import container
from ..image import download, sha256
from ..image_index import get_url
from ..tar import extract_layer
from metadict import MetaDict
from pathlib import Path
import shutil
import os

def run(
    image_url,
    command: Optional[str] = typer.Argument(None),
    container_options: Optional[str] = typer.Argument({}),
):
    url = get_url(image_url)
    image_url = url or image_url
    if not image_url:
        print_info("No index was found for image", image_url)
        exit(5)
    is_validate_only = False
    if not command:
        command = ["/bin/sh"]
    else:
        command = [command]
    image_protocol = image_url.split(":")[0].lower()
    if image_protocol in ["http", "https"]:
        _, image_fn = download(image_url)
    else:
        _, image_fn = sha256(image_url).hexdigest(), image_url
    rootfs = extract_layer(image_fn)
    if len(command) == 1 and command[0] == "-":
        is_validate_only = True
        print("Validating container setup with the rootfs")
    else:
        print_info("Executing", command[0])
    _, exit_code = container.runc(rootfs, command, container_options)
    if exit_code != 0:
        print_error("Last command returned an error")
    elif is_validate_only:
        print_success("OK")
