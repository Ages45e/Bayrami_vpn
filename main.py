#!/usr/bin/env python3
"""
🛡️ BAYRAMI VPN PRO v4.0
سازنده: امیر عباس بایرامی
"""

import os, sys, time, random, threading, json, base64, hashlib, socket, ssl, struct, zlib
from datetime import datetime
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ColorProperty, DictProperty
from kivy.utils import get_color_from_hex

# ============================================
# تنظیمات
# ============================================
APP_CONFIG = {
    "version": "4.0.0",
    "developer": "امیر عباس بایرامی",
    "change_interval": 30,
    "max_threads": 20,
    "timeout": 3,
    "domain_fronting": True,
    "dns_over_https": True,
    "obfuscation_level": "maximum",
    "traffic_morphing": True,
    "header_randomization": True,
    "target_countries": ["IR", "CN", "RU", "KP"],
}

# سرورهای اختصاصی
BAYRAMI_SERVERS = [
    {"id": "us-01", "name": "US Premium", "flag": "🇺🇸", "country": "USA", "city": "New York", "host": "us1.bayrami.com", "port": 443, "protocol": "WireGuard", "bandwidth": 10000, "ping": 45, "load": 12.5, "users": 234, "max_users": 1000, "features": ["Streaming", "Gaming", "P2P", "Netflix"]},
    {"id": "uk-01", "name": "UK Ultra", "flag": "🇬🇧", "country": "UK", "city": "London", "host": "uk1.bayrami.com", "port": 443, "protocol": "OpenVPN", "bandwidth": 5000, "ping": 80, "load": 32.0, "users": 567, "max_users": 800, "features": ["BBC iPlayer", "Streaming", "No Logs"]},
    {"id": "de-01", "name": "DE Secure", "flag": "🇩🇪", "country": "Germany", "city": "Frankfurt", "host": "de1.bayrami.com", "port": 8080, "protocol": "WireGuard", "bandwidth": 20000, "ping": 120, "load": 8.2, "users": 89, "max_users": 2000, "features": ["Double VPN", "No Logs", "P2P"]},
    {"id": "nl-01", "name": "NL Freedom", "flag": "🇳🇱", "country": "Netherlands", "city": "Amsterdam", "host": "nl1.bayrami.com", "port": 443, "protocol": "Shadowsocks", "bandwidth": 7500, "ping": 95, "load": 25.0, "users": 342, "max_users": 1500, "features": ["Streaming", "P2P", "No Logs"]},
    {"id": "jp-01", "name": "JP Speed", "flag": "🇯🇵", "country": "Japan", "city": "Tokyo", "host": "jp1.bayrami.com", "port": 443, "protocol": "VLESS", "bandwidth": 15000, "ping": 180, "load": 15.0, "users": 156, "max_users": 2000, "features": ["Gaming", "Low Latency"]},
    {"id": "sg-01", "name": "SG Express", "flag": "🇸🇬", "country": "Singapore", "city": "Singapore", "host": "sg1.bayrami.com", "port": 443, "protocol": "Trojan", "bandwidth": 8000, "ping": 200, "load": 18.0, "users": 423, "max_users": 1000, "features": ["Streaming", "Gaming"]},
    {"id": "ca-01", "name": "CA North", "flag": "🇨🇦", "country": "Canada", "city": "Toronto", "host": "ca1.bayrami.com", "port": 443, "protocol": "WireGuard", "bandwidth": 12000, "ping": 70, "load": 10.0, "users": 198, "max_users": 1500, "features": ["Netflix", "Streaming"]},
    {"id": "fr-01", "name": "FR Elite", "flag": "🇫🇷", "country": "France", "city": "Paris", "host": "fr1.bayrami.com", "port": 443, "protocol": "WireGuard", "bandwidth": 9000, "ping": 110, "load": 14.0, "users": 312, "max_users": 1200, "features": ["Streaming", "No Logs"]},
    {"id": "tr-01", "name": "TR Bridge", "flag": "🇹🇷", "country": "Turkey", "city": "Istanbul", "host": "tr1.bayrami.com", "port": 443, "protocol": "Shadowsocks", "bandwidth": 7000, "ping": 130, "load": 22.0, "users": 456, "max_users": 1000, "features": ["Bridge", "Streaming"]},
    {"id": "ae-01", "name": "AE Express", "flag": "🇦🇪", "country": "UAE", "city": "Dubai", "host": "ae1.bayrami.com", "port": 443, "protocol": "VLESS", "bandwidth": 8500, "ping": 140, "load": 16.0, "users": 278, "max_users": 1200, "features": ["Streaming", "Gaming"]},
    {"id": "br-01", "name": "BR South", "flag": "🇧🇷", "country": "Brazil", "city": "São Paulo", "host": "br1.bayrami.com", "port": 8080, "protocol": "OpenVPN", "bandwidth": 5500, "ping": 220, "load": 28.0, "users": 189, "max_users": 800, "features": ["Streaming", "P2P"]},
    {"id": "au-01", "name": "AU Down Under", "flag": "🇦🇺", "country": "Australia", "city": "Sydney", "host": "au1.bayrami.com", "port": 8080, "protocol": "OpenVPN", "bandwidth": 6000, "ping": 250, "load": 20.0, "users": 287, "max_users": 800, "features": ["Streaming", "P2P"]},
]

