import asyncio
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN, ADMIN_IDS, TARGET_BOT
from userbot import userbot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

users = {}

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def main_menu(user_id: int):
    keyboard = [
        [InlineKeyboardButton("📝 Добавить ники", callback_data="add_nicks")],
        [InlineKeyboardButton("🔑 Указать пароль", callback_data="set_password")],
        [InlineKeyboardButton("🔗 Bind (привязать)", callback_data="bind")],
        [InlineKeyboardButton("🔓 2FA (отключить)", callback_data="twofa")],
    ]
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("🎬 Добавить гифку", callback_data="add_gif")])
        keyboard.append([InlineKeyboardButton("📱 Добавить сессию", callback_data="add_session")])
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in users:
        users[user_id] = {"nicks": [], "password": "", "gif": None, "session": None}
    
    gif = users[user_id].get("gif")
    
    if gif:
        await update.message.reply_animation(
            animation=gif,
            caption="Меню:",
            reply_markup=main_menu(user_id)
        )
    else:
        await update.message.reply_text("Меню:", reply_markup=main_menu(user_id))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    action = query.data
    
    if user_id not in users:
        users[user_id] = {"nicks": [], "password": "", "gif": None, "session": None}
    
    if action == "add_nicks":
        await query.edit_message_text(
            "Отправьте ники списком:\n\nник1\nник2\nник3",
            reply_markup=back_button()
        )
        context.user_data["awaiting"] = "nicks"
    
    elif action == "set_password":
        await query.edit_message_text(
            "Отправьте пароль:",
            reply_markup=back_button()
        )
        context.user_data["awaiting"] = "password"
    
    elif action == "bind":
        nicks = users[user_id]["nicks"]
        password = users[user_id]["password"]
        
        if not nicks:
            await query.edit_message_text("❌ Сначала добавьте ники", reply_markup=main_menu(user_id))
            return
        
        if not password:
            await query.edit_message_text("❌ Сначала укажите пароль", reply_markup=main_menu(user_id))
            return
        
        if not userbot.is_running:
            await query.edit_message_text("❌ Userbot не запущен. Добавьте сессию.", reply_markup=main_menu(user_id))
            return
        
        await query.edit_message_text(f"🔄 Отправляю команды bind в {TARGET_BOT}...", reply_markup=main_menu(user_id))
        
        results = []
        for nick in nicks:
            success, message = await userbot.send_bind(nick, password)
            results.append(message)
        
        await query.message.reply_text("Результаты:\n\n" + "\n".join(results))
    
    elif action == "twofa":
        nicks = users[user_id]["nicks"]
        
        if not nicks:
            await query.edit_message_text("❌ Сначала добавьте ники", reply_markup=main_menu(user_id))
            return
        
        if not userbot.is_running:
            await query.edit_message_text("❌ Userbot не запущен. Добавьте сессию.", reply_markup=main_menu(user_id))
            return
        
        await query.edit_message_text(f"🔄 Отправляю команды 2FA в {TARGET_BOT}...", reply_markup=main_menu(user_id))
        
        results = []
        for nick in nicks:
            success, message = await userbot.send_2fa(nick)
            results.append(message)
        
        await query.message.reply_text("Результаты:\n\n" + "\n".join(results))
    
    elif action == "add_session":
        if not is_admin(user_id):
            await query.edit_message_text("❌ Нет прав администратора", reply_markup=main_menu(user_id))
            return
        
        await query.edit_message_text(
            "Отправьте строку сессии Pyrogram\n\n"
            "Для получения:\n"
            "1. Запустите get_session.py\n"
            "2. Введите номер телефона\n"
            "3. Введите код из Telegram\n"
            "4. Скопируйте строку сессии",
            reply_markup=back_button()
        )
        context.user_data["awaiting"] = "session"
    
    elif action == "add_gif":
        if not is_admin(user_id):
            await query.edit_message_text("❌ Нет прав администратора", reply_markup=main_menu(user_id))
            return
        
        await query.edit_message_text("Отправьте гифку:", reply_markup=back_button())
        context.user_data["awaiting"] = "gif"
    
    elif action == "back":
        await query.edit_message_text("Меню:", reply_markup=main_menu(user_id))
        context.user_data["awaiting"] = None

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    awaiting = context.user_data.get("awaiting")
    
    if user_id not in users:
        users[user_id] = {"nicks": [], "password": "", "gif": None, "session": None}
    
    if awaiting == "nicks":
        nicks = [n.strip() for n in text.split("\n") if n.strip()]
        users[user_id]["nicks"] = nicks
        await update.message.reply_text(f"✅ Ники добавлены: {len(nicks)}", reply_markup=main_menu(user_id))
        context.user_data["awaiting"] = None
    
    elif awaiting == "password":
        users[user_id]["password"] = text.strip()
        await update.message.reply_text("✅ Пароль установлен", reply_markup=main_menu(user_id))
        context.user_data["awaiting"] = None
    
    elif awaiting == "session":
        if not is_admin(user_id):
            return
        
        users[user_id]["session"] = text.strip()
        
        await userbot.stop()
        
        import config
        config.SESSION_STRING = text.strip()
        
        success = await userbot.init()
        
        if success:
            await update.message.reply_text("✅ Сессия добавлена и userbot запущен", reply_markup=main_menu(user_id))
        else:
            await update.message.reply_text("❌ Ошибка при запуске userbot", reply_markup=main_menu(user_id))
        
        context.user_data["awaiting"] = None
    
    elif awaiting == "gif":
        await update.message.reply_text("Пожалуйста, отправьте гифку (анимацию)", reply_markup=back_button())

async def gif_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        return
    
    if context.user_data.get("awaiting") == "gif":
        gif_id = update.message.animation.file_id
        users[user_id]["gif"] = gif_id
        await update.message.reply_text("✅ Гифка сохранена", reply_markup=main_menu(user_id))
        context.user_data["awaiting"] = None

async def init_userbot():
    await userbot.init()

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.ANIMATION, gif_handler))
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_userbot())
    
    logger.info("Bot started")
    logger.info(f"Target bot: {TARGET_BOT}")
    logger.info(f"Admins: {ADMIN_IDS}")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
