import yaml
import requests

from proxy import proxyBase
from proxy import encryptionBase as eb
from proxy import serverBase as sb
from proxy import *

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

@check_nodes_type
def _format_vmess(node):
    _is_tls = node.get('tls')
    _network = node.get('network')
    _is_ws = False if _network is None or _network != 'ws' else True
    _ws_opts = node.get('ws-opts')
    _headers = _ws_opts.get('headers') if _ws_opts else None
    _path = _ws_opts.get('path') if _ws_opts else None
    _host = _headers.get('Host') if _headers else None
    _origin = _ws_opts.get('origin') if _ws_opts else None
    _skipVerify = node.get('skip-cert-verify')
    _serverName = node.get('servername')
    server = node.get('server')
    port = node.get('port')
    uuid = node.get('uuid')
    security = node.get('cipher')
    alterId = node.get('alterId')
    
    if _is_tls:
        tls_proxy = tls(server, port, skipVerify=_skipVerify, serverName=_serverName)
        vmess_proxy = vmess(uuid, security=security, alterId=alterId)
        if _is_ws:
            ws_proxy = ws(path=_path, host=_host, origin=_origin)
            return f'{tls_proxy},{ws_proxy},{vmess_proxy}'
        else:
            return f'{tls_proxy},{vmess_proxy}'
    else:
        if _is_ws:
            ws_proxy = ws(server=server, port=port, path=_path, host=_host, origin=_origin)
            vmess_proxy = vmess(uuid, security=security, alterId=alterId)
            return f'{ws_proxy},{vmess_proxy}'
        else:
            return vmess(uuid, server=server, port=port, security=security, alterId=alterId)
            
@check_nodes_type
def _format_trojan(node):
    return trojan(node)


def converter(node):
    try:
        return eval(f'_format_{node["type"]}({node})')
    except NameError:
        raise NameError(f'Unknown proxy type: {node["type"]}')