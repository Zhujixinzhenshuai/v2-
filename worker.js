/**
 * Cloudflare Worker - VLESS/Trojan 链接管理工具
 * 部署：wrangler deploy
 */

export default {
  async fetch(request, env, ctx) {
    return new Response(HTML_CONTENT, {
      headers: {
        "Content-Type": "text/html;charset=utf-8",
        "Cache-Control": "no-cache"
      }
    });
  }
};

const HTML_CONTENT = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VLESS/Trojan 链接管理</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, rgba(30,30,50,0.85) 0%, rgba(50,30,60,0.85) 100%);
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #fff;
            padding: 20px;
        }
        
        .glass {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 16px;
        }
        
        .container { max-width: 1400px; margin: 0 auto; }
        
        h1 { 
            text-align: center; 
            margin-bottom: 20px;
            font-size: 2em;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(102,126,234,0.5);
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .tab:hover { background: rgba(255,255,255,0.15); }
        .tab.active { background: linear-gradient(135deg, #667eea, #764ba2); }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        
        .panel { padding: 20px; }
        
        .panel-title {
            font-size: 1.1em;
            margin-bottom: 15px;
            color: #a0a0ff;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        textarea {
            width: 100%;
            height: 300px;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            color: #fff;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            resize: vertical;
        }
        
        textarea:focus { outline: none; border-color: #667eea; }
        textarea::placeholder { color: rgba(255,255,255,0.4); }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff;
        }
        
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102,126,234,0.4); }
        .btn:active { transform: translateY(0); }
        
        .btn-secondary { background: rgba(255,255,255,0.15); }
        .btn-secondary:hover { background: rgba(255,255,255,0.25); }
        
        .btn-success { background: linear-gradient(135deg, #11998e, #38ef7d); }
        .btn-success:hover { box-shadow: 0 5px 20px rgba(17,153,142,0.4); }
        
        .btn-group { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 15px; }
        
        .field { margin-bottom: 15px; }
        
        .field label {
            display: block;
            margin-bottom: 6px;
            color: #a0a0ff;
            font-size: 13px;
        }
        
        .field input, .field select {
            width: 100%;
            padding: 10px 14px;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: #fff;
            font-size: 14px;
        }
        
        .field input:focus, .field select:focus { outline: none; border-color: #667eea; }
        .field select option { background: #1a1a2e; }
        
        .row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        
        .output {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.4);
            border-radius: 10px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .output-title { color: #38ef7d; margin-bottom: 10px; font-weight: 500; }
        
        .link-item {
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            margin-bottom: 8px;
            word-break: break-all;
            font-family: monospace;
            font-size: 12px;
            position: relative;
        }
        
        .link-item:hover { background: rgba(255,255,255,0.1); }
        
        .copy-btn {
            position: absolute;
            right: 10px;
            top: 10px;
            padding: 4px 10px;
            font-size: 11px;
            background: rgba(102,126,234,0.5);
            border-radius: 4px;
            border: none;
            color: #fff;
            cursor: pointer;
        }
        
        .copy-btn:hover { background: #667eea; }
        
        .batch-config {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .batch-input { height: 200px !important; }
        
        .stats {
            display: flex;
            gap: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .stat { text-align: center; }
        .stat-value { font-size: 2em; font-weight: bold; color: #38ef7d; }
        .stat-label { font-size: 12px; color: #a0a0ff; }
        
        .note {
            padding: 15px;
            background: rgba(255,193,7,0.1);
            border: 1px solid rgba(255,193,7,0.3);
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 13px;
            color: #ffc107;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: rgba(255,255,255,0.5);
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            .row { grid-template-columns: 1fr; }
        }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 VLESS/Trojan 链接管理</h1>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('editor')">📝 编辑模式</div>
            <div class="tab" onclick="switchTab('batch')">⚡ 批量生成</div>
        </div>
        
        <div id="editor" class="tab-content active">
            <div class="grid">
                <div class="panel glass">
                    <div class="panel-title">📥 输入链接</div>
                    <textarea id="inputLinks" placeholder="粘贴 VLESS 或 Trojan 链接..."></textarea>
                    <div class="btn-group">
                        <button class="btn" onclick="parseLinks()">🔍 解析</button>
                        <button class="btn btn-secondary" onclick="loadExample()">📝 加载示例</button>
                        <button class="btn btn-secondary" onclick="clearAll()">🗑️ 清空</button>
                    </div>
                    
                    <div class="panel-title" style="margin-top: 20px;">⚙️ 批量替换</div>
                    <div class="row">
                        <div class="field">
                            <label>旧 ProxyIP</label>
                            <input type="text" id="oldProxy" placeholder="如: krliam.us.ci">
                        </div>
                        <div class="field">
                            <label>新 ProxyIP</label>
                            <input type="text" id="newProxy" placeholder="如: 45.32.36.167">
                        </div>
                    </div>
                    <button class="btn" onclick="batchReplaceProxy()">🔄 批量替换 ProxyIP</button>
                </div>
                
                <div class="panel glass">
                    <div class="panel-title">✏️ 编辑字段</div>
                    
                    <div class="row">
                        <div class="field">
                            <label>协议类型</label>
                            <select id="protocol">
                                <option value="vless">VLESS</option>
                                <option value="trojan">Trojan</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>UUID / 密码</label>
                            <input type="text" id="uuid" placeholder="384cd0f5-d7d2-4c63-b06f-f29595788a45">
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="field">
                            <label>服务器地址</label>
                            <input type="text" id="address" placeholder="87.8.100.1">
                        </div>
                        <div class="field">
                            <label>端口</label>
                            <input type="text" id="port" placeholder="43">
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="field">
                            <label>TLS SNI</label>
                            <input type="text" id="sni" placeholder="joeyh102.xyz">
                        </div>
                        <div class="field">
                            <label>Fingerprint</label>
                            <select id="fp">
                                <option value="random">random</option>
                                <option value="randomized">randomized</option>
                                <option value="chrome">chrome</option>
                                <option value="firefox">firefox</option>
                                <option value="safari">safari</option>
                                <option value="ios">ios</option>
                                <option value="android">android</option>
                                <option value="edge">edge</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="field">
                            <label>ALPN</label>
                            <select id="alpn">
                                <option value="h3,h2,http/1.1">h3,h2,http/1.1 (推荐)</option>
                                <option value="h3">h3 (仅 HTTP/3)</option>
                                <option value="h2">h2 (仅 HTTP/2)</option>
                                <option value="http/1.1">http/1.1 (仅 HTTP/1.1)</option>
                                <option value="h3,http/1.1">h3,http/1.1 (混合)</option>
                                <option value="h2,http/1.1">h2,http/1.1 (混合)</option>
                            </select>
                        </div>
                        <div class="field">
                            <label>传输网络</label>
                            <select id="network">
                                <option value="ws">WebSocket (WS)</option>
                                <option value="grpc">gRPC</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="field">
                            <label>Host</label>
                            <input type="text" id="host" placeholder="joey102.xyz">
                        </div>
                        <div class="field">
                            <label>Path</label>
                            <input type="text" id="path" placeholder="/proxyip=xxx">
                        </div>
                    </div>
                    
                    <div class="field">
                        <label>显示名称</label>
                        <input type="text" id="remark" placeholder="JP 🇯🇵🇯🇵🇯🇵">
                    </div>
                    
                    <button class="btn btn-success" onclick="generateLink()">✨ 生成链接</button>
                    <button class="btn btn-secondary" onclick="copyLink()">📋 复制</button>
                </div>
            </div>
            
            <div class="panel glass" style="margin-top: 20px;">
                <div class="panel-title">📤 生成的链接</div>
                <textarea id="output" readonly placeholder="生成的链接会显示在这里..."></textarea>
                <div class="btn-group">
                    <button class="btn" onclick="copyOutput()">📋 复制全部</button>
                    <button class="btn btn-secondary" onclick="downloadOutput()">💾 下载 TXT</button>
                </div>
            </div>
        </div>
        
        <div id="batch" class="tab-content">
            <div class="panel glass">
                <div class="panel-title">⚡ 批量生成模式</div>
                
                <div class="note">
                    💡 支持多种格式：<br>
                    • 每行一个IP：``<br>
                    • IP:端口：``<br>
                    • IP|名称：``<br>
                    • 完整格式：`IP|端口|地址`
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value" id="ipCount">0</div>
                        <div class="stat-label">待生成</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="batchCount">0</div>
                        <div class="stat-label">已生成</div>
                    </div>
                </div>
                
                <div class="batch-config">
                    <div class="field">
                        <label>协议类型</label>
                        <select id="batchProtocol">
                            <option value="vless">VLESS</option>
                            <option value="trojan">Trojan</option>
                        </select>
                    </div>
                    <div class="field">
                        <label>UUID / 密码</label>
                        <input type="text" id="batchUuid" value="384cd0f5-d7d2-4c63-b06f-f29595788a45">
                    </div>
                    <div class="field">
                        <label>默认端口</label>
                        <input type="text" id="batchPort" value="443">
                    </div>
                    <div class="field">
                        <label>TLS SNI</label>
                        <input type="text" id="batchSni" value="joeyhuang.19960102.xyz">
                    </div>
                    <div class="field">
                        <label>Fingerprint</label>
                        <select id="batchFp">
                            <option value="random">random</option>
                            <option value="randomized">randomized</option>
                            <option value="chrome">chrome</option>
                            <option value="firefox">firefox</option>
                            <option value="safari">safari</option>
                        </select>
                    </div>
                    <div class="field">
                        <label>ALPN</label>
                        <select id="batchAlpn">
                            <option value="h3,h2,http/1.1">h3,h2,http/1.1 (推荐)</option>
                            <option value="h3">h3</option>
                            <option value="h2">h2</option>
                            <option value="http/1.1">http/1.1</option>
                        </select>
                    </div>
                    <div class="field">
                        <label>Host</label>
                        <input type="text" id="batchHost" value="joeyhuang.19960102.xyz">
                    </div>
                    <div class="field">
                        <label>名称前缀</label>
                        <input type="text" id="batchPrefix" value="JP">
                    </div>
                </div>
                
                <div class="field">
                    <label>ProxyIP 列表（每行一个）</label>
                    <textarea id="batchIps" class="batch-input" placeholder="粘贴 IP 列表...&#10;45.32.36.167&#10;45.32.36.168&#10;45.32.36.169"></textarea>
                </div>
                
                <div class="btn-group">
                    <button class="btn btn-success" onclick="batchGenerate()">⚡ 批量生成</button>
                    <button class="btn" onclick="loadBatchExample()">📝 加载示例</button>
                    <button class="btn btn-secondary" onclick="batchClear()">🗑️ 清空</button>
                </div>
                
                <div class="output" style="margin-top: 20px;">
                    <div class="output-title">生成的链接：</div>
                    <div id="batchOutput"></div>
                </div>
                
                <div class="btn-group" style="margin-top: 15px;">
                    <button class="btn" onclick="copyBatchOutput()">📋 复制全部</button>
                    <button class="btn btn-secondary" onclick="downloadBatchOutput()">💾 下载 TXT</button>
                </div>
            </div>
        </div>
        
        <div class="footer">
            © 2026 VLESS/Trojan 链接管理工具 | 仅供学习使用
        </div>
    </div>
    
    <script>
        let currentParsed = null;
        
        function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tab).classList.add('active');
        }
        
        function parseLinks() {
            const input = document.getElementById('inputLinks').value.trim();
            if (!input) return alert('请先粘贴链接！');
            const lines = input.split('\n').filter(l => l.trim());
            if (lines.length === 0) return alert('未检测到链接！');
            const link = lines[0].trim();
            currentParsed = parseUrl(link);
            if (currentParsed) {
                document.getElementById('protocol').value = currentParsed.protocol;
                document.getElementById('uuid').value = currentParsed.uuid;
                document.getElementById('address').value = currentParsed.address;
                document.getElementById('port').value = currentParsed.port;
                document.getElementById('sni').value = currentParsed.sni || '';
                document.getElementById('fp').value = currentParsed.fp || 'random';
                document.getElementById('alpn').value = currentParsed.alpn || 'h3,h2,http/1.1';
                document.getElementById('network').value = currentParsed.network || 'ws';
                document.getElementById('host').value = currentParsed.host || '';
                document.getElementById('path').value = currentParsed.path || '';
                document.getElementById('remark').value = currentParsed.remark || '';
            }
        }
        
        function parseUrl(url) {
            try {
                let protocol, uuid, address, port, params = {}, remark = '';
                if (url.startsWith('vless://')) {
                    protocol = 'vless';
                    const withoutProto = url.substring(8);
                    const atIndex = withoutProto.indexOf('@');
                    uuid = withoutProto.substring(0, atIndex);
                    const rest = withoutProto.substring(atIndex + 1);
                    const hashIndex = rest.indexOf('#');
                    let mainPart = rest;
                    if (hashIndex !== -1) {
                        remark = decodeURIComponent(rest.substring(hashIndex + 1));
                        mainPart = rest.substring(0, hashIndex);
                    }
                    const qIndex = mainPart.indexOf('?');
                    if (qIndex !== -1) {
                        const hostPart = mainPart.substring(0, qIndex);
                        const queryPart = mainPart.substring(qIndex + 1);
                        const colonHost = hostPart.lastIndexOf(':');
                        if (colonHost !== -1) {
                            address = hostPart.substring(0, colonHost);
                            port = hostPart.substring(colonHost + 1);
                        }
                        queryPart.split('&').forEach(p => {
                            const [k, v] = p.split('=');
                            params[decodeURIComponent(k)] = decodeURIComponent(v || '');
                        });
                    } else {
                        const colonHost = mainPart.lastIndexOf(':');
                        if (colonHost !== -1) {
                            address = mainPart.substring(0, colonHost);
                            port = mainPart.substring(colonHost + 1);
                        }
                    }
                } else if (url.startsWith('trojan://')) {
                    protocol = 'trojan';
                    const withoutProto = url.substring(9);
                    const atIndex = withoutProto.indexOf('@');
                    uuid = withoutProto.substring(0, atIndex);
                    const rest = withoutProto.substring(atIndex + 1);
                    const hashIndex = rest.indexOf('#');
                    if (hashIndex !== -1) {
                        remark = decodeURIComponent(rest.substring(hashIndex + 1));
                    }
                    const qIndex = rest.indexOf('?');
                    let hostPart = rest;
                    if (qIndex !== -1) {
                        hostPart = rest.substring(0, qIndex);
                        const queryPart = rest.substring(qIndex + 1);
                        queryPart.split('&').forEach(p => {
                            const [k, v] = p.split('=');
                            params[decodeURIComponent(k)] = decodeURIComponent(v || '');
                        });
                    }
                    const colonHost = hostPart.lastIndexOf(':');
                    if (colonHost !== -1) {
                        address = hostPart.substring(0, colonHost);
                        port = hostPart.substring(colonHost + 1);
                    }
                    params.password = uuid;
                }
                return {
                    protocol,
                    uuid: params.password || uuid,
                    address,
                    port,
                    sni: params.sni || params.peer || '',
                    fp: params.fp || params.fingerprint || 'random',
                    alpn: params.alpn || 'h3,h2,http/1.1',
                    network: params.type || 'ws',
                    host: params.host || '',
                    path: params.path || '',
                    remark
                };
            } catch (e) {
                alert('解析失败: ' + e.message);
                return null;
            }
        }
        
        function generateLink() {
            const protocol = document.getElementById('protocol').value;
            const uuid = document.getElementById('uuid').value.trim();
            const address = document.getElementById('address').value.trim();
            const port = document.getElementById('port').value.trim();
            const sni = document.getElementById('sni').value.trim();
            const fp = document.getElementById('fp').value;
            const alpn = document.getElementById('alpn').value;
            const network = document.getElementById('network').value;
            const host = document.getElementById('host').value.trim();
            const path = document.getElementById('path').value.trim();
            const remark = document.getElementById('remark').value.trim();
            if (!address || !port) {
                alert('请填写服务器地址和端口！');
                return;
            }
            let link = '';
            if (protocol === 'vless') {
                const uuidPart = uuid || '384cd0f5-d7d2-4c63-b06f-f29595788a45';
                const params = new URLSearchParams({
                    encryption: 'none',
                    security: 'tls',
                    sni: sni || host,
                    fp: fp,
                    alpn: alpn,
                    insecure: '1',
                    allowInsecure: '1',
                    type: network,
                    host: host || sni,
                    path: path || '/'
                });
                link = 'vless://' + uuidPart + '@' + address + ':' + port + '?' + params.toString() + '#' + encodeURIComponent(remark || '节点');
            } else {
                const password = uuid || 'password';
                const params = new URLSearchParams({
                    security: 'tls',
                    sni: sni || host,
                    fp: fp,
                    alpn: alpn,
                    insecure: '1',
                    allowInsecure: '1',
                    type: network,
                    host: host || sni,
                    path: path || '/'
                });
                link = 'trojan://' + password + '@' + address + ':' + port + '?' + params.toString() + '#' + encodeURIComponent(remark || '节点');
            }
            document.getElementById('output').value = link;
        }
        
        function copyLink() {
            const output = document.getElementById('output').value;
            if (!output) return alert('没有链接可复制！');
            navigator.clipboard.writeText(output);
            alert('已复制到剪贴板！');
        }
        
        function copyOutput() {
            const output = document.getElementById('output').value;
            if (!output) return;
            navigator.clipboard.writeText(output);
            alert('已复制！');
        }
        
        function downloadOutput() {
            const output = document.getElementById('output').value;
            if (!output) return;
            downloadText(output, 'links.txt');
        }
        
        function batchReplaceProxy() {
            const oldProxy = document.getElementById('oldProxy').value.trim();
            const newProxy = document.getElementById('newProxy').value.trim();
            const input = document.getElementById('inputLinks').value;
            if (!oldProxy || !input) {
                alert('请填写旧ProxyIP和输入链接！');
                return;
            }
            const lines = input.split('\n');
            const result = lines.map(line => {
                if (line.includes(oldProxy)) {
                    return line.replace(oldProxy, newProxy || '');
                }
                return line;
            });
            document.getElementById('inputLinks').value = result.join('\n');
            alert('已替换 ' + lines.filter(l => l.includes(oldProxy)).length + ' 条！');
        }
        
        function batchGenerate() {
            const protocol = document.getElementById('batchProtocol').value;
            const uuid = document.getElementById('batchUuid').value.trim() || '384cd0f5-d7d2-4c63-b06f-f29595788a45';
            const defaultPort = document.getElementById('batchPort').value.trim() || '443';
            const sni = document.getElementById('batchSni').value.trim();
            const fp = document.getElementById('batchFp').value;
            const alpn = document.getElementById('batchAlpn').value;
            const host = document.getElementById('batchHost').value.trim();
            const prefix = document.getElementById('batchPrefix').value.trim();
            const ipText = document.getElementById('batchIps').value.trim();
            if (!ipText) {
                alert('请输入IP列表！');
                return;
            }
            const lines = ipText.split('\n').filter(l => l.trim());
            document.getElementById('ipCount').textContent = lines.length;
            const results = [];
            lines.forEach((line, i) => {
                line = line.trim();
                let ip, port = defaultPort, name = '';
                if (line.includes('|')) {
                    const parts = line.split('|');
                    ip = parts[0].trim();
                    name = parts.slice(1).join('|');
                } else if (line.includes(':')) {
                    const colonIdx = line.lastIndexOf(':');
                    ip = line.substring(0, colonIdx);
                    port = line.substring(colonIdx + 1).split(' ')[0];
                } else {
                    ip = line.split(' ')[0];
                }
                if (!name) {
                    const ipParts = ip.split('.');
                    if (ipParts.length === 4) {
                        name = (prefix || 'Node') + '-' + ipParts[3];
                    } else {
                        name = prefix || 'Node';
                    }
                }
                const remark = (prefix || 'JP') + ' ' + name;
                let link = '';
                if (protocol === 'vless') {
                    const params = new URLSearchParams({
                        encryption: 'none',
                        security: 'tls',
                        sni: sni || host,
                        fp: fp,
                        alpn: alpn,
                        insecure: '1',
                        allowInsecure: '1',
                        type: 'ws',
                        host: host || sni,
                        path: '/'
                    });
                    link = 'vless://' + uuid + '@' + ip + ':' + port + '?' + params.toString() + '#' + encodeURIComponent(remark);
                } else {
                    const params = new URLSearchParams({
                        security: 'tls',
                        sni: sni || host,
                        fp: fp,
                        alpn: alpn,
                        insecure: '1',
                        allowInsecure: '1',
                        type: 'ws',
                        host: host || sni,
                        path: '/'
                    });
                    link = 'trojan://' + uuid + '@' + ip + ':' + port + '?' + params.toString() + '#' + encodeURIComponent(remark);
                }
                results.push(link);
            });
            document.getElementById('batchCount').textContent = results.length;
            const outputDiv = document.getElementById('batchOutput');
            outputDiv.innerHTML = results.map(link => {
                const encoded = encodeURIComponent(link);
                return '<div class="link-item">' + escapeHtml(link) + '<button class="copy-btn" onclick="copySingleLink(this, \\'' + encoded + '\\')">复制</button></div>';
            }).join('');
        }
        
        function copySingleLink(btn, encoded) {
            navigator.clipboard.writeText(decodeURIComponent(encoded));
            btn.textContent = '已复制!';
            setTimeout(function() { btn.textContent = '复制'; }, 1500);
        }
        
        function copyBatchOutput() {
            const links = document.querySelectorAll('#batchOutput .link-item');
            if (links.length === 0) return;
            const text = Array.from(links).map(function(l) { return l.textContent.replace('复制', '').trim(); }).join('\n');
            navigator.clipboard.writeText(text);
            alert('已复制 ' + links.length + ' 条链接！');
        }
        
        function downloadBatchOutput() {
            const links = document.querySelectorAll('#batchOutput .link-item');
            if (links.length === 0) return;
            const text = Array.from(links).map(function(l) { return l.textContent.replace('复制', '').trim(); }).join('\n');
            downloadText(text, 'links_' + Date.now() + '.txt');
        }
        
        function downloadText(text, filename) {
            const blob = new Blob([text], { type: 'text/plain' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = filename;
            a.click();
        }
        
        function escapeHtml(text) {
            return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }
        
        function loadExample() {
            document.getElementById('inputLinks').value = 'vless://384cd0f5-d7d2-4c63-b06f-f29595788a45@87.83.100.1:443?encryption=none&security=tls&sni=joeyhuang.19960102.xyz&fp=random&alpn=h3%2Ch2%2Chttp%2F1.1&insecure=1&allowInsecure=1&type=ws&host=joeyhuang.19960102.xyz&path=%2Fproxyip%3Dkr.william.us.ci#JP%20%7C%20%E6%97%A5%E6%9C%AC%E2%AD%90%E2%AD%90%E2%AD%90\ntrojan://beb4a73a-cf04-4c34-8626-214c53f744af@47.76.218.163:443?security=tls&sni=trojancm.19960102.xyz&fp=randomized&alpn=h3&insecure=1&allowInsecure=1&type=ws&host=trojancm.19960102.xyz&path=%2Fproxyip%3D79998553.tp30001.ip.090227.xyz%3Fed%3D2560#HK%F0%9F%90%B2%E2%84%A2%EF%B8%8F%E3%80%90%E8%AF%B7%E5%BF%97%E6%B5%8B%E9%80%9F%E3%80%91';
        }
        
        function loadBatchExample() {
            document.getElementById('batchIps').value = '45.32.36.167\n45.32.36.168|美国\n45.32.36.169:443|日本\n45.32.36.170|新加坡|8080';
        }
        
        function clearAll() {
            document.getElementById('inputLinks').value = '';
            document.getElementById('output').value = '';
            document.getElementById('oldProxy').value = '';
            document.getElementById('newProxy').value = '';
        }
        
        function batchClear() {
            document.getElementById('batchIps').value = '';
            document.getElementById('batchOutput').innerHTML = '';
            document.getElementById('ipCount').textContent = '0';
            document.getElementById('batchCount').textContent = '0';
        }
    </script>
</body>
</html>`;
