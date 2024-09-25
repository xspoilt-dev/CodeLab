__author__ = "@x_spoilt"
__version__ = "1.0.0"
__description__ = "Telegram bot to generate images using API"

import telebot
import requests
import base64
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot API Token
__0x1A__ = '7788853732:AAHmqInoT8e-Tb5Nnz6KF4u0KUo-OAW38eo'
# Admin Chat ID
__0x2B__ = '7375280700'
__0x3C__ = 'users.json'

__0x4D__ = telebot.TeleBot(__0x1A__)

def __0x5E__():
    if os.path.exists(__0x3C__):
        with open(__0x3C__, 'r') as __0x6F__:
            return json.load(__0x6F__)
    return []

def __0x7A__(__0x8B__):
    with open(__0x3C__, 'w') as __0x6F__:
        json.dump(__0x8B__, __0x6F__)

__0x9C__ = __0x5E__()

def __0xAD__():
    __0xBE__ = InlineKeyboardMarkup(row_width=2)
    __0xCF__ = InlineKeyboardButton('Send Notice', callback_data='send_notice')
    __0xD0__ = InlineKeyboardButton('Show Ads', callback_data='show_ads')
    __0xE1__ = InlineKeyboardButton('Total Users', callback_data='total_users')
    __0xBE__.add(__0xCF__, __0xD0__, __0xE1__)
    return __0xBE__

@__0x4D__.message_handler(commands=['start'])
def __0xF2__(__0x102__):
    __0x113__ = str(__0x102__.chat.id)
    if __0x113__ not in __0x9C__:
        __0x9C__.append(__0x113__)
        __0x7A__(__0x9C__)

    if __0x113__ == __0x2B__:
        __0x4D__.reply_to(__0x102__, "Welcome Admin!", reply_markup=__0xAD__())
    else:
        __0x4D__.reply_to(__0x102__, "Welcome to the bot! Please type your prompt to generate an image.")

@__0x4D__.callback_query_handler(func=lambda __0xA__: True)
def __0x124__(__0x135__):
    if str(__0x135__.message.chat.id) == __0x2B__:
        if __0x135__.data == 'send_notice':
            __0x4D__.send_message(__0x2B__, "Please enter the notice message:")
            __0x4D__.register_next_step_handler(__0x135__.message, __0x146__)
        elif __0x135__.data == 'show_ads':
            __0x4D__.send_message(__0x2B__, "Please enter the ad message:")
            __0x4D__.register_next_step_handler(__0x135__.message, __0x157__)
        elif __0x135__.data == 'total_users':
            __0x4D__.send_message(__0x2B__, f"Total Users: {len(__0x9C__)}")

@__0x4D__.message_handler(func=lambda __0xB__: True)
def __0x168__(__0x102__):
    __0x179__ = __0x102__.text
    __0x4D__.reply_to(__0x102__, "Generating image, please wait...")
    __0x18A__(__0x102__, __0x179__)

def __0x18A__(__0x102__, __0x179__):
    __0x19B__ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://own-ai.pages.dev/',
        'Content-Type': 'application/json',
        'Origin': 'https://own-ai.pages.dev',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=0',
    }

    __0x1AC__ = {
        'prompt': __0x179__,
    }

    __0x1BD__ = requests.post('https://own-ai.onrender.com/api/v1/generateImage', headers=__0x19B__, json=__0x1AC__)
    __0x1CE__ = __0x1BD__.json()

    if __0x1CE__['statusCode']:
        __0x1DF__ = base64.b64decode(__0x1CE__['data']['photo'])
        __0x4D__.send_photo(__0x102__.chat.id, __0x1DF__)
    else:
        __0x4D__.reply_to(__0x102__, "Failed to generate image. Please try again.")

def __0x146__(__0x102__):
    __0x179__ = __0x102__.text
    for __0x113__ in __0x9C__:
        __0x4D__.send_message(__0x113__, f"Notice: {__0x179__}")

def __0x157__(__0x102__):
    __0x18B__ = __0x102__.text
    for __0x113__ in __0x9C__:
        __0x4D__.send_message(__0x113__, f"Ad: {__0x18B__}")

__0x4D__.polling()

