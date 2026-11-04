#!/usr/bin/env python3
"""Read-only ONVIF probe run on the ROCK. Prints a redacted JSON summary.

Only Get* requests are sent. No camera setting is changed, nothing is recorded.
Hosts, credentials and stream URIs are never printed.
"""
import base64, datetime, hashlib, json, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

SRC = json.load(open(os.path.expanduser('~/sd5531/private/camera_source.json')))
u = urllib.parse.urlsplit(SRC['uri'])
HOST = u.hostname
USER = urllib.parse.unquote(u.username or '')
PASS = urllib.parse.unquote(u.password or '')
ONVIF_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 80
DEVICE = f'http://{HOST}:{ONVIF_PORT}/onvif/device_service'

NS = {'s': 'http://www.w3.org/2003/05/soap-envelope',
      'tds': 'http://www.onvif.org/ver10/device/wsdl',
      'trt': 'http://www.onvif.org/ver10/media/wsdl',
      'tt': 'http://www.onvif.org/ver10/schema',
      'tev': 'http://www.onvif.org/ver10/events/wsdl',
      'wsnt': 'http://docs.oasis-open.org/wsn/b-2',
      'wstop': 'http://docs.oasis-open.org/wsn/t-1'}


def security_header():
    if not USER:
        return ''
    nonce = os.urandom(16)
    created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    digest = base64.b64encode(hashlib.sha1(nonce + created.encode() + PASS.encode()).digest()).decode()
    return ('<s:Header><Security s:mustUnderstand="1" xmlns="http://docs.oasis-open.org/wss/2004/01/'
            'oasis-200401-wss-wssecurity-secext-1.0.xsd"><UsernameToken>'
            f'<Username>{USER}</Username>'
            '<Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">'
            f'{digest}</Password><Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/'
            f'oasis-200401-wss-soap-message-security-1.0#Base64Binary">{base64.b64encode(nonce).decode()}</Nonce>'
            '<Created xmlns="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">'
            f'{created}</Created></UsernameToken></Security></s:Header>')


