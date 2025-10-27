#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
==================================================
🌐  SESSION GENERATOR v2.0
🔧 Yaradan: Rzayeffdi / Ağa
✨ Premium Ultra Edition with Enhanced Features
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

# Global variables for package availability
pyro_available = False
telethon_available = False
pyro_version = "0.0.0"
tele_version = "0.0.0"

# Import checks with enhanced error handling
try:
    from pyrogram import Client as PyroClient
    from pyrogram import __version__ as pyro_version
    from pyrogram.errors import (
        SessionPasswordNeeded, ApiIdInvalid, PhoneCodeInvalid, 
        PhoneCodeExpired, PhoneNumberInvalid, PhoneNumberUnoccupied,
        BadRequest
    )
    pyro_available = True
except ImportError:
    pyro_available = False

try:
    from telethon import TelegramClient as TeleClient
    from telethon import __version__ as tele_version
    from telethon.sessions import StringSession as TeleString
    from telethon.errors import (
        ApiIdInvalidError, PhoneNumberInvalidError, 
        PhoneCodeInvalidError, PhoneCodeExpiredError,
        SessionPasswordNeededError, FloodWaitError
    )
    telethon_available = True
except ImportError:
    telethon_available = False

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
        """Paketin mövcud olub-olmadığını və versiya tələblərinə cavab verib-vermədiyini yoxlayın"""
        try:
            if package_name == 'pyrogram':
                if not pyro_available:
                    return False, "0.0.0"
                current_version = pyro_version
            elif package_name == 'telethon':
                if not telethon_available:
                    return False, "0.0.0"
                current_version = tele_version
            else:
                # Digər paketlər üçün importlib istifadə edin
                module = importlib.import_module(package_name)
                current_version = getattr(module, '__version__', '0.0.0')
            
            min_version = self.required_packages[package_name]['min_version']
            return self.compare_versions(current_version, min_version), current_version
        except ImportError:
            return False, "0.0.0"
    
    def compare_versions(self, current, minimum):
        """Versiya sətirlərini müqayisə edin"""
        try:
            current_parts = list(map(int, current.split('.')))
            min_parts = list(map(int, minimum.split('.')))
            
            # Uzunluqlar uyğun gəlmirsə, sıfırlarla doldurun
            max_len = max(len(current_parts), len(min_parts))
            current_parts += [0] * (max_len - len(current_parts))
            min_parts += [0] * (max_len - len(min_parts))
            
            return current_parts >= min_parts
        except (ValueError, AttributeError):
            return False
    
    def install_package(self, package_name):
        """Paketi uyğun səhv idarəsi ilə quraşdırın"""
        package_info = self.required_packages[package_name]
        print(f"\n{Colors.YELLOW}📦 {package_name} paketi yüklənir...{Colors.END}")
        
        try:
            # Termux üçün Python-un quraşdırıldığından əmin olun
            if self.environment == 'termux':
                print(f"{Colors.CYAN}🔄 Termux mühiti aşkar edildi, zəruri paketlər yoxlanılır...{Colors.END}")
                try:
                    subprocess.run("pkg update -y", shell=True, check=True, capture_output=True)
                    subprocess.run("pkg install python -y", shell=True, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    print(f"{Colors.YELLOW}⚠️ Sistem paketləri yenilənə bilmədi, pip ilə davam edilir...{Colors.END}")
            
            # Pip istifadə edərək quraşdırın
            print(f"{Colors.CYAN}🔧 Pip ilə {package_name} yüklənir...{Colors.END}")
            result = subprocess.run(
                f"{package_info['install_cmd']} --upgrade",
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 dəqiqəlik zaman aşımı
            )
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ {package_name} uğurla yükləndi!{Colors.END}")
                
                # Quraşdırmadan sonra modulları yenidən yükləyin
                self._reload_modules()
                return True
            else:
                print(f"{Colors.RED}❌ {package_name} yüklənə bilmədi!{Colors.END}")
                print(f"{Colors.YELLOW}📋 Xəta təfərrüatı: {result.stderr}{Colors.END}")
                
                # Alternativ quraşdırma metodunu sınayın
                print(f"{Colors.CYAN}🔄 Alternativ quraşdırma metodu sınanılır...{Colors.END}")
                try:
                    subprocess.run(
                        f"pip install {package_name} --upgrade --force-reinstall",
                        shell=True,
                        check=True,
                        capture_output=True,
                        timeout=300
                    )
                    print(f"{Colors.GREEN}✅ {package_name} alternativ üsulla yükləndi!{Colors.END}")
                    self._reload_modules()
                    return True
                except subprocess.CalledProcessError:
                    print(f"{Colors.RED}❌ Alternativ metod da uğursuz oldu!{Colors.END}")
                    return False
                
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}❌ Quraşdırma zaman aşımına uğradı!{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ Gözlənilməz quraşdırma xətası: {e}{Colors.END}")
            return False
    
    def _reload_modules(self):
        """Quraşdırmadan sonra modulları yenidən yükləyin"""
        global pyro_available, telethon_available, pyro_version, tele_version
        
        print(f"{Colors.CYAN}🔄 Modullar yenidən yüklənir...{Colors.END}")
        
        # Pyrogram-ı yenidən yükləyin
        try:
            if 'pyrogram' in sys.modules:
                importlib.reload(sys.modules['pyrogram'])
            from pyrogram import Client as PyroClient
            from pyrogram import __version__ as pyro_version
            pyro_available = True
            print(f"{Colors.GREEN}✅ Pyrogram {pyro_version} yenidən yükləndi{Colors.END}")
        except ImportError:
            pyro_available = False
            print(f"{Colors.RED}❌ Pyrogram yenidən yüklənə bilmədi{Colors.END}")
        
        # Telethon-u yenidən yükləyin
        try:
            if 'telethon' in sys.modules:
                importlib.reload(sys.modules['telethon'])
            from telethon import TelegramClient as TeleClient
            from telethon import __version__ as tele_version
            from telethon.sessions import StringSession as TeleString
            telethon_available = True
            print(f"{Colors.GREEN}✅ Telethon {tele_version} yenidən yükləndi{Colors.END}")
        except ImportError:
            telethon_available = False
            print(f"{Colors.RED}❌ Telethon yenidən yüklənə bilmədi{Colors.END}")
    
    def check_and_install_all(self):
        """Bütün tələb olunan paketləri yoxlayın və quraşdırın"""
        print(f"\n{Colors.CYAN}🔍 Zəruri paketlər yoxlanılır...{Colors.END}")
        print(f"{Colors.CYAN}🌍 Aşkar edilən mühit: {self.environment}{Colors.END}")
        
        packages_to_check = list(self.required_packages.keys())
        installation_successful = True
        
        for package_name in packages_to_check:
            is_ok, version = self.check_package(package_name)
            
            if is_ok:
                print(f"{Colors.GREEN}✅ {package_name} {version} - OK{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️ {package_name} tapılmadı və ya aktuallaşdırılmadı ({version}){Colors.END}")
                choice = input(f"{Colors.CYAN}📥 {package_name} yükləmək istəyirsiniz? (e/h): {Colors.END}").lower().strip()
                
                if choice in ['e', 'h' 'y', 'yes', 'he', 'evet', 'yox']:
                    if self.install_package(package_name):
                        # Quraşdırmadan sonra quraşdırmaları yoxlayın
                        is_ok_after, new_version = self.check_package(package_name)
                        if is_ok_after:
                            print(f"{Colors.GREEN}✅ {package_name} {new_version} uğurla yükləndi!{Colors.END}")
                        else:
                            print(f"{Colors.RED}❌ {package_name} yükləndikdən sonra hələ də işləmir!{Colors.END}")
                            installation_successful = False
                    else:
                        installation_successful = False
                        print(f"{Colors.YELLOW}⚠️ {package_name} olmadan bəzi xüsusiyyətlər işləməyə bilər.{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}⚠️ {package_name} atlandı, bəzi xüsusiyyətlər işləməyə bilər.{Colors.END}")
        
        return installation_successful

# Enhanced session generator with better error handling
class PremiumSessionGenerator:
    def __init__(self):
        self.requirements = RequirementsManager()
        self.setup_directories()
    
    def setup_directories(self):
        """Zəruri qovluqları yaradın"""
        directories = ['sessions', 'logs', 'backups']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def clear_screen(self):
        """Ekranı təmizləyin"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """Premium banner göstərin"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  🌐 SESSION GENERATOR v2.0                ║
║  🔧 Yaradan: Rzayeffdi / Ağa                                ║
║  🚀 Gelişmiş Xüsusiyyətlərlə Təkmilləşdirilmiş              ║
║                                                              ║
║  📊 Sistem: {platform.system()} {platform.release()}{' '*(30-len(platform.system()+platform.release()))}║
║  🐍 Python: {platform.python_version()}{' '*(38-len(platform.python_version()))}║
║  🌍 Mühit: {self.requirements.environment}{' '*(30-len(self.requirements.environment))}║
║  🔥 Pyrogram: {pyro_version if pyro_available else 'MÖVCUD DEYİL'}{' '*(35-len(pyro_version if pyro_available else 'MÖVCUD DEYİL'))}║
║  ⚡ Telethon: {tele_version if telethon_available else 'MÖVCUD DEYİL'}{' '*(36-len(tele_version if telethon_available else 'MÖVCUD DEYİL'))}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    async def get_credentials(self, bot: bool = False) -> Tuple[str, str, Optional[str]]:
        """İstifadəçidən şəxsiyyət vəsiqələrini alın"""
        print(f"\n{Colors.CYAN}🔐 Şəxsiyyət vəsiqələrinizi daxil edin:{Colors.END}")
        
        while True:
            api_id = input(f"{Colors.BLUE}🔹 API_ID: {Colors.END}").strip()
            if api_id.isdigit() and len(api_id) >= 5:
                break
            print(f"{Colors.RED}❌ Yanlış API_ID! Zəhmət olmasa rəqəmlərdən ibarət etibarlı API_ID daxil edin.{Colors.END}")
        
        api_hash = input(f"{Colors.BLUE}🔹 API_HASH: {Colors.END}").strip()
        if not api_hash:
            print(f"{Colors.RED}❌ API_HASH boş ola bilməz!{Colors.END}")
            return await self.get_credentials(bot)
        
        bot_token = None
        if bot:
            bot_token = input(f"{Colors.BLUE}🤖 Bot Token: {Colors.END}").strip()
            if not bot_token:
                print(f"{Colors.RED}❌ Bot Token boş ola bilməz!{Colors.END}")
                return await self.get_credentials(bot)
        
        return api_id, api_hash, bot_token
    
    async def handle_user_authentication(self, client):
        """İstifadəçi autentifikasiya əməliyyatları"""
        phone_number = input(f"{Colors.BLUE}📞 Telefon Nömrəsi (+994...): {Colors.END}").strip()
        
        sent_code = await client.send_code(phone_number)
        print(f"{Colors.YELLOW}📲 Doğrulama kodu göndərildi...{Colors.END}")
        
        while True:
            phone_code = input(f"{Colors.BLUE}🔐 SMS ilə gələn kodu daxil edin: {Colors.END}").strip()
            
            try:
                await client.sign_in(phone_number, sent_code.phone_code_hash, phone_code)
                break
            except PhoneCodeInvalid:
                print(f"{Colors.RED}❌ Yanlış kod! Yenidən cəhd edin.{Colors.END}")
            except PhoneCodeExpired:
                print(f"{Colors.RED}❌ Kodun müddəti bitmiş! Yenidən kod istəyirəm...{Colors.END}")
                sent_code = await client.resend_code(phone_number, sent_code.phone_code_hash)
            except SessionPasswordNeeded:
                print(f"{Colors.YELLOW}🔒 2FA aktiv, şifrə tələb olunur...{Colors.END}")
                password = getpass.getpass(f"{Colors.BLUE}🔑 2FA Şifrəsini daxil edin: {Colors.END}")
                await client.check_password(password)
                break
    
    async def create_pyrogram_session(self, bot: bool):
        """Təkmilləşdirilmiş Pyrogram session yaradın"""
        if not pyro_available:
            print(f"{Colors.RED}❌ Pyrogram kitabxanası mövcud deyil!{Colors.END}")
            print(f"{Colors.YELLOW}📦 Zəhmət olmasa əvvəlcə Pyrogram quraşdırın.{Colors.END}")
            return
        
        print(f"\n{Colors.MAGENTA}🚀 Pyrogram {'BOT' if bot else 'İSTİFADƏÇİ'} Sessionu Yaradılır...{Colors.END}")
        
        try:
            api_id, api_hash, bot_token = await self.get_credentials(bot)
            session_name = f"pyrogram_{'bot' if bot else 'user'}_{int(time.time())}"
            
            # Client konfiqurasiyası - YALNIZCA name istifadə edin
            client_config = {
                "name": session_name,
                "api_id": int(api_id),
                "api_hash": api_hash,
                "workdir": "./sessions",
                "in_memory": False
            }
            
            if bot:
                client_config["bot_token"] = bot_token
            
            # Client-i başlatmaq üçün xüsusi metod
            client = await self._start_pyrogram_client(client_config, bot)
            
            if not client:
                return
            
            # Session məlumatlarını alın
            me = await client.get_me()
            session_string = await client.export_session_string()
            
            # Nəticələri göstərin
            await self.show_session_results(client, me, session_string, "Pyrogram", "son", bot)
            
            # Sessionu fayla saxlayın
            await self.save_session_to_file(session_name, session_string, "pyrogram")
            
            await client.stop()
            
        except ApiIdInvalid:
            print(f"{Colors.RED}❌ Yanlış API_ID və ya API_HASH!{Colors.END}")
        except PhoneNumberInvalid:
            print(f"{Colors.RED}❌ Yanlış telefon nömrəsi!{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Gözlənilməz xəta: {e}{Colors.END}")
    
    async def _start_pyrogram_client(self, client_config, bot: bool):
        """Pyrogram client-i xüsusi başlatma metodu"""
        client = PyroClient(**client_config)
        
        try:
            if bot:
                # Bot üçün sadə başlatma
                await client.start()
            else:
                # İstifadəçi üçün xüsusi başlatma
                await client.connect()
                
                # Telefon nömrəsini alın
                phone_number = input(f"{Colors.BLUE}📞 Telefon Nömrəsi (+994...): {Colors.END}").strip()
                
                # Kodu göndərin
                sent_code = await client.send_code(phone_number)
                print(f"{Colors.YELLOW}📲 Doğrulama kodu göndərildi...{Colors.END}")
                
                # Kodu alın
                phone_code = input(f"{Colors.BLUE}🔐 SMS ilə gələn kodu daxil edin: {Colors.END}").strip()
                
                try:
                    await client.sign_in(phone_number, sent_code.phone_code_hash, phone_code)
                except SessionPasswordNeeded:
                    print(f"{Colors.YELLOW}🔒 2FA aktiv, şifrə tələb olunur...{Colors.END}")
                    password = getpass.getpass(f"{Colors.BLUE}🔑 2FA Şifrəsini daxil edin: {Colors.END}")
                    await client.check_password(password)
            
            return client
            
        except Exception as e:
            print(f"{Colors.RED}❌ Client başlatma xətası: {e}{Colors.END}")
            await client.disconnect()
            return None
    
    async def create_telethon_session(self, bot: bool):
        """Təkmilləşdirilmiş Telethon session yaradın"""
        if not telethon_available:
            print(f"{Colors.RED}❌ Telethon kitabxanası mövcud deyil!{Colors.END}")
            print(f"{Colors.YELLOW}📦 Zəhmət olmasa əvvəlcə Telethon quraşdırın.{Colors.END}")
            return
        
        print(f"\n{Colors.MAGENTA}⚡ Telethon {'BOT' if bot else 'İSTİFADƏÇİ'} Sessionu Yaradılır...{Colors.END}")
        
        try:
            api_id, api_hash, bot_token = await self.get_credentials(bot)
            session_name = f"telethon_{'bot' if bot else 'user'}_{int(time.time())}"
            
            client = TeleClient(TeleString(), int(api_id), api_hash)
            
            if bot:
                await client.start(bot_token=bot_token)
            else:
                phone_number = input(f"{Colors.BLUE}📞 Telefon Nömrəsi (+994...): {Colors.END}").strip()
                await client.start(phone=phone_number)
            
            me = await client.get_me()
            session_string = client.session.save()
            
            await self.show_session_results(client, me, session_string, "Telethon", "son", bot)
            await self.save_session_to_file(session_name, session_string, "telethon")
            
            await client.disconnect()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Xəta: {e}{Colors.END}")
    
    async def show_session_results(self, client, me, session_string, lib_name, version, bot):
        """Session nəticələrini göstərin"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ {lib_name} Sessionu Uğurla Yaradıldı!{Colors.END}")
        print(f"{Colors.CYAN}┌───────────────────────────────────────────────{Colors.END}")
        print(f"{Colors.CYAN}│ 👤 Ad: {me.first_name or me.username}{Colors.END}")
        print(f"{Colors.CYAN}│ 🆔 ID: {me.id}{Colors.END}")
        print(f"{Colors.CYAN}│ 📛 İstifadəçi Adı: @{me.username or 'Yox'}{Colors.END}")
        print(f"{Colors.CYAN}│ 🤖 Növ: {'Bot' if bot else 'İstifadəçi'}{Colors.END}")
        print(f"{Colors.CYAN}│ 📚 Kitabxana: {lib_name} {version}{Colors.END}")
        print(f"{Colors.CYAN}│ ⏰ Vaxt: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────{Colors.END}")
        
        print(f"\n{Colors.YELLOW}📦 Session Sətiri:{Colors.END}")
        print(f"{Colors.WHITE}{session_string}{Colors.END}\n")
        
        # Saxlanılmış Mesajlara göndərin
        try:
            await client.send_message(
                "me",
                f"""**✅ {lib_name} {'Bot' if bot else 'İstifadəçi'} Sessionu Yaradıldı!**

👤 **Ad:** `{me.first_name or me.username}`
🆔 **ID:** `{me.id}`
📛 **İstifadəçi Adı:** `@{me.username or 'Yox'}`
🤖 **Növ:** `{'Bot' if bot else 'İstifadəçi'}`
📚 **Versiya:** `{lib_name} {version}`
⏰ **Vaxt:** `{time.strftime('%Y-%m-%d %H:%M:%S')}`

`{session_string}`"""
            )
            print(f"{Colors.GREEN}💾 Session məlumatları Saxlanılmış Mesajlara göndərildi!{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ Saxlanılmış Mesajlara göndərilə bilmədi: {e}{Colors.END}")
    
    async def save_session_to_file(self, session_name, session_string, lib_type):
        """Sessionu fayla saxlayın"""
        filename = f"sessions/{session_name}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {lib_type.upper()} SESSION SƏTİRİ\n")
                f.write(f"# Yaradıldı: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# BUNU HEÇ KİMƏ GÖSTƏRMEYİN!\n\n")
                f.write(session_string)
            
            print(f"{Colors.GREEN}💾 Session fayla saxlandı: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}❌ Fayla yazma xətası: {e}{Colors.END}")
    
    async def show_session_manager(self):
        """Session meneceri"""
        print(f"\n{Colors.CYAN}📊 Session Meneceri{Colors.END}")
        
        if os.path.exists('sessions'):
            sessions = [f for f in os.listdir('sessions') if f.endswith('.txt')]
            if sessions:
                print(f"{Colors.GREEN}📁 Mövcud Sessionlar:{Colors.END}")
                for i, session in enumerate(sessions, 1):
                    print(f"  {i}. {session}")
            else:
                print(f"{Colors.YELLOW}📁 Hələ ki, session faylı yoxdur.{Colors.END}")
        else:
            print(f"{Colors.RED}📁 Sessions qovluğu tapılmadı.{Colors.END}")
    
    async def system_info(self):
        """Sistem məlumatlarını göstərin"""
        print(f"\n{Colors.CYAN}🖥️  Sistem Məlumatları{Colors.END}")
        print(f"{Colors.WHITE}┌───────────────────────────────────────────────{Colors.END}")
        print(f"{Colors.WHITE}│ 🖥️  Əməliyyat Sistemi: {platform.system()} {platform.release()}{Colors.END}")
        print(f"{Colors.WHITE}│ 🐍 Python Versiyası: {platform.python_version()}{Colors.END}")
        print(f"{Colors.WHITE}│ 🏠 Mühit: {self.requirements.environment}{Colors.END}")
        print(f"{Colors.WHITE}│ 📁 İş Qovluğu: {os.getcwd()}{Colors.END}")
        
        if pyro_available:
            print(f"{Colors.WHITE}│ 🔥 Pyrogram Versiyası: {pyro_version}{Colors.END}")
        if telethon_available:
            print(f"{Colors.WHITE}│ ⚡ Telethon Versiyası: {tele_version}{Colors.END}")
        
        print(f"{Colors.WHITE}└───────────────────────────────────────────────{Colors.END}")
    
    async def main_menu(self):
        """Ana menyu"""
        while True:
            self.clear_screen()
            self.show_banner()
            
            menu = f"""
{Colors.CYAN}🎯 ANA MENYU - Seçiminizi edin:{Colors.END}

{Colors.GREEN}1️⃣  Pyrogram İstifadəçi Sessionu{Colors.END}
{Colors.GREEN}2️⃣  Pyrogram Bot Sessionu{Colors.END}
{Colors.BLUE}3️⃣  Telethon İstifadəçi Sessionu{Colors.END}
{Colors.BLUE}4️⃣  Telethon Bot Sessionu{Colors.END}
{Colors.YELLOW}5️⃣  Session Meneceri{Colors.END}
{Colors.MAGENTA}6️⃣  Sistem Məlumatları{Colors.END}
{Colors.RED}0️⃣  Çıxış{Colors.END}

{Colors.CYAN}┌───────────────────────────────────────────────{Colors.END}
{Colors.CYAN}│ 💡 Məsləhət: Bot sessionu üçün @BotFather-dan{Colors.END}
{Colors.CYAN}│ bot yaradın və API məlumatlarını alın.{Colors.END}
{Colors.CYAN}└───────────────────────────────────────────────{Colors.END}
            """
            print(menu)
            
            choice = input(f"{Colors.BOLD}🔸 Seçiminiz (0-6): {Colors.END}").strip()
            
            if choice == "1":
                if pyro_available:
                    await self.create_pyrogram_session(False)
                else:
                    print(f"{Colors.RED}❌ Pyrogram quraşdırılmayıb!{Colors.END}")
            elif choice == "2":
                if pyro_available:
                    await self.create_pyrogram_session(True)
                else:
                    print(f"{Colors.RED}❌ Pyrogram quraşdırılmayıb!{Colors.END}")
            elif choice == "3":
                if telethon_available:
                    await self.create_telethon_session(False)
                else:
                    print(f"{Colors.RED}❌ Telethon quraşdırılmayıb!{Colors.END}")
            elif choice == "4":
                if telethon_available:
                    await self.create_telethon_session(True)
                else:
                    print(f"{Colors.RED}❌ Telethon quraşdırılmayıb!{Colors.END}")
            elif choice == "5":
                await self.show_session_manager()
            elif choice == "6":
                await self.system_info()
            elif choice == "0":
                print(f"\n{Colors.GREEN}👋 Görüşənədək!{Colors.END}")
                break
            else:
                print(f"{Colors.RED}❌ Yanlış seçim!{Colors.END}")
            
            if choice != "0":
                input(f"\n{Colors.CYAN}⏎ Davam etmək üçün Enter düyməsini basın...{Colors.END}")

async def main():
    """Ana funksiya"""
    generator = PremiumSessionGenerator()
    
    # Tələbləri yoxlayın
    if not generator.requirements.check_and_install_all():
        print(f"{Colors.RED}❌ Bəzi zəruri paketlər yüklənə bilmədi!{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ Bəzi xüsusiyyətlər işləməyə bilər.{Colors.END}")
    
    # Ana menyunu başladın
    try:
        await generator.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Proqram istifadəçi tərəfindən dayandırıldı.{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Gözlənilməz xəta: {e}{Colors.END}")

if __name__ == "__main__":
    # Python versiya yoxlaması
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 və ya daha yüksək tələb olunur!")
        sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Proqram dayandırıldı.{Colors.END}")
