import yaml
import requests

from proxy import proxyBase
from proxy import encryptionBase as eb
from proxy import serverBase as sb

def load_nodes(url):
    rr = requests.get(url)
    if rr.status_code != 200:
        raise Exception("Error loading nodes")
    return yaml.load(rr.text, Loader=yaml.FullLoader)['proxies']

def check_nodes_type(func):
    def wrapper(node):
        if node['type'] != func.__name__.split('_')[-1]:
            return None
        return func(node)
    return wrapper

@check_nodes_type
def _format_ss(node):
    method_list = ['AEAD_AES_128_GCM', 'AEAD_AES_192_GCM', 'AEAD_AES_256_GCM', 'AEAD_CHACHA20_POLY1305',
        'AEAD_XCHACHA20_POLY1305', 'AES-128-CFB', 'AES-128-CTR', 'AES-192-CFB', 'AES-192-CTR', 'AES-256-CFB',
        'AES-256-CTR', 'CHACHA20-IETF', 'XCHACHA20', 'CHACHA20', 'RC4-MD5', 'chacha20-ietf-poly1305',
        'xchacha20-ietf-poly1305']
    if node.get('cipher') not in method_list:
        raise NameError(f'Unknown ss method: {node.get("cipher")}')
    ss_proxy = proxyBase(
        scheme=node['type'], 
        encryption=eb(passwd=node.get('password'), method=node.get('cipher')), 
        server=sb(host=node.get('server'), port=node.get('port'))
    )
    return f'{ss_proxy}'

@check_nodes_type
def _format_ssr(node):
    used_params = ['cipher', 'password', 'server', 'port', 'name', 'type']
    # ↓ 格式化参数为glider支持的格式
    params = {k.replace('-', '_'):f'{v if isinstance(v, str) else str(v).lower()}' for k,v in node.items() if k not in used_params}
    ssr_proxy = proxyBase(
        scheme=node['type'], 
        encryption=eb(passwd=node.get('password'), method=node.get('cipher')), 
        server=sb(host=node.get('server'), port=node.get('port')),
        **params
    )
    return f'{ssr_proxy}'

def converter(node):
    try:
        return eval(f'_format_{node["type"]}({node})')
    except NameError:
        raise NameError(f'Unknown proxy type: {node["type"]}')