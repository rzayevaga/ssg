#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==================================================
🌐 SESSION GENERATOR v2.0
🔧 Created by Rzayeffdi / Ağa
==================================================
"""

import asyncio
import os
import sys
import platform
import subprocess
import importlib
import time
from typing import Optional, Tuple
import getpass

# Import checks with enhanced error handling
try:
    from pyrogram import Client as PyroClient, __version__ as pyro_version
    from pyrogram.errors import (
        SessionPasswordNeeded, ApiIdInvalid, PhoneCodeInvalid, 
        PhoneCodeExpired, PhoneNumberInvalid, PhoneNumberUnoccupied,
        BadRequest
    )
except ImportError:
    pyro_available = False
else:
    pyro_available = True

try:
    from telethon import TelegramClient as TeleClient, __version__ as tele_version
    from telethon.sessions import StringSession as TeleString
    from telethon.errors import (
        ApiIdInvalidError, PhoneNumberInvalidError, 
        PhoneCodeInvalidError, PhoneCodeExpiredError,
        SessionPasswordNeededError, FloodWaitError
    )
except ImportError:
    telethon_available = False
else:
    telethon_available = True

# Color codes for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# System detection
class SystemDetector:
    @staticmethod
    def detect_environment():
        system = platform.system().lower()
        if 'termux' in os.environ.get('PREFIX', ''):
            return 'termux'
        elif system == 'linux':
            if 'kali' in platform.release().lower():
                return 'kali'
            elif 'ubuntu' in platform.version().lower():
                return 'ubuntu'
            else:
                return 'linux'
        elif system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'macos'
        else:
            return 'unknown'
    
    @staticmethod
    def get_install_command(package_manager):
        commands = {
            'termux': 'pkg install',
            'ubuntu': 'sudo apt-get install',
            'kali': 'sudo apt-get install', 
            'linux': 'sudo apt-get install',
            'macos': 'brew install'
        }
        return commands.get(package_manager, 'pip install')

# Enhanced requirements management
class RequirementsManager:
    def __init__(self):
        self.environment = SystemDetector.detect_environment()
        self.required_packages = {
            'pyrogram': {
                'package': 'pyrogram',
                'min_version': '2.0.0',
                'install_cmd': 'pip install pyrogram tgcrypto'
            },
            'telethon': {
                'package': 'telethon', 
                'min_version': '1.24.0',
                'install_cmd': 'pip install telethon'
            }
        }
    
    def check_package(self, package_name):
        try:
            module = importlib.import_module(package_name)
            if package_name == 'pyrogram':
                current_version = pyro_version
            elif package_name == 'telethon':
                current_version = tele_version
            else:
                current_version = getattr(module, '__version__', '0.0.0')
            
            min_version = self.required_packages[package_name]['min_version']
            return self.compare_versions(current_version, min_version)
        except ImportError:
            return False, "0.0.0"
    
    def compare_versions(self, current, minimum):
        current_parts = list(map(int, current.split('.')))
        min_parts = list(map(int, minimum.split('.')))
        return current_parts >= min_parts, current
    
    def install_package(self, package_name):
        package_info = self.required_packages[package_name]
        print(f"\n{Colors.YELLOW}📦 {package_name} paketi yükleniyor...{Colors.END}")
        
        try:
            if self.environment == 'termux':
                # Termux için özel kurulum
                subprocess.run(f"pkg install python -y", shell=True, check=True)
            
            result = subprocess.run(
                f"{package_info['install_cmd']} --upgrade",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ {package_name} başarıyla yüklendi!{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}❌ {package_name} yüklenemedi: {result.stderr}{Colors.END}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ Kurulum hatası: {e}{Colors.END}")
            return False
    
    def check_and_install_all(self):
        print(f"\n{Colors.CYAN}🔍 Gerekli paketler kontrol ediliyor...{Colors.END}")
        
        for package_name, info in self.required_packages.items():
            is_ok, version = self.check_package(package_name)
            
            if is_ok:
                print(f"{Colors.GREEN}✅ {package_name} {version} - OK{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️ {package_name} bulunamadı veya güncel değil ({version}){Colors.END}")
                choice = input(f"{Colors.CYAN}📥 {package_name} yüklemek istiyor musunuz? (e/h): {Colors.END}").lower()
                
                if choice in ['e', 'y', 'yes', 'evet']:
                    if self.install_package(package_name):
                        # Yükleme sonrası tekrar kontrol
                        is_ok, new_version = self.check_package(package_name)
                        if is_ok:
                            print(f"{Colors.GREEN}✅ {package_name} {new_version} başarıyla yüklendi!{Colors.END}")
                        else:
                            print(f"{Colors.RED}❌ {package_name} hala yüklü değil!{Colors.END}")
                            return False
                    else:
                        return False
                else:
                    print(f"{Colors.YELLOW}⚠️ {package_name} olmadan bazı özellikler çalışmayabilir.{Colors.END}")
        
        return True

# Enhanced session generator with better error handling
class PremiumSessionGenerator:
    def __init__(self):
        self.requirements = RequirementsManager()
        self.setup_directories()
    
    def setup_directories(self):
        """Gerekli dizinleri oluştur"""
        directories = ['sessions', 'legacy_sessions', 'logs', 'backups']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """Premium banner göster"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🌐 UNIVERSAL PREMIUM SESSION GENERATOR v2.0                ║
