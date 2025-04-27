from dataclasses import dataclass
from .mod_commands.removeme import Removeme
from .mod_commands.keyboard import Keyboard
from .mod_commands.inline_keyboard import InlineKeyboard

@dataclass
class Commands:
	start: str = '🤖  Hello! I\'m just a template bot for developers\n\n🔗  <a href="https://github.com/deedtm/aiogram_base_bot">Source code</a>\n⭐️  Please star the project if you liked the bot'
	database: str = "📊  Here's your information saved in the database:\n\n{}"
	removeme: Removeme = Removeme(general="❓  Are you sure you want to remove your data from the database?\n\n😴  Ignore this message, if you don't", yes='✅  Your data has been removed from the database.\n\n❗️  You will be added to database again if you send any message to me')
	keyboard: Keyboard = Keyboard(general='⌨️  You can use the keyboard below to learn information about yourself', id='🆔  Your ID is <code>{}</code>', username='👤  Your username is <code>{}</code>', first_name='👤  Your first name is <code>{}</code>', last_name='👤  Your last name is <code>{}</code>', phone_number='📱  Your phone number is <code>{}</code>', location='📍  Your location is <code>{}</code>', language_code='🌐  Your language code is <code>{}</code>', url='🔗  Your profile URL is {}')
	inline_keyboard: InlineKeyboard = InlineKeyboard(general='📋  You can use the keyboard below to learn information about me', id='🆔  My ID is <code>{}</code>', username='👤  My username is <code>{}</code>', first_name='👤  My first name is <code>{}</code>', last_name='👤  My last name is <code>{}</code>', language_code='🌐  My language code is <code>{}</code>', url='🔗  My profile URL is {}')
