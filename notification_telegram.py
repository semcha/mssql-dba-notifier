from dataclasses import dataclass

import telebot
from dacite import from_dict


@dataclass
class TelegramChat:
    api_token: str
    chat_id: str


def get_telegram_chat(config_telegram):
    tg_chat = from_dict(data_class=TelegramChat, data=config_telegram)
    return tg_chat


def escape_text_message(text):
    for ch in ["-", ":", ".", ",", "(", ")", "#", "_", "!"]:
        if ch in text:
            text = text.replace(ch, "\\" + ch)
    return text


def send_text_message(tg_chat: TelegramChat, message_text):
    text = escape_text_message(message_text)
    bot = telebot.TeleBot(tg_chat.api_token)
    bot.send_message(tg_chat.chat_id, text, parse_mode="MarkdownV2")