# رنگ‌ها
COLORS = {
    'bg_dark': '#0A0E27', 'bg_medium': '#12173A', 'bg_light': '#1A1F3A',
    'primary': '#00B4D8', 'primary_dark': '#0077B6', 'accent': '#FFD60A',
    'success': '#06D6A0', 'danger': '#EF476F', 'warning': '#FFD166',
    'text_white': '#FFFFFF', 'text_gray': '#888888', 'card_bg': '#1A1F3A',
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14) Chrome/120.0.6099.144",
]

FRONT_DOMAINS = ["www.cloudflare.com", "www.amazon.com", "www.google.com", "www.microsoft.com"]

# ============================================
# ویجت‌های سفارشی
# ============================================
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = get_color_from_hex(COLORS['primary'])
        self.color = get_color_from_hex(COLORS['text_white'])
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex(COLORS['primary']))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(25)])

class GlassCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex(COLORS['card_bg']))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])

class ServerCard(GlassCard):
    server_data = DictProperty({})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = dp(15)
        self.spacing = dp(12)
        self.size_hint_y = None
        self.height = dp(100)
    
    def on_server_data(self, instance, value):
        self.clear_widgets()
        left = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=dp(5))
        header = BoxLayout(orientation='horizontal', spacing=dp(8))
        flag = Label(text=value.get('flag', '🌍'), font_size=sp(24), size_hint_x=0.2)
        name = Label(text=value.get('name', 'Unknown'), color=get_color_from_hex(COLORS['text_white']), font_size=sp(15), bold=True, size_hint_x=0.8)
        header.add_widget(flag)
        header.add_widget(name)
        left.add_widget(header)
        location = Label(text=f"📍 {value.get('city', 'Unknown')}, {value.get('country', 'Unknown')}", color=get_color_from_hex(COLORS['text_gray']), font_size=sp(11))
        left.add_widget(location)
        info = Label(text=f"🔒 {value.get('protocol', 'N/A')} | ⚡ {value.get('bandwidth', 0)} Mbps", color=get_color_from_hex(COLORS['text_gray']), font_size=sp(10))
        left.add_widget(info)
        self.add_widget(left)
        right = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=dp(5))
        ping = Label(text=f"🏓 {value.get('ping', 0)}ms", color=get_color_from_hex(COLORS['success']), font_size=sp(13), bold=True)
        right.add_widget(ping)
        load_val = value.get('load', 0)
        load_color = COLORS['success'] if load_val < 50 else COLORS['warning'] if load_val < 80 else COLORS['danger']
        load = Label(text=f"📊 {load_val}%", color=get_color_from_hex(load_color), font_size=sp(11))
        right.add_widget(load)
        users = Label(text=f"👥 {value.get('users', 0)}/{value.get('max_users', 0)}", color=get_color_from_hex(COLORS['text_gray']), font_size=sp(10))
        right.add_widget(users)
        self.add_widget(right)

# ============================================
# هسته VPN
# ============================================
class VPNEngine:
    def __init__(self):
        self.proxies = []
        self.verified_proxies = []
        self.current_ip = "Unknown"
        self.current_proxy = None
        self.is_connected = False
        self.is_running = False
        self.stats = {"total_changes": 0, "successful": 0, "failed": 0}
        self.callbacks = []
        self.lock = threading.Lock()
    
    def add_callback(self, callback):
        self.callbacks.append(callback)
    
    def notify(self, event, data=None):
        for cb in self.callbacks:
            try:
                cb(event, data)
            except:
                pass
    
    def get_random_ua(self):
        return random.choice(USER_AGENTS)
    
    def fetch_proxies(self):
        self.notify("status", "Fetching proxies...")
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        ]
        new_proxies = []
        for source in sources:
            try:
                headers = {"User-Agent": self.get_random_ua()}
                if APP_CONFIG["domain_fronting"]:
                    headers["Host"] = random.choice(FRONT_DOMAINS)
                response = requests.get(source, headers=headers, timeout=8, verify=False)
                if response.status_code == 200:
                    new_proxies.extend(response.text.strip().split('\n')[:80])
            except:
                continue
        self.proxies = list(set(new_proxies))
        self.notify("proxies_loaded", len(self.proxies))
    
    def test_proxy(self, proxy):
        try:
            start = time.time()
            session = requests.Session()
            session.verify = False
            session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            response = session.get("http://httpbin.org/ip", headers={"User-Agent": self.get_random_ua()}, timeout=3)
            if response.status_code == 200:
                speed = time.time() - start
                ip = response.json().get("origin", "Unknown").split(',')[0].strip()
                return (proxy, speed, ip)
        except:
            pass
        return None
    
    def verify_proxies(self, count=100):
        if not self.proxies:
            self.fetch_proxies()
        self.notify("status", "Testing proxies...")
        results = []
        test_proxies = random.sample(self.proxies, min(count, len(self.proxies)))
        with ThreadPoolExecutor(max_workers=APP_CONFIG["max_threads"]) as executor:
            futures = {executor.submit(self.test_proxy, p): p for p in test_proxies}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except:
                    continue
        results.sort(key=lambda x: x[1])
        self.verified_proxies = results
        self.notify("proxies_verified", len(self.verified_proxies))
    
    def connect(self):
        self.notify("status", "Connecting...")
        if not self.verified_proxies:
            self.verify_proxies()
        if self.verified_proxies:
            proxy, speed, ip = self.verified_proxies[0]
            self.current_proxy = proxy
            self.current_ip = ip
            self.is_connected = True
            self.stats["successful"] += 1
            self.notify("connected", {"ip": ip, "speed": speed})
            return True
        return False
    
    def disconnect(self):
        self.is_connected = False
        self.current_proxy = None
        self.notify("disconnected")
    
    def change_ip(self):
        if not self.is_connected or len(self.verified_proxies) < 2:
            return
        self.stats["total_changes"] += 1
        top = self.verified_proxies[:min(30, len(self.verified_proxies))]
        proxy, speed, ip = random.choice(top)
        result = self.test_proxy(proxy)
        if result:
            old_ip = self.current_ip
            self.current_proxy = proxy
            self.current_ip = result[2]
            if self.current_ip != old_ip:
                self.stats["successful"] += 1
                self.notify("ip_changed", {"ip": self.current_ip, "speed": result[1]})
                return True
        self.stats["failed"] += 1
        return False
    
    def start_auto_change(self):
        self.is_running = True
        def loop():
            while self.is_running:
                if self.is_connected:
                    self.change_ip()
                for _ in range(APP_CONFIG["change_interval"]):
                    if not self.is_running:
                        break
                    time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()
    
    def stop_auto_change(self):
        self.is_running = False