def call(url, body, auth=True):
    env = ('<?xml version="1.0" encoding="UTF-8"?><s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" '
           'xmlns:tds="http://www.onvif.org/ver10/device/wsdl" xmlns:trt="http://www.onvif.org/ver10/media/wsdl" '
           'xmlns:tt="http://www.onvif.org/ver10/schema" xmlns:tev="http://www.onvif.org/ver10/events/wsdl">'
           f'{security_header() if auth else ""}<s:Body>{body}</s:Body></s:Envelope>')
    req = urllib.request.Request(url, env.encode(), {'Content-Type': 'application/soap+xml; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, ET.fromstring(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, ET.fromstring(e.read())
        except Exception:
            return e.code, None
    except Exception as e:
        return type(e).__name__, None


def fault(root):
    if root is None:
        return None
    f = root.find('.//s:Fault', NS)
    return None if f is None else ' '.join(t.strip() for t in f.itertext() if t.strip())[:160]


def local(tag):
    return tag.split('}')[-1]


def redact_path(url):
    """Keep only the service path shape, never host/userinfo/query."""
    return urllib.parse.urlsplit(url).path


out = {'read_only': True, 'requests': 'Get* only'}

st, r = call(DEVICE, '<tds:GetSystemDateAndTime/>', auth=False)
if r is not None:
    d = r.find('.//tt:UTCDateTime', NS)
    if d is not None:
        vals = {local(e.tag): e.text for e in d.iter() if e.text and e.text.strip()}
        out['camera_utc'] = '{Year}-{Month:0>2}-{Day:0>2}T{Hour:0>2}:{Minute:0>2}:{Second:0>2}Z'.format(**vals)
    dt = r.find('.//tt:DateTimeType', NS)
    out['camera_time_source'] = dt.text if dt is not None else None
    ntp = r.find('.//tt:DaylightSavings', NS)
out['board_utc'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

st, r = call(DEVICE, '<tds:GetDeviceInformation/>')
out['device_information_status'] = st
if r is not None and fault(r) is None:
    info = r.find('.//tds:GetDeviceInformationResponse', NS)
    out['device_information'] = {local(e.tag): e.text for e in info} if info is not None else None
    out['device_information'].pop('SerialNumber', None)
else:
    out['device_information_fault'] = fault(r)

st, r = call(DEVICE, '<tds:GetServices><tds:IncludeCapability>false</tds:IncludeCapability></tds:GetServices>')
services = {}
if r is not None:
    for s in r.findall('.//tds:Service', NS):
        ns = s.findtext('tds:Namespace', namespaces=NS)
        xa = s.findtext('tds:XAddr', namespaces=NS)
        services[ns] = xa
out['services'] = {ns: redact_path(x) for ns, x in services.items()}
out['services_fault'] = fault(r)

st, r = call(DEVICE, '<tds:GetCapabilities><tds:Category>All</tds:Category></tds:GetCapabilities>')
caps = {}
if r is not None:
    c = r.find('.//tds:Capabilities', NS)
    if c is not None:
        for child in c:
            caps[local(child.tag)] = True
        ext = c.find('tt:Extension', NS)
        if ext is not None:
            caps['Extension'] = [local(e.tag) for e in ext]
        ev = c.find('tt:Events', NS)
        if ev is not None:
            caps['Events_detail'] = {local(e.tag): e.text for e in ev if local(e.tag) != 'XAddr'}
        media = c.find('tt:Media/tt:StreamingCapabilities', NS)
        if media is not None:
            caps['Media_streaming'] = {local(e.tag): e.text for e in media}
out['capabilities'] = caps

media_url = services.get('http://www.onvif.org/ver10/media/wsdl') or DEVICE.replace('device_service', 'Media')
st, r = call(media_url, '<trt:GetProfiles/>')
profiles = []
if r is not None:
    for p in r.findall('.//trt:Profiles', NS):
        enc = p.find('tt:VideoEncoderConfiguration', NS)
        prof = {'token': p.get('token'), 'name': p.findtext('tt:Name', namespaces=NS)}
        if enc is not None:
            prof['encoding'] = enc.findtext('tt:Encoding', namespaces=NS)
            prof['width'] = enc.findtext('tt:Resolution/tt:Width', namespaces=NS)
            prof['height'] = enc.findtext('tt:Resolution/tt:Height', namespaces=NS)
            prof['fps_limit'] = enc.findtext('tt:RateControl/tt:FrameRateLimit', namespaces=NS)
            prof['bitrate_kbps'] = enc.findtext('tt:RateControl/tt:BitrateLimit', namespaces=NS)
            prof['gov_length'] = enc.findtext('tt:H264/tt:GovLength', namespaces=NS)
            prof['h264_profile'] = enc.findtext('tt:H264/tt:H264Profile', namespaces=NS)
        profiles.append(prof)
out['profiles'] = profiles
out['profiles_fault'] = fault(r)

uris = {}
for p in profiles:
    body = ('<trt:GetStreamUri><trt:StreamSetup><tt:Stream>RTP-Unicast</tt:Stream><tt:Transport>'
            '<tt:Protocol>RTSP</tt:Protocol></tt:Transport></trt:StreamSetup>'
            f'<trt:ProfileToken>{p["token"]}</trt:ProfileToken></trt:GetStreamUri>')
    st, r = call(media_url, body)
    if r is not None and fault(r) is None:
        uri = r.findtext('.//tt:Uri', namespaces=NS)
        if uri:
            uris[p['token']] = uri
    p['stream_uri_available'] = p['token'] in uris

ev_url = services.get('http://www.onvif.org/ver10/events/wsdl')
out['events_service'] = bool(ev_url)
if ev_url:
    st, r = call(ev_url, '<tev:GetEventProperties/>')
    out['event_properties_fault'] = fault(r)
    topics = []
    if r is not None:
        ts = r.find('.//wstop:TopicSet', NS)
        if ts is not None:
            def walk(node, path):
                for ch in node:
                    name = local(ch.tag)
                    if name in ('MessageDescription',):
                        topics.append(path)
                        continue
                    walk(ch, path + '/' + name)
            walk(ts, '')
    out['event_topics'] = sorted(set(topics))
    st, r = call(ev_url, '<tev:GetServiceCapabilities/>')
    capel = r.find('.//tev:Capabilities', NS) if r is not None else None
    out['event_service_capabilities'] = dict(capel.attrib) if capel is not None else fault(r)

for key, ns in [('recording', 'http://www.onvif.org/ver10/recording/wsdl'),
                ('search', 'http://www.onvif.org/ver10/search/wsdl'),
                ('replay', 'http://www.onvif.org/ver10/replay/wsdl')]:
    out[key + '_service'] = ns in services

# Hand stream URIs to the shell side through a private file (0600), never stdout.
priv = os.path.expanduser('~/sd5531/private/probe-stream-uris.json')
with os.fdopen(os.open(priv, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), 'w') as f:
    json.dump(uris, f)
out['stream_uri_tokens'] = sorted(uris)
print(json.dumps(out, ensure_ascii=False, indent=1))