║  🔧 Created by: Rzayeffdi / Ağa                             ║
║  🚀 Enhanced with Advanced Features                         ║
║                                                              ║
║  📊 System: {platform.system()} {platform.release()}{' '*(30-len(platform.system()+platform.release()))}║
║  🐍 Python: {platform.python_version()}{' '*(38-len(platform.python_version()))}║
║  🌍 Environment: {self.requirements.environment}{' '*(30-len(self.requirements.environment))}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    async def get_credentials(self, bot: bool = False) -> Tuple[str, str, Optional[str]]:
        """Kullanıcıdan kimlik bilgilerini al"""
        print(f"\n{Colors.CYAN}🔐 Kimlik bilgilerini girin:{Colors.END}")
        
        while True:
            api_id = input(f"{Colors.BLUE}🔹 API_ID: {Colors.END}").strip()
            if api_id.isdigit() and len(api_id) >= 5:
                break
            print(f"{Colors.RED}❌ Geçersiz API_ID! Lütfen sayılardan oluşan geçerli bir API_ID girin.{Colors.END}")
        
        api_hash = input(f"{Colors.BLUE}🔹 API_HASH: {Colors.END}").strip()
        if not api_hash:
            print(f"{Colors.RED}❌ API_HASH boş olamaz!{Colors.END}")
            return await self.get_credentials(bot)
        
        bot_token = None
        if bot:
            bot_token = input(f"{Colors.BLUE}🤖 Bot Token: {Colors.END}").strip()
            if not bot_token:
                print(f"{Colors.RED}❌ Bot Token boş olamaz!{Colors.END}")
                return await self.get_credentials(bot)
        
        return api_id, api_hash, bot_token
    
    async def create_pyrogram_session(self, version: str, bot: bool):
        """Gelişmiş Pyrogram session oluşturma"""
        print(f"\n{Colors.MAGENTA}🚀 Pyrogram ({version}) {'BOT' if bot else 'USER'} Session Oluşturuluyor...{Colors.END}")
        
        try:
            api_id, api_hash, bot_token = await self.get_credentials(bot)
            session_name = f"pyrogram_{version}_{'bot' if bot else 'user'}_{int(time.time())}"
            
            # Client konfigürasyonu
            client_config = {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "workdir": "./sessions" if version == "new" else "./legacy_sessions",
                "in_memory": False
            }
            
            if bot:
                client_config["bot_token"] = bot_token
            else:
                client_config["session_name"] = session_name
            
            client = PyroClient(**client_config)
            
            # Bağlantı ve giriş işlemleri
            await client.start()
            
            if not bot:
                # User session için telefon doğrulama
                await self.handle_user_authentication(client)
            
            # Session bilgilerini al
            me = await client.get_me()
            session_string = await client.export_session_string()
            
            # Sonuçları göster
            await self.show_session_results(client, me, session_string, "Pyrogram", version, bot)
            
            # Session'ı dosyaya kaydet
            await self.save_session_to_file(session_name, session_string, "pyrogram")
            
            await client.stop()
            
        except ApiIdInvalid:
            print(f"{Colors.RED}❌ Geçersiz API_ID veya API_HASH!{Colors.END}")
        except PhoneNumberInvalid:
            print(f"{Colors.RED}❌ Geçersiz telefon numarası!{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Beklenmeyen hata: {e}{Colors.END}")
    
    async def handle_user_authentication(self, client):
        """Kullanıcı doğrulama işlemleri"""
        phone_number = input(f"{Colors.BLUE}📞 Telefon Numarası (+994...): {Colors.END}").strip()
        
        sent_code = await client.send_code(phone_number)
        print(f"{Colors.YELLOW}📲 Doğrulama kodu gönderildi...{Colors.END}")
        
        while True:
            phone_code = input(f"{Colors.BLUE}🔐 SMS ile gelen kodu girin: {Colors.END}").strip()
            
            try:
                await client.sign_in(phone_number, sent_code.phone_code_hash, phone_code)
                break
            except PhoneCodeInvalid:
                print(f"{Colors.RED}❌ Yanlış kod! Tekrar deneyin.{Colors.END}")
            except PhoneCodeExpired:
                print(f"{Colors.RED}❌ Kodun süresi dolmuş! Yeniden kod istiyorum...{Colors.END}")
                sent_code = await client.resend_code(phone_number, sent_code.phone_code_hash)
            except SessionPasswordNeeded:
                print(f"{Colors.YELLOW}🔒 2FA etkin, şifre gerekiyor...{Colors.END}")
                password = getpass.getpass(f"{Colors.BLUE}🔑 2FA Şifresini girin: {Colors.END}")
                await client.check_password(password)
                break
    
    async def create_telethon_session(self, bot: bool):
        """Gelişmiş Telethon session oluşturma"""
        print(f"\n{Colors.MAGENTA}⚡ Telethon {'BOT' if bot else 'USER'} Session Oluşturuluyor...{Colors.END}")
        
        try:
            api_id, api_hash, bot_token = await self.get_credentials(bot)
            session_name = f"telethon_{'bot' if bot else 'user'}_{int(time.time())}"
            
            client = TeleClient(TeleString(), int(api_id), api_hash)
            
            if bot:
                await client.start(bot_token=bot_token)
            else:
                await client.start(phone=lambda: input(f"{Colors.BLUE}📞 Telefon Numarası (+994...): {Colors.END}").strip())
            
            me = await client.get_me()
            session_string = client.session.save()
            
            await self.show_session_results(client, me, session_string, "Telethon", "latest", bot)
            await self.save_session_to_file(session_name, session_string, "telethon")
            
            await client.disconnect()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Hata: {e}{Colors.END}")
    
    async def show_session_results(self, client, me, session_string, lib_name, version, bot):
        """Session sonuçlarını göster"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ {lib_name} Session Başarıyla Oluşturuldu!{Colors.END}")
        print(f"{Colors.CYAN}┌───────────────────────────────────────────────{Colors.END}")
        print(f"{Colors.CYAN}│ 👤 Ad: {me.first_name or me.username}{Colors.END}")
        print(f"{Colors.CYAN}│ 🆔 ID: {me.id}{Colors.END}")
        print(f"{Colors.CYAN}│ 📛 Kullanıcı Adı: @{me.username or 'Yok'}{Colors.END}")
        print(f"{Colors.CYAN}│ 🤖 Tür: {'Bot' if bot else 'User'}{Colors.END}")
        print(f"{Colors.CYAN}│ 📚 Kütüphane: {lib_name} {version}{Colors.END}")
        print(f"{Colors.CYAN}│ ⏰ Zaman: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────{Colors.END}")
        
        print(f"\n{Colors.YELLOW}📦 Session String:{Colors.END}")
        print(f"{Colors.WHITE}{session_string}{Colors.END}\n")
        
        # Saved Messages'a gönder
        try:
            await client.send_message(
                "me",
                f"""**✅ {lib_name} {'Bot' if bot else 'User'} Session Oluşturuldu!**