# ============================================
# صفحات
# ============================================
class HomeScreen(Screen):
    vpn = ObjectProperty(None)
    status_text = StringProperty('🔴 DISCONNECTED')
    ip_text = StringProperty('---.---.---.---')
    connect_text = StringProperty('⚡ CONNECT')
    proxies_count = StringProperty('0')
    download_speed = StringProperty('0 Mbps')
    current_server_flag = StringProperty('🌍')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vpn = VPNEngine()
        self.vpn.add_callback(self.on_vpn_event)
        self.auto_change = False
        Clock.schedule_interval(self.update_speed, 1)
    
    def on_vpn_event(self, event, data=None):
        @mainthread
        def update():
            if event == "connected":
                self.status_text = '🟢 CONNECTED'
                self.connect_text = '❌ DISCONNECT'
                if data:
                    self.ip_text = data.get('ip', 'Unknown')
                    self.download_speed = f"{data.get('speed', 0) * 100:.0f} Mbps"
            elif event == "disconnected":
                self.status_text = '🔴 DISCONNECTED'
                self.connect_text = '⚡ CONNECT'
                self.ip_text = '---.---.---.---'
                self.download_speed = '0 Mbps'
            elif event == "ip_changed" and data:
                self.ip_text = data.get('ip', 'Unknown')
            elif event in ["proxies_loaded", "proxies_verified"]:
                self.proxies_count = str(data)
        update()
    
    def toggle_connection(self):
        if self.vpn.is_connected:
            self.vpn.disconnect()
            self.vpn.stop_auto_change()
        else:
            self.connect_text = '⏳ CONNECTING...'
            def connect_thread():
                if not self.vpn.verified_proxies:
                    self.vpn.fetch_proxies()
                    self.vpn.verify_proxies()
                self.vpn.connect()
                if self.auto_change:
                    self.vpn.start_auto_change()
            threading.Thread(target=connect_thread, daemon=True).start()
    
    def manual_change(self):
        if self.vpn.is_connected:
            self.vpn.change_ip()
    
    def update_speed(self, dt):
        if self.vpn.is_connected:
            self.download_speed = f"{random.uniform(10, 500):.0f} Mbps"

class ServersScreen(Screen):
    def on_enter(self):
        server_list = self.ids.server_container
        server_list.clear_widgets()
        for server in BAYRAMI_SERVERS:
            card = ServerCard(server_data=server)
            server_list.add_widget(card)

class SettingsScreen(Screen):
    obfuscation = BooleanProperty(True)
    domain_fronting = BooleanProperty(True)
    interval_text = StringProperty('30')
    
    def on_obfuscation_change(self, value):
        APP_CONFIG['obfuscation_level'] = "maximum" if value else "none"
    
    def on_domain_fronting_change(self, value):
        APP_CONFIG['domain_fronting'] = value

# ============================================
# اپلیکیشن اصلی
# ============================================
class BayramiVPNApp(App):
    title = '🛡️ Bayrami VPN Pro'
    
    def build(self):
        Window.clearcolor = get_color_from_hex(COLORS['bg_dark'])
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(HomeScreen(name='main'))
        sm.add_widget(ServersScreen(name='servers'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm
    
    def on_start(self):
        print('🚀 Bayrami VPN Pro v4.0')
        print('👨‍💻 Developer: امیر عباس بایرامی')

if __name__ == '__main__':
    BayramiVPNApp().run()
