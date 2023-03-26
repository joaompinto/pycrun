URL_MAP = {
    "alpine": "https://dl-cdn.alpinelinux.org/alpine/v3.17/releases/x86_64/alpine-minirootfs-3.17.2-x86_64.tar.gz",
    "ubuntu": "https://cloud-images.ubuntu.com/releases/22.10/release/ubuntu-22.10-server-cloudimg-amd64-root.tar.xz",
    "voidlinux": "https://repo-default.voidlinux.org/live/current/void-x86_64-ROOTFS-20221001.tar.xz"
}


def get_url(key):
    return URL_MAP.get(key)