👤 **Ad:** `{me.first_name or me.username}`
🆔 **ID:** `{me.id}`
📛 **Kullanıcı Adı:** `@{me.username or 'Yok'}`
🤖 **Tür:** `{'Bot' if bot else 'User'}`
📚 **Versiyon:** `{lib_name} {version}`
⏰ **Zaman:** `{time.strftime('%Y-%m-%d %H:%M:%S')}`

`{session_string}`"""
            )
            print(f"{Colors.GREEN}💾 Session bilgileri Saved Messages'a gönderildi!{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ Saved Messages'a gönderilemedi: {e}{Colors.END}")
    
    async def save_session_to_file(self, session_name, session_string, lib_type):
        """Session'ı dosyaya kaydet"""
        filename = f"sessions/{session_name}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {lib_type.upper()} SESSION STRING\n")
                f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# DO NOT SHARE THIS WITH ANYONE!\n\n")
                f.write(session_string)
            
            print(f"{Colors.GREEN}💾 Session dosyaya kaydedildi: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Dosyaya yazma hatası: {e}{Colors.END}")
    
    async def show_session_manager(self):
        """Session yöneticisi"""
        print(f"\n{Colors.CYAN}📊 Session Yöneticisi{Colors.END}")
        
        if os.path.exists('sessions'):
            sessions = [f for f in os.listdir('sessions') if f.endswith('.txt')]
            if sessions:
                print(f"{Colors.GREEN}📁 Mevcut Sessionlar:{Colors.END}")
                for i, session in enumerate(sessions, 1):
                    print(f"  {i}. {session}")
            else:
                print(f"{Colors.YELLOW}📁 Henüz session dosyası bulunmamaktadır.{Colors.END}")
        else:
            print(f"{Colors.RED}📁 Sessions dizini bulunamadı.{Colors.END}")
    
    async def system_info(self):
        """Sistem bilgilerini göster"""
        print(f"\n{Colors.CYAN}🖥️  Sistem Bilgileri{Colors.END}")
        print(f"{Colors.WHITE}┌───────────────────────────────────────────────{Colors.END}")
        print(f"{Colors.WHITE}│ 🖥️  İşletim Sistemi: {platform.system()} {platform.release()}{Colors.END}")
        print(f"{Colors.WHITE}│ 🐍 Python Versiyonu: {platform.python_version()}{Colors.END}")
        print(f"{Colors.WHITE}│ 🏠 Ortam: {self.requirements.environment}{Colors.END}")
        print(f"{Colors.WHITE}│ 📁 Çalışma Dizini: {os.getcwd()}{Colors.END}")
        
        if pyro_available:
            print(f"{Colors.WHITE}│ 🔥 Pyrogram Versiyonu: {pyro_version}{Colors.END}")
        if telethon_available:
            print(f"{Colors.WHITE}│ ⚡ Telethon Versiyonu: {tele_version}{Colors.END}")
        
        print(f"{Colors.WHITE}└───────────────────────────────────────────────{Colors.END}")
    
    async def main_menu(self):
        """Ana menü"""
        while True:
            self.clear_screen()
            self.show_banner()
            
            menu = f"""
{Colors.CYAN}🎯 ANA MENÜ - Seçiminizi yapın:{Colors.END}

{Colors.GREEN}1️⃣  Pyrogram (Yeni Versiyon) User Session{Colors.END}
{Colors.GREEN}2️⃣  Pyrogram (Eski Versiyon) User Session{Colors.END}  
{Colors.GREEN}3️⃣  Pyrogram Bot Session{Colors.END}
{Colors.BLUE}4️⃣  Telethon User Session{Colors.END}
{Colors.BLUE}5️⃣  Telethon Bot Session{Colors.END}
{Colors.YELLOW}6️⃣  Session Yöneticisi{Colors.END}
{Colors.MAGENTA}7️⃣  Sistem Bilgileri{Colors.END}
{Colors.RED}0️⃣  Çıkış{Colors.END}

{Colors.CYAN}┌───────────────────────────────────────────────{Colors.END}
{Colors.CYAN}│ 💡 İpucu: Bot session için @BotFather'dan{Colors.END}
{Colors.CYAN}│ bot oluşturup API bilgilerini alın.{Colors.END}
{Colors.CYAN}└───────────────────────────────────────────────{Colors.END}
            """
            print(menu)
            
            choice = input(f"{Colors.BOLD}🔸 Seçiminiz (0-7): {Colors.END}").strip()
            
            if choice == "1":
                if pyro_available:
                    await self.create_pyrogram_session("new", False)
                else:
                    print(f"{Colors.RED}❌ Pyrogram kurulu değil!{Colors.END}")
            elif choice == "2":
                if pyro_available:
                    await self.create_pyrogram_session("old", False)
                else:
                    print(f"{Colors.RED}❌ Pyrogram kurulu değil!{Colors.END}")
            elif choice == "3":
                if pyro_available:
                    await self.create_pyrogram_session("new", True)
                else:
                    print(f"{Colors.RED}❌ Pyrogram kurulu değil!{Colors.END}")
            elif choice == "4":
                if telethon_available:
                    await self.create_telethon_session(False)
                else:
                    print(f"{Colors.RED}❌ Telethon kurulu değil!{Colors.END}")
            elif choice == "5":
                if telethon_available:
                    await self.create_telethon_session(True)
                else:
                    print(f"{Colors.RED}❌ Telethon kurulu değil!{Colors.END}")
            elif choice == "6":
                await self.show_session_manager()
            elif choice == "7":
                await self.system_info()
            elif choice == "0":
                print(f"\n{Colors.GREEN}👋 Görüşmek üzere!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.END}")
            
            if choice != "0":
                input(f"\n{Colors.CYAN}⏎ Devam etmek için Enter'a basın...{Colors.END}")

async def main():
    """Ana fonksiyon"""
    generator = PremiumSessionGenerator()
    
    # Gereksinimleri kontrol et
    if not generator.requirements.check_and_install_all():
        print(f"{Colors.RED}❌ Gerekli paketler yüklenemedi!{Colors.END}")
        return
    
    # Ana menüyü başlat
    try:
        await generator.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Program kullanıcı tarafından durduruldu.{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Beklenmeyen hata: {e}{Colors.END}")

if __name__ == "__main__":
    # Python versiyon kontrolü
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 veya üstü gereklidir!")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Program sonlandırıldı.{Colors.END}")
