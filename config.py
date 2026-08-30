import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8617104939:AAFVn71gU6WdKPwSeEGOnxiy1j7_r2dKm4k")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "8361641777").split(",") if x.strip()]
TARGET_BOT = os.getenv("TARGET_BOT", "@FunAuthBot")
API_ID = int(os.getenv("API_ID", "37635168"))
API_HASH = os.getenv("API_HASH", "47e36b7f99b31f55be222b4200ea94ca")
SESSION_STRING = os.getenv("SESSION_STRING", "BQI-RGAATWam7mmua4XLiKB8DH5JnvSYYSZV5sQYxZEKd2dU6J-Ozt6OqKc5dn3TnnqSe9ZBjaN-2sPSmbBSx5CQasA3-oDwhurBUfIK8nHKDqOymqptViFhMuSnZT0kNK6t6ti9L3KJPElwd4baYnjduB8Dgnea8fNGDseA1bXhkIZdbq2ffGLGS8EXRhMfAPkM0KXk_MQasZNcUQ_ZHUPHitr4pEgJtnfgl8tWjHOl4zKPUqS2SPLtHlSKMigAyscB-a5iBKxdmuS0RaU89AVOcjT_yj6GOUezcMfkCfz88i2WHo9b8-feZyNvo0nTaEc3qRSkyhBYQ-21kQmb3-6CAa05WAAAAAH3bW-aAA")
