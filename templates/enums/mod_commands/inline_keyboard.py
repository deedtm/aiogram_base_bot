from dataclasses import dataclass


@dataclass
class InlineKeyboard:
	general: str = '📋  You can use the keyboard below to learn information about me'
	id: str = '🆔  My ID is <code>{}</code>'
	username: str = '👤  My username is <code>{}</code>'
	first_name: str = '👤  My first name is <code>{}</code>'
	last_name: str = '👤  My last name is <code>{}</code>'
	language_code: str = '🌐  My language code is <code>{}</code>'
	url: str = '🔗  My profile URL is {}'
