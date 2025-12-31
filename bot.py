import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = -1002822914255

saved_text = ""
waiting_for_links = False
link_dict = {}

async def save_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saved_text, waiting_for_links
    message = update.message

    if message.chat_id != GROUP_ID:
        return

    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply_text("❌ Reply to a message with `.l`")
        return

    saved_text = message.reply_to_message.text.strip()
    waiting_for_links = True
    await message.reply_text("📎 Send links (digit + link)")

async def process_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_links, saved_text, link_dict

    if not waiting_for_links:
        return

    message = update.message
    if message.chat_id != GROUP_ID:
        return

    if not re.search(r'https?://|deleted', message.text or ''):
        return

    link_dict.clear()

    for line in message.text.splitlines():
        try:
            digit, link = line.split(maxsplit=1)
            if digit.isdigit():
                link_dict[digit] = link.strip()
        except:
            pass
