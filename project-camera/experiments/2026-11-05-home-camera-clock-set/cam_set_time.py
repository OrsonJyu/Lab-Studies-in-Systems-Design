import base64, datetime, hashlib, json, os, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
SRC = json.load(open(os.path.expanduser('~/sd5531/private/camera_source.json')))
u = urllib.parse.urlsplit(SRC['uri'])
HOST, USER, PASS = u.hostname, urllib.parse.unquote(u.username or ''), urllib.parse.unquote(u.password or '')
NS = {'s': 'http://www.w3.org/2003/05/soap-envelope', 'tt': 'http://www.onvif.org/ver10/schema'}
DEV = f'http://{HOST}:{sys.argv[1]}/onvif/device_service'
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



import re, time
def read():
    st, r = call(DEV, '<tds:GetSystemDateAndTime/>', auth=False)
    x = ET.tostring(r, encoding='unicode')
    seg = x[x.find('UTCDateTime'):]
    v = [int(re.search(r'<[^>]*:%s>(\d+)<' % k, seg).group(1)) for k in ['Year','Month','Day','Hour','Minute','Second']]
    cam = time.mktime(time.struct_time((*v, 0, 0, 0))) - time.timezone   # UTC fields -> epoch
    tz = re.search(r'<[^>]*:TZ>([^<]*)<', x).group(1)
    typ = re.search(r'<[^>]*:DateTimeType>([^<]*)<', x).group(1)
    dst = re.search(r'<[^>]*:DaylightSavings>([^<]*)<', x).group(1)
    return cam, tz, typ, dst
mode = sys.argv[2]
cam, tz, typ, dst = read(); now = time.time()
print(json.dumps({'when': 'before' if mode == 'set' else 'check', 'board_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
                  'camera_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(cam)), 'camera_minus_board_s': round(cam - now, 1),
                  'tz': tz, 'type': typ, 'daylight_savings': dst}))
if mode == 'set':
    # Wait for the start of the next board second so the whole-second value is as exact as possible.
    time.sleep(1 - time.time() % 1)
    g = time.gmtime(time.time())
    body = ('<tds:SetSystemDateAndTime><tds:DateTimeType>Manual</tds:DateTimeType>'
            f'<tds:DaylightSavings>{dst}</tds:DaylightSavings>'
            f'<tds:TimeZone><tt:TZ>{tz}</tt:TZ></tds:TimeZone>'
            '<tds:UTCDateTime><tt:Date>'
            f'<tt:Year>{g.tm_year}</tt:Year><tt:Month>{g.tm_mon}</tt:Month><tt:Day>{g.tm_mday}</tt:Day></tt:Date><tt:Time>'
            f'<tt:Hour>{g.tm_hour}</tt:Hour><tt:Minute>{g.tm_min}</tt:Minute><tt:Second>{g.tm_sec}</tt:Second>'
            '</tt:Time></tds:UTCDateTime></tds:SetSystemDateAndTime>')
    st, r = call(DEV, body)
    print(json.dumps({'set_status': st, 'fault': fault(r), 'set_to_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', g)}))
    time.sleep(2)
    cam, tz, typ, dst = read(); now = time.time()
    print(json.dumps({'when': 'after', 'board_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now)),
                      'camera_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(cam)), 'camera_minus_board_s': round(cam - now, 1),
                      'tz': tz, 'type': typ, 'daylight_savings': dst}))

