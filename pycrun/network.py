#
"""
https://pypi.org/project/pyroute2/
https://blogs.igalia.com/dpino/2016/04/10/network-namespaces/

# Share internet access between host and NS.

# Enable IP-forwarding.
echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -A FORWARD -o eth0 -i v0p0@if11 -j ACCEPT
iptables -A FORWARD -i eth0 -o v0p0@if11 -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.0.0.1/24 -o eth0 -j MASQUERADE
"""
from pyroute2 import IPRoute


def set_loopback():
    ip = IPRoute()
    idx = ip.link_lookup(ifname="lo")[0]
    ip.addr(
        "add", index=idx, address="127.0.0.1", broadcast="127.0.0.255", prefixlen=24
    )
    ip.link("set", index=idx, state="up")
    ip.close()


def set_host_veth(container_id):
    # create VETH pair and move v0p1 to netns 'test'
    ip = IPRoute()
    idx = ip.link_lookup(ifname="v0p0")
    if idx:
        ip.link("del", ifname="v0p0")
    ip.link("add", ifname="v0p0", peer="v0p1", kind="veth")
    idx = ip.link_lookup(ifname="v0p0")[0]
    ip.link("set", index=idx, state="up")
    ip.addr("add", index=idx, address="10.0.0.1", broadcast="10.0.0.255", prefixlen=24)
    idx = ip.link_lookup(ifname="v0p1")[0]
    ip.link("set", index=idx, net_ns_fd=container_id)
    ip.close()


def set_container_veth():
    ip = IPRoute()
    idx = ip.link_lookup(ifname="v0p1")[0]
    ip.link("set", index=idx, state="up")
    ip.addr("add", index=idx, address="10.0.0.2", broadcast="10.0.0.255", prefixlen=24)
    ip.route(
        "add", dst="default", gateway="10.0.0.1", metrics={"mtu": 1400, "hoplimit": 16}
    )
    ip.close()
