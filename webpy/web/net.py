"""
Network Utilities
(from web.py)
"""

import datetime
import re
import socket
import time

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

__all__ = [
    "validipaddr",
    "validip6addr",
    "validipport",
    "validip",
    "validaddr",
    "urlquote",
    "httpdate",
    "parsehttpdate",
    "htmlquote",
    "htmlunquote",
    "websafe",
]


def validip6addr(address):
    """
    Returns True if `address` is a valid IPv6 address.
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except (socket.error, AttributeError, ValueError):
        return False

    return True


def validipaddr(address):
    """
    Returns True if `address` is a valid IPv4 address.
    """
    try:
        octets = address.split(".")
        if len(octets) != 4:
            return False

        for x in octets:
            if " " in x:
                return False

            if not (0 <= int(x) <= 255):
                return False
    except ValueError:
        return False
    return True


def validipport(port):
    """
    Returns True if `port` is a valid IPv4 port.
    """
    try:
        if not (0 <= int(port) <= 65535):
            return False
    except ValueError:
        return False
    return True


def validip(ip, defaultaddr="0.0.0.0", defaultport=8080):
    """
    Returns `(ip_address, port)` from string `ip_addr_port`.
    """
    addr = defaultaddr
    port = defaultport

    # Matt Boswell's code to check for IPv6 first
    match = re.search(r"^\[([^]]+)\](?::(\d+))?$", ip) # check for [ipv6]:port
    if match:
        if validip6addr(match.group(1)):
            if match.group(2):
                if validipport(match.group(2)):
                    return (match.group(1), int(match.group(2)))
            else:
                return (match.group(1), port)
    else:
        if validip6addr(ip):
            return (ip, port)
    # end ipv6 code

    ip = ip.split(":", 1)
    if len(ip) == 1:
        if not ip[0]:
            pass
        elif validipaddr(ip[0]):
            addr = ip[0]
        elif validipport(ip[0]):
            port = int(ip[0])
        else:
            raise ValueError(":".join(ip) + " is not a valid IP address/port")
    elif len(ip) == 2:
        addr, port = ip
        if not validipaddr(addr) or not validipport(port):
            raise ValueError(":".join(ip) + " is not valid IP address/port")
        port = int(port)
    else:
        raise ValueError(":".join(ip) + " is not a valid IP address/port")
    return (addr, port)


def validaddr(string_):
    """
    Returns either (ip_address, port) or "/path/to/socket" from string_.
    """
    if "/" in string_:
        return string_;
    else:
        return validip(string_)

def urlquote(val):
    """
    Quotes a string for use in a URL.
    """
    if val is None:
        return ""
    val = str(val).encode("utf-8")
    return quote(val)


def httpdate(date_obj):
    """
    Formats a datetime object for use in HTTP headers.
    """
    return date_obj.strftime("%a, %d %b %Y %H:%M:%S GMT")


def parsehttpdate(string_):
    """
    Parses an HTTP date into a datetime object.
    """
    try:
        t = time.strptime(string_, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return None
    return datetime.datetime(*t[:6])


def htmlquote(text):
    """
    Encodes `text` for raw use in HTML.
    """
    text = text.replace(u"&", u"&amp;") # Must be done first
    text = text.replace(u"<", u"&lt;")
    text = text.replace(u">", u"&gt;")
    text = text.replace(u"'", u"&#39;")
    text = text.replace(u'"', u"&quot;")
    return text


def htmlunquote(text):
    """
    Decodes `text` that's HTML quoted.
    """
    text = text.replace(u"&quot;", u'"')
    text = text.replace(u"&#39;", u"'")
    text = text.replace(u"&gt;", u">")
    text = text.replace(u"&lt;", u"<")
    text = text.replace(u"&amp;", u"&")  # Must be done last!
    return text


def websafe(val):
    """
    Converts `val` so that it is safe for use in Unicode HTML.
    """
    if val is None:
        return u""
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    elif not isinstance(val, str):
        val = str(val)
    return htmlquote(val)
