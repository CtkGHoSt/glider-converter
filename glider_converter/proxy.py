'''
    基于glider的proxy底座：https://github.com/nadoo/glider/tree/master/proxy
'''

class encryptionBase:
    def __init__(self, passwd=None, method=None):
        self.encryption = f'{method+":" if method is not None else ""}{passwd if passwd is not None else ""}'
    
    def __str__(self):
        return self.encryption

class serverBase:
    def __init__(self, host=None, port=None):
            self.server = f'{host+":" if host is not None else ""}{port if port is not None else ""}'
    
    def __str__(self):
        return self.server

class proxyBase:
    def __init__(self, scheme:str, encryption:encryptionBase, server:serverBase, **params):
        self.scheme = scheme
        self.encryption = encryption
        self.server = server
        self.params = params
        self.base_url = f'{scheme}://{encryption}@{server}{"?" if len(params) > 0 else ""}{"&".join(f"{k}={v}" for k, v in params.items())}'

    def __str__(self):
        return self.base_url

def tls(server, port, skipVerify=None, serverName=None):
    function_params = locals().copy()
    base_url = f'tls://{server}:{port}'
    params = []
    if skipVerify is not None:
        params.append(f'skipVerify={str(skipVerify).lower()}')
    if serverName is not None:
        params.append(f'serverName={serverName}')
    return f'{base_url}{"" if len(params)==0 else "?"+"&".join(params)}'

def ws(server=None, port=None, path=None, host=None, origin=None):
    if server is None and port is None:
        base_url = f'ws://@{"" if path is None else path}'
    else:
        base_url = f'ws://{server}:{port}{"" if path is None else path}'
    params = []
    if host is not None:
        params.append(f'host={host}')
    if origin is not None:
        params.append(f'origin={origin}')
    return f'{base_url}{"" if len(params)==0 else "?"+"&".join(params)}'

def vmess(uuid, security=None, server=None, port=None, alterId=None):
    if security == 'auto':
        security = None
    if security is not None:
        if security not in ['zero', 'none', 'aes-128-gcm', 'chacha20-poly1305']:
            raise ValueError('security must be one of "zero", "none", "aes-128-gcm", "chanacha20-poly1305"')
    return f'vmess://{"" if security is None else security+":"}{uuid}@{"" if server is None else server}:{"" if port is None else port}{"" if alterId is None else f"?alterID={alterId}"}'

def ss(server, port, method, passwd, scheme='ss'):
    '''
    AEAD Ciphers:
      AEAD_AES_128_GCM AEAD_AES_192_GCM AEAD_AES_256_GCM AEAD_CHACHA20_POLY1305 AEAD_XCHACHA20_POLY1305
    Stream Ciphers:
      AES-128-CFB AES-128-CTR AES-192-CFB AES-192-CTR AES-256-CFB AES-256-CTR CHACHA20-IETF XCHACHA20 CHACHA20 RC4-MD5
    Alias:
	  chacha20-ietf-poly1305 = AEAD_CHACHA20_POLY1305, xchacha20-ietf-poly1305 = AEAD_XCHACHA20_POLY1305
    '''
    method_list = ['AEAD_AES_128_GCM', 'AEAD_AES_192_GCM', 'AEAD_AES_256_GCM', 'AEAD_CHACHA20_POLY1305',
        'AEAD_XCHACHA20_POLY1305', 'AES-128-CFB', 'AES-128-CTR', 'AES-192-CFB', 'AES-192-CTR', 'AES-256-CFB',
        'AES-256-CTR', 'CHACHA20-IETF', 'XCHACHA20', 'CHACHA20', 'RC4-MD5', 'chacha20-ietf-poly1305',
        'xchacha20-ietf-poly1305']
    if method not in method_list:
        raise NameError('Unknown method')
    if scheme not in ['ss', 'ssr']:
        raise NameError('Unknown scheme')
    return f'{scheme}://{method}:{passwd}@{server}:{port}'

def ssr(server, port, method, passwd, *args, **kwargs):
    '''
    SSR scheme:
        ssr://method:pass@host:port?protocol=xxx&protocol_param=yyy&obfs=zzz&obfs_param=xyz
    '''
    base_url = ss(server, port, method, passwd, scheme='ssr')
    return f'{base_url}?{"&".join([k+"="+v for k,v in kwargs.items()])}'

def trojan(server, port, passwd, *args, **kwargs):
    """
    trojan scheme:
        trojan://pass@host:port[?serverName=SERVERNAME][&skipVerify=true][&cert=PATH]
    """