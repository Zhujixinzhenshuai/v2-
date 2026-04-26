#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VLESS & Trojan 链接管理工具
磨砂质感界面 - 小朱专属
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from urllib.parse import unquote, quote
import re
import json
from PIL import Image, ImageTk
import os
import math

# 背景图片路径
BG_IMAGE = r"Z:\已下载\大图\横 (1288).jpg"

class VlessTrojanTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🔗 VLESS & Trojan 链接管理工具")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # 尝试加载背景图片
        self.bg_image = None
        self.bg_photo = None
        self.canvas = None
        
        try:
            if os.path.exists(BG_IMAGE):
                img = Image.open(BG_IMAGE)
                # 缩放到窗口大小
                self.bg_image = img.resize((1600, 1000), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.create_blur_ui()
            else:
                self.create_simple_ui()
        except Exception as e:
            print(f"背景加载失败: {e}")
            self.create_simple_ui()
        
        # 当前选中的链接类型
        self.current_type = tk.StringVar(value="VLESS")
        
        # 存储解析后的数据
        self.current_links = []
        
    def create_blur_ui(self):
        """创建磨砂质感界面"""
        # 创建画布放置背景
        self.canvas = tk.Canvas(self.root, width=1400, height=900, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_photo)
        
        # 创建磨砂效果覆盖层
        self.blur_frame = tk.Frame(self.canvas, bg='#1a1a2e', bd=0)
        self.blur_frame.configure(bg='#1a1a2e')
        
        # 创建主容器（带透明效果）
        self.main_container = tk.Frame(self.canvas, bg='#ffffff', bd=0)
        self.main_container.configure(bg='#ffffff')
        
        # 放置主容器
        container = self.canvas.create_window(50, 50, window=self.main_container, width=1300, height=800, anchor='nw')
        
        self.setup_ui()
        
    def create_simple_ui(self):
        """备用简单界面"""
        self.main_container = tk.Frame(self.root, bg='#1a1a2e')
        self.main_container.pack(fill='both', expand=True)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI组件"""
        # 标题栏
        title_frame = tk.Frame(self.main_container, bg='#16213e', height=60)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame, 
            text="🔗 VLESS & Trojan 链接管理工具",
            font=("Microsoft YaHei", 20, "bold"),
            fg='#e94560',
            bg='#16213e'
        ).pack(side='left', padx=20, pady=10)
        
        tk.Label(
            title_frame,
            text="小朱专属工具",
            font=("Microsoft YaHei", 10),
            fg='#a0a0a0',
            bg='#16213e'
        ).pack(side='right', padx=20, pady=10)
        
        # 主内容区域
        content = tk.Frame(self.main_container, bg='#f0f0f0')
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 左侧：输入区域
        left_frame = tk.Frame(content, bg='#ffffff', width=450)
        left_frame.pack(side='left', fill='both', padx=(0, 5), pady=0)
        left_frame.pack_propagate(False)
        
        # 类型选择
        type_frame = tk.LabelFrame(left_frame, text="📋 链接类型", font=("Microsoft YaHei", 11, "bold"),
                                    bg='#ffffff', fg='#333333', padx=10, pady=5)
        type_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        tk.Radiobutton(type_frame, text="VLESS", variable=self.current_type, value="VLESS",
                       font=("Microsoft YaHei", 10), bg='#ffffff', command=self.update_preset).pack(side='left', padx=20)
        tk.Radiobutton(type_frame, text="Trojan", variable=self.current_type, value="Trojan",
                       font=("Microsoft YaHei", 10), bg='#ffffff', command=self.update_preset).pack(side='left', padx=20)
        
        # 原始链接输入
        input_frame = tk.LabelFrame(left_frame, text="📝 原始链接 (粘贴或拖入)", 
                                     font=("Microsoft YaHei", 11, "bold"),
                                     bg='#ffffff', fg='#333333', padx=10, pady=5)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.input_text = tk.Text(input_frame, font=("Consolas", 10), wrap='word',
                                   bg='#f8f9fa', fg='#333333', insertbackground='#e94560')
        scroll_input = tk.Scrollbar(input_frame, command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=scroll_input.set)
        scroll_input.pack(side='right', fill='y')
        self.input_text.pack(fill='both', expand=True)
        
        # 按钮区域
        btn_frame = tk.Frame(left_frame, bg='#ffffff', height=50)
        btn_frame.pack(fill='x', padx=10, pady=5)
        btn_frame.pack_propagate(False)
        
        tk.Button(btn_frame, text="🔍 解析链接", command=self.parse_links,
                 font=("Microsoft YaHei", 10, "bold"), bg='#e94560', fg='white',
                 cursor='hand2', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ 清空", command=self.clear_all,
                 font=("Microsoft YaHei", 10), bg='#6c757d', fg='white',
                 cursor='hand2', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="📂 导入文件", command=self.import_file,
                 font=("Microsoft YaHei", 10), bg='#28a745', fg='white',
                 cursor='hand2', padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="💾 导出文件", command=self.export_file,
                 font=("Microsoft YaHei", 10), bg='#007bff', fg='white',
                 cursor='hand2', padx=15, pady=5).pack(side='right', padx=5)
        
        # 右侧：模块化编辑区域
        right_frame = tk.Frame(content, bg='#f0f0f0')
        right_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        # 模块编辑区
        edit_frame = tk.LabelFrame(right_frame, text="✏️ 模块化编辑", 
                                   font=("Microsoft YaHei", 12, "bold"),
                                   bg='#ffffff', fg='#333333', padx=15, pady=10)
        edit_frame.pack(fill='both', expand=True)
        
        # 创建模块输入框
        self.modules = {}
        
        # 第一行：UUID/密码 + 基础参数
        row1 = tk.Frame(edit_frame, bg='#ffffff')
        row1.pack(fill='x', pady=3)
        
        tk.Label(row1, text="UUID/密码:", font=("Microsoft YaHei", 9), bg='#ffffff', width=12).pack(side='left')
        self.modules['uuid'] = tk.Entry(row1, font=("Consolas", 10), width=40, bg='#f8f9fa')
        self.modules['uuid'].pack(side='left', padx=5)
        
        tk.Label(row1, text="地址:", font=("Microsoft YaHei", 9), bg='#ffffff', width=8).pack(side='left')
        self.modules['address'] = tk.Entry(row1, font=("Consolas", 10), width=20, bg='#f8f9fa')
        self.modules['address'].pack(side='left', padx=5)
        
        tk.Label(row1, text="端口:", font=("Microsoft YaHei", 9), bg='#ffffff', width=6).pack(side='left')
        self.modules['port'] = tk.Entry(row1, font=("Consolas", 10), width=8, bg='#f8f9fa')
        self.modules['port'].pack(side='left')
        
        # 第二行：SNI + Host
        row2 = tk.Frame(edit_frame, bg='#ffffff')
        row2.pack(fill='x', pady=3)
        
        tk.Label(row2, text="SNI:", font=("Microsoft YaHei", 9), bg='#ffffff', width=12).pack(side='left')
        self.modules['sni'] = tk.Entry(row2, font=("Consolas", 10), width=30, bg='#f8f9fa')
        self.modules['sni'].pack(side='left', padx=5)
        
        tk.Label(row2, text="Host:", font=("Microsoft YaHei", 9), bg='#ffffff', width=6).pack(side='left')
        self.modules['host'] = tk.Entry(row2, font=("Consolas", 10), width=25, bg='#f8f9fa')
        self.modules['host'].pack(side='left', padx=5)
        
        tk.Label(row2, text="Path:", font=("Microsoft YaHei", 9), bg='#ffffff', width=6).pack(side='left')
        self.modules['path'] = tk.Entry(row2, font=("Consolas", 10), width=20, bg='#f8f9fa')
        self.modules['path'].pack(side='left')
        
        # 第三行：安全参数
        row3 = tk.Frame(edit_frame, bg='#ffffff')
        row3.pack(fill='x', pady=3)
        
        tk.Label(row3, text="Security:", font=("Microsoft YaHei", 9), bg='#ffffff', width=12).pack(side='left')
        self.modules['security'] = ttk.Combobox(row3, values=['tls', 'none'], width=10, state='readonly')
        self.modules['security'].current(0)
        self.modules['security'].pack(side='left', padx=5)
        
        tk.Label(row3, text="Fingerprint:", font=("Microsoft YaHei", 9), bg='#ffffff', width=10).pack(side='left')
        self.modules['fp'] = ttk.Combobox(row3, values=['chrome', 'random', 'randomized', 'ios', 'android'], 
                                           width=12, state='readonly')
        self.modules['fp'].current(0)
        self.modules['fp'].pack(side='left', padx=5)
        
        tk.Label(row3, text="ALPN:", font=("Microsoft YaHei", 9), bg='#ffffff', width=6).pack(side='left')
        self.modules['alpn'] = tk.Entry(row3, font=("Consolas", 10), width=30, bg='#f8f9fa')
        self.modules['alpn'].insert(0, "h3,h2,http/1.1")
        self.modules['alpn'].pack(side='left')
        
        # 第四行：网络类型 + 代理IP + 显示名称
        row4 = tk.Frame(edit_frame, bg='#ffffff')
        row4.pack(fill='x', pady=3)
        
        tk.Label(row4, text="Network:", font=("Microsoft YaHei", 9), bg='#ffffff', width=12).pack(side='left')
        self.modules['type'] = ttk.Combobox(row4, values=['ws', 'grpc', 'h2', 'http'], width=10, state='readonly')
        self.modules['type'].current(0)
        self.modules['type'].pack(side='left', padx=5)
        
        tk.Label(row4, text="ProxyIP:", font=("Microsoft YaHei", 9), bg='#ffffff', width=8).pack(side='left')
        self.modules['proxyip'] = tk.Entry(row4, font=("Consolas", 10), width=25, bg='#fff3cd')
        self.modules['proxyip'].pack(side='left', padx=5)
        
        tk.Label(row4, text="显示名称:", font=("Microsoft YaHei", 9), bg='#ffffff', width=8).pack(side='left')
        self.modules['name'] = tk.Entry(row4, font=("Microsoft YaHei", 10), width=30, bg='#d4edda')
        self.modules['name'].pack(side='left')
        
        # 第五行：批量操作
        row5 = tk.Frame(edit_frame, bg='#e8f4f8', height=50)
        row5.pack(fill='x', pady=(10, 5), ipady=8)
        row5.pack_propagate(False)
        
        tk.Label(row5, text="⚡ 批量操作:", font=("Microsoft YaHei", 10, "bold"), 
                bg='#e8f4f8', fg='#0066cc').pack(side='left', padx=10)
        
        tk.Button(row5, text="🔄 替换 ProxyIP", command=self.batch_replace_proxyip,
                 font=("Microsoft YaHei", 9), bg='#17a2b8', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(row5, text="🔄 批量改端口", command=self.batch_change_port,
                 font=("Microsoft YaHei", 9), bg='#6610f2', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(row5, text="🔄 批量改名称", command=self.batch_change_name,
                 font=("Microsoft YaHei", 9), bg='#fd7e14', fg='white', cursor='hand2').pack(side='left', padx=5)
        tk.Button(row5, text="🔄 批量改SNI", command=self.batch_change_sni,
                 font=("Microsoft YaHei", 9), bg='#20c997', fg='white', cursor='hand2').pack(side='left', padx=5)
        
        # 生成预览
        preview_frame = tk.LabelFrame(edit_frame, text="👁️ 生成结果预览", 
                                     font=("Microsoft YaHei", 11, "bold"),
                                     bg='#ffffff', fg='#333333', padx=10, pady=5)
        preview_frame.pack(fill='x', pady=(10, 0), ipady=5)
        
        self.preview_text = tk.Text(preview_frame, font=("Consolas", 9), height=3,
                                     bg='#1e1e1e', fg='#00ff00', wrap='word')
        self.preview_text.pack(fill='x', padx=5, pady=5)
        
        # 生成按钮
        gen_btn = tk.Button(edit_frame, text="✨ 生成链接", command=self.generate_link,
                           font=("Microsoft YaHei", 12, "bold"), bg='#28a745', fg='white',
                           cursor='hand2', padx=20, pady=8)
        gen_btn.pack(pady=10)
        
        # 底部状态栏
        self.status_var = tk.StringVar(value="就绪 | 等待输入链接...")
        status_bar = tk.Label(self.main_container, textvariable=self.status_var,
                             font=("Microsoft YaHei", 9), fg='#666666', bg='#f0f0f0', anchor='w')
        status_bar.pack(fill='x', padx=10, pady=(0, 5))
        
        # 填充示例数据
        self.fill_example()
        
    def fill_example(self):
        """填充示例数据"""
        vless_example = """vless://384cd0f5-d7d2-4c63-b06f-f29595788a45@87.83.100.1:443?encryption=none&security=tls&sni=joeyhuang.19960102.xyz&fp=random&alpn=h3%2Ch2%2Chttp%2F1.1&insecure=1&allowInsecure=1&type=ws&host=joeyhuang.19960102.xyz&path=%2Fproxyip%3Dkr.william.us.ci#JP%20%7C%20%E6%97%A5%E6%9C%AC%E2%AD%90%E2%AD%90%E2%AD%90"""
        self.input_text.insert('1.0', vless_example)
        
    def update_preset(self):
        """更新预设值"""
        link_type = self.current_type.get()
        if link_type == "VLESS":
            self.modules['security'].current(0)
            self.modules['fp'].current(1)
            self.modules['alpn'].delete(0, 'end')
            self.modules['alpn'].insert(0, "h3,h2,http/1.1")
            self.modules['type'].current(0)
        else:  # Trojan
            self.modules['security'].current(0)
            self.modules['fp'].current(2)
            self.modules['alpn'].delete(0, 'end')
            self.modules['alpn'].insert(0, "h3")
            self.modules['type'].current(0)
        self.update_preview()
        
    def parse_links(self):
        """解析链接"""
        text = self.input_text.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning("提示", "请先粘贴链接！")
            return
            
        self.current_links = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('vless://'):
                parsed = self.parse_vless(line)
                if parsed:
                    self.current_links.append(parsed)
            elif line.startswith('trojan://'):
                parsed = self.parse_trojan(line)
                if parsed:
                    self.current_links.append(parsed)
            elif line.startswith('vmess://'):
                parsed = self.parse_vmess(line)
                if parsed:
                    self.current_links.append(parsed)
        
        if self.current_links:
            self.display_link(0)
            self.status_var.set(f"已解析 {len(self.current_links)} 条链接 | 第 1/{len(self.current_links)} 条")
        else:
            messagebox.showerror("错误", "未能解析任何链接，请检查格式！")
            
    def parse_vless(self, link):
        """解析VLESS链接"""
        try:
            link = link.replace('vless://', '')
            # 分离前半部分(用户信息)和后半部分(查询参数)
            if '@' in link:
                user_info, rest = link.split('@', 1)
                uuid = user_info
            else:
                return None
            
            # 分离路径和查询参数
            if '?' in rest:
                path_part, query_part = rest.split('?', 1)
            else:
                path_part = rest
                query_part = ''
            
            # 分离主机端口和名称
            if '#' in path_part:
                host_port, name = path_part.split('#', 1)
            else:
                host_port = path_part
                name = ''
            
            # 分离主机和端口
            if ':' in host_port:
                address, port = host_port.split(':', 1)
            else:
                address = host_port
                port = '443'
            
            # 解析查询参数
            params = {}
            if '?' in rest:
                query = rest.split('?', 1)[1].split('#')[0]
                for param in query.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[unquote(key)] = unquote(value)
            
            # 提取proxyip
            proxyip = ''
            if 'path' in params:
                path = params['path']
                match = re.search(r'proxyip=([^&]+)', path)
                if match:
                    proxyip = match.group(1)
            
            return {
                'type': 'VLESS',
                'uuid': uuid,
                'address': address,
                'port': port,
                'name': unquote(name.replace('+', ' ')),
                'sni': params.get('sni', ''),
                'host': params.get('host', ''),
                'fp': params.get('fp', 'chrome'),
                'alpn': params.get('alpn', 'h3,h2,http/1.1'),
                'security': params.get('security', 'tls'),
                'type_net': params.get('type', 'ws'),
                'proxyip': proxyip,
                'path': params.get('path', ''),
                'insecure': params.get('insecure', '1'),
                'raw': link
            }
        except Exception as e:
            print(f"解析VLESS错误: {e}")
            return None
            
    def parse_trojan(self, link):
        """解析Trojan链接"""
        try:
            link = link.replace('trojan://', '')
            
            if '@' in link:
                user_info, rest = link.split('@', 1)
                password = user_info
            else:
                return None
                
            # 分离主机端口和名称
            if '#' in rest:
                host_port, name = rest.split('#', 1)
            else:
                host_port = rest
                name = ''
            
            # 分离主机和端口
            if ':' in host_port:
                address, port = host_port.split(':', 1)
            else:
                address = host_port
                port = '443'
            
            # 解析查询参数
            params = {}
            if '?' in host_port:
                query = host_port.split('?', 1)[1].split('#')[0]
                for param in query.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[unquote(key)] = unquote(value)
            
            # 提取proxyip
            proxyip = ''
            if 'path' in params:
                path = params['path']
                match = re.search(r'proxyip=([^&]+)', path)
                if match:
                    proxyip = match.group(1)
            
            return {
                'type': 'Trojan',
                'uuid': password,  # Trojan用密码
                'address': address,
                'port': port,
                'name': unquote(name.replace('+', ' ')),
                'sni': params.get('sni', ''),
                'host': params.get('host', ''),
                'fp': params.get('fp', 'random'),
                'alpn': params.get('alpn', 'h3'),
                'security': params.get('security', 'tls'),
                'type_net': params.get('type', 'ws'),
                'proxyip': proxyip,
                'path': params.get('path', ''),
                'insecure': params.get('insecure', '1'),
                'raw': link
            }
        except Exception as e:
            print(f"解析Trojan错误: {e}")
            return None
            
    def parse_vmess(self, link):
        """解析VMess链接（简化版）"""
        try:
            import base64
            link = link.replace('vmess://', '')
            json_str = base64.b64decode(link).decode('utf-8')
            data = json.loads(json_str)
            return {
                'type': 'VMess',
                'name': data.get('ps', ''),
                'address': data.get('add', ''),
                'port': str(data.get('port', '')),
                'uuid': data.get('id', ''),
                'proxyip': '',
                'raw': link
            }
        except:
            return None
            
    def display_link(self, index):
        """显示指定索引的链接"""
        if 0 <= index < len(self.current_links):
            link = self.current_links[index]
            self.current_type.set(link['type'])
            
            self.modules['uuid'].delete(0, 'end')
            self.modules['uuid'].insert(0, link.get('uuid', ''))
            
            self.modules['address'].delete(0, 'end')
            self.modules['address'].insert(0, link.get('address', ''))
            
            self.modules['port'].delete(0, 'end')
            self.modules['port'].insert(0, link.get('port', ''))
            
            self.modules['sni'].delete(0, 'end')
            self.modules['sni'].insert(0, link.get('sni', ''))
            
            self.modules['host'].delete(0, 'end')
            self.modules['host'].insert(0, link.get('host', ''))
            
            self.modules['path'].delete(0, 'end')
            self.modules['path'].insert(0, link.get('path', ''))
            
            self.modules['security'].set(link.get('security', 'tls'))
            self.modules['fp'].set(link.get('fp', 'chrome'))
            self.modules['alpn'].delete(0, 'end')
            self.modules['alpn'].insert(0, link.get('alpn', 'h3,h2,http/1.1'))
            self.modules['type'].set(link.get('type_net', 'ws'))
            
            self.modules['proxyip'].delete(0, 'end')
            self.modules['proxyip'].insert(0, link.get('proxyip', ''))
            
            self.modules['name'].delete(0, 'end')
            self.modules['name'].insert(0, link.get('name', ''))
            
            self.update_preview()
            
    def update_preview(self):
        """更新预览"""
        link = self.generate_link_text()
        self.preview_text.delete('1.0', 'end')
        self.preview_text.insert('1.0', link)
        
    def generate_link(self):
        """生成链接"""
        link = self.generate_link_text()
        self.preview_text.delete('1.0', 'end')
        self.preview_text.insert('1.0', link)
        
        # 复制到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(link)
        self.status_var.set("✅ 链接已生成并复制到剪贴板！")
        messagebox.showinfo("成功", "链接已生成并复制到剪贴板！")
        
    def generate_link_text(self):
        """生成链接文本"""
        link_type = self.current_type.get()
        uuid = self.modules['uuid'].get().strip()
        address = self.modules['address'].get().strip()
        port = self.modules['port'].get().strip() or '443'
        sni = self.modules['sni'].get().strip()
        host = self.modules['host'].get().strip() or sni
        fp = self.modules['fp'].get()
        alpn = self.modules['alpn'].get().strip()
        security = self.modules['security'].get()
        type_net = self.modules['type'].get()
        proxyip = self.modules['proxyip'].get().strip()
        name = self.modules['name'].get().strip()
        
        if link_type == 'VLESS':
            # 构建path
            if proxyip:
                path = f"/proxyip={proxyip}"
            else:
                path = "/proxyip=placeholder"
            path_encoded = quote(path)
            
            params = [
                f"encryption=none",
                f"security={security}",
                f"sni={sni}" if sni else "",
                f"fp={fp}",
                f"alpn={quote(alpn)}",
                "insecure=1",
                "allowInsecure=1",
                f"type={type_net}",
                f"host={host}" if host else "",
                f"path={path_encoded}"
            ]
            params = [p for p in params if p]
            
            return f"vless://{uuid}@{address}:{port}?{'&'.join(params)}#{quote(name)}"
            
        else:  # Trojan
            if proxyip:
                path = f"/proxyip={proxyip}"
            else:
                path = "/proxyip=placeholder"
            path_encoded = quote(path)
            
            params = [
                f"security={security}",
                f"sni={sni}" if sni else "",
                f"fp={fp}",
                f"alpn={quote(alpn)}",
                "insecure=1",
                "allowInsecure=1",
                f"type={type_net}",
                f"host={host}" if host else "",
                f"path={path_encoded}"
            ]
            params = [p for p in params if p]
            
            return f"trojan://{uuid}@{address}:{port}?{'&'.join(params)}#{quote(name)}"
            
    def batch_replace_proxyip(self):
        """批量替换ProxyIP"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 批量替换 ProxyIP")
        dialog.geometry("400x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="原 ProxyIP:", font=("Microsoft YaHei", 10)).pack(pady=5)
        old_entry = tk.Entry(dialog, font=("Consolas", 11), width=40)
        old_entry.pack(pady=5)
        
        tk.Label(dialog, text="新 ProxyIP:", font=("Microsoft YaHei", 10)).pack(pady=5)
        new_entry = tk.Entry(dialog, font=("Consolas", 11), width=40)
        new_entry.pack(pady=5)
        
        def do_replace():
            old = old_entry.get().strip()
            new = new_entry.get().strip()
            if not old:
                messagebox.showwarning("提示", "请输入原 ProxyIP！")
                return
                
            # 更新所有链接
            for link in self.current_links:
                if link.get('proxyip') == old:
                    link['proxyip'] = new
                    # 更新path
                    if 'path' in link:
                        link['path'] = re.sub(r'proxyip=[^&]+', f'proxyip={new}', link['path'])
            
            self.display_link(0)
            dialog.destroy()
            self.status_var.set(f"✅ 已将 {len(self.current_links)} 条链接的 ProxyIP 从 [{old}] 改为 [{new}]")
            messagebox.showinfo("完成", f"已替换 {len(self.current_links)} 条链接！")
        
        tk.Button(dialog, text="确认替换", command=do_replace,
                 font=("Microsoft YaHei", 10, "bold"), bg='#28a745', fg='white').pack(pady=15)
        
    def batch_change_port(self):
        """批量修改端口"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 批量修改端口")
        dialog.geometry("400x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="新端口:", font=("Microsoft YaHei", 10)).pack(pady=5)
        port_entry = tk.Entry(dialog, font=("Consolas", 11), width=40)
        port_entry.insert(0, "443")
        port_entry.pack(pady=5)
        
        tk.Label(dialog, text="（留空则保持原端口不变）", font=("Microsoft YaHei", 9), fg='#888888').pack()
        
        def do_change():
            new_port = port_entry.get().strip()
            if not new_port:
                dialog.destroy()
                return
                
            for link in self.current_links:
                link['port'] = new_port
            
            self.display_link(0)
            dialog.destroy()
            self.status_var.set(f"✅ 已将所有链接端口改为 [{new_port}]")
            messagebox.showinfo("完成", f"已修改 {len(self.current_links)} 条链接的端口！")
        
        tk.Button(dialog, text="确认修改", command=do_change,
                 font=("Microsoft YaHei", 10, "bold"), bg='#6610f2', fg='white').pack(pady=15)
        
    def batch_change_name(self):
        """批量修改名称"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 批量修改显示名称")
        dialog.geometry("500x220")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="新名称（支持变量）:", font=("Microsoft YaHei", 10)).pack(pady=5)
        tk.Label(dialog, text="可用: {index}（序号）, {ip}（IP）, {port}（端口）, {date}（日期）", 
                font=("Microsoft YaHei", 9), fg='#888888').pack()
        name_entry = tk.Entry(dialog, font=("Microsoft YaHei", 11), width=45)
        name_entry.insert(0, "{index}号节点")
        name_entry.pack(pady=5)
        
        def do_change():
            template = name_entry.get().strip()
            if not template:
                return
                
            import datetime
            for i, link in enumerate(self.current_links, 1):
                name = template
                name = name.replace('{index}', str(i))
                name = name.replace('{ip}', link.get('address', ''))
                name = name.replace('{port}', link.get('port', ''))
                name = name.replace('{date}', datetime.datetime.now().strftime('%Y%m%d'))
                link['name'] = name
            
            self.display_link(0)
            dialog.destroy()
            self.status_var.set(f"✅ 已批量修改 {len(self.current_links)} 条链接名称")
            messagebox.showinfo("完成", "名称已批量修改！")
        
        tk.Button(dialog, text="确认修改", command=do_change,
                 font=("Microsoft YaHei", 10, "bold"), bg='#fd7e14', fg='white').pack(pady=15)
        
    def batch_change_sni(self):
        """批量修改SNI"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔄 批量修改 SNI")
        dialog.geometry("450x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="新 SNI:", font=("Microsoft YaHei", 10)).pack(pady=5)
        sni_entry = tk.Entry(dialog, font=("Consolas", 11), width=40)
        sni_entry.insert(0, "laowang.19960102.xyz")
        sni_entry.pack(pady=5)
        
        tk.Label(dialog, text="常用选项:", font=("Microsoft YaHei", 9)).pack(pady=5)
        sni_frame = tk.Frame(dialog, bg='#f0f0f0')
        sni_frame.pack(pady=5)
        
        sni_options = [
            "laowang.19960102.xyz",
            "joeyhuang.19960102.xyz", 
            "trojancm.19960102.xyz"
        ]
        
        for opt in sni_options:
            tk.Button(sni_frame, text=opt, command=lambda o=opt: sni_entry.delete(0,'end') or sni_entry.insert(0,o),
                     font=("Microsoft YaHei", 8), bg='#e0e0e0').pack(side='left', padx=3)
        
        def do_change():
            new_sni = sni_entry.get().strip()
            if not new_sni:
                return
                
            for link in self.current_links:
                link['sni'] = new_sni
                link['host'] = new_sni
            
            self.display_link(0)
            dialog.destroy()
            self.status_var.set(f"✅ 已将所有链接 SNI 改为 [{new_sni}]")
            messagebox.showinfo("完成", f"已修改 {len(self.current_links)} 条链接的 SNI！")
        
        tk.Button(dialog, text="确认修改", command=do_change,
                 font=("Microsoft YaHei", 10, "bold"), bg='#20c997', fg='white').pack(pady=15)
        
    def clear_all(self):
        """清空所有"""
        self.input_text.delete('1.0', 'end')
        self.current_links = []
        for key in self.modules:
            if hasattr(self.modules[key], 'delete'):
                self.modules[key].delete(0, 'end')
        self.preview_text.delete('1.0', 'end')
        self.status_var.set("就绪 | 已清空")
        
    def import_file(self):
        """导入文件"""
        file_path = filedialog.askopenfilename(
            title="选择链接文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete('1.0', 'end')
                self.input_text.insert('1.0', content)
                self.status_var.set(f"📂 已导入文件: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}")
                
    def export_file(self):
        """导出文件"""
        link = self.preview_text.get('1.0', 'end').strip()
        if not link:
            messagebox.showwarning("提示", "没有可导出的链接！")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="保存链接文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile="vless_links.txt"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(link)
                self.status_var.set(f"💾 已导出到: {os.path.basename(file_path)}")
                messagebox.showinfo("成功", f"已导出到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")

def main():
    root = tk.Tk()
    app = VlessTrojanTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
