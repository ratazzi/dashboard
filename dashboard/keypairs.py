import os
import base64
import hashlib

def get_key_fingerprint(line):
    key = base64.b64decode(line.strip().split()[1])
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

def get_keys(username):
    home_dir = os.path.expanduser('~%s' % username)
    authorized_keys = os.path.join(home_dir, '.ssh', 'authorized_keys')
    keys = []
    if not os.path.isfile(authorized_keys):
        return keys

    with open(authorized_keys, 'r') as fp:
        for line in fp.readlines():
            try:
                if len(line) < 50:
                    continue
                name = line.split()[-1].rstrip()
                keys.append({
                    'name': name,
                    'fingerprint': get_key_fingerprint(line.rstrip())
                })
            except Exception:
                pass
    return keys

def add_key(username, key):
    authorized_keys = os.path.join(os.path.expanduser('~%s' % username), '.ssh', 'authorized_keys')
    fingerprint = get_key_fingerprint(key)
    with open(authorized_keys, 'a+') as fp:
        fp.write('%s\n' % key)
        return fingerprint

def delete_key(username, fingerprint):
    authorized_keys = os.path.join(os.path.expanduser('~%s' % username), '.ssh', 'authorized_keys')
    with open(authorized_keys, 'r') as fp:
        lines = fp.readlines()
        with open(authorized_keys, 'w') as output:
            for line in lines:
                if get_key_fingerprint(line.rstrip()) != fingerprint:
                    output.write(line)
