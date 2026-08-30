import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, SESSION_STRING, TARGET_BOT

logger = logging.getLogger(__name__)

class UserBot:
    def __init__(self):
        self.client = None
        self.is_running = False
    
    async def init(self):
        if not API_ID or not API_HASH:
            return False
        
        try:
            if SESSION_STRING:
                self.client = Client(
                    "userbot",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=SESSION_STRING,
                    in_memory=True
                )
            else:
                self.client = Client(
                    "userbot",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    in_memory=True
                )
            
            await self.client.start()
            self.is_running = True
            logger.info("Userbot started")
            return True
        except Exception as e:
            logger.error(f"Failed to start userbot: {e}")
            return False
    
    async def send_bind(self, nick, password):
        if not self.client or not self.is_running:
            return False, "Userbot not initialized"
        
        try:
            command = f"/bind {nick} {password}"
            await self.client.send_message(TARGET_BOT, command)
            await asyncio.sleep(2)
            return True, f"✓ {nick}: bind отправлен"
        except Exception as e:
            return False, f"✗ {nick}: {e}"
    
    async def send_2fa(self, nick):
        if not self.client or not self.is_running:
            return False, "Userbot not initialized"
        
        try:
            command = f"/2fa {nick}"
            await self.client.send_message(TARGET_BOT, command)
            await asyncio.sleep(2)
            return True, f"✓ {nick}: 2fa отправлен"
        except Exception as e:
            return False, f"✗ {nick}: {e}"
    
    async def stop(self):
        if self.client:
            await self.client.stop()
            self.is_running = False

userbot = UserBot()
