# glider-converter

Based on the https://github.com/tindy2013/subconverter project, converting various protocols to glider-supported formats    
    
基于 https://github.com/tindy2013/subconverter 项目，转换各种协议为glider支持的格式       
推荐使用https://acl4ssr-sub.github.io/ 转换为clash node     
![](https://p.sda1.dev/12/9576a7aae3931e9b74ff521a9b67fbb0/acl4ssr.jpg)

# Usage
```
from converter import load_nodes, converter

# clash subconverter node subscription links
# clash subconverter node订阅链接
link = 'abc.com'

# 获取节点信息
# Get node information
nodes = load_nodes(link)

# 转换为glider支持的样式
# Convert to glider scheme
for node in nodes:
    print(converter(node))
```

# Supported Protocols
|Protocol|convert|Description|
|:-:|:-:|:--|
|ss|√|ss://method:pass@host:port|
|ssr|√|ssr://method:pass@host:port?protocol=xxx&protocol_param=yyy&obfs=zzz&obfs_param=xyz|
|trojan|√|trojan://pass@host:port[?serverName=SERVERNAME][&skipVerify=true][&cert=PATH]|
|VMess|√|vmess://[security:]uuid@host:port[?alterID=num]|
|tls|√|tls://host:port[?serverName=SERVERNAME][&skipVerify=true]|
|ws|√|ws://host:port[/path][?serverName=SERVERNAME][&skipVerify=true]|

# Protocol Chains
目前支持vmess代理链/Currently supports vmess proxy chains:

example：    
```
node = {'name': 'example node',
 'server': 'converter.example.net',
 'port': 80,
 'type': 'vmess',
 'uuid': 'aaaaaaaa-bbbb-dddd-ffff-tttttttttttt',
 'alterId': 0,
 'cipher': 'auto',
 'tls': True,
 'skip-cert-verify': False,
 'network': 'ws',
 'ws-opts': {'path': '/windows', 'headers': {'Host': 'host.example.com'}},
 'udp': True}
```
conversion protocol chain `converter(node)`:
```
tls://converter.example.net:80?skipVerify=false,ws://@/windows?host=host.example.com,vmess://aaaaaaaa-bbbb-dddd-ffff-tttttttttttt@:?alterID=0
```

# TODO
- [ ] 忘记requirements.txt了
- [ ] 根据订阅链接生成glider.conf

# Links
* https://github.com/nadoo/glider: glider is a forward proxy with multiple protocols support, and also a dns/dhcp server with ipset management features(like dnsmasq).
* https://github.com/tindy2013/subconverter: Utility to convert between various subscription format
* https://github.com/ACL4SSR/ACL4SSR: SSR 去广告ACL规则/SS完整GFWList规则/Clash规则碎片，Telegram频道订阅地址

