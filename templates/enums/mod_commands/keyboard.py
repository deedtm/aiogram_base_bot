from dataclasses import dataclass


@dataclass
class Keyboard:
	general: str = '⌨️  You can use the keyboard below to learn information about yourself'
	id: str = '🆔  Your ID is <code>{}</code>'
	username: str = '👤  Your username is <code>{}</code>'
	first_name: str = '👤  Your first name is <code>{}</code>'
	last_name: str = '👤  Your last name is <code>{}</code>'
	phone_number: str = '📱  Your phone number is <code>{}</code>'
	location: str = '📍  Your location is <code>{}</code>'
	language_code: str = '🌐  Your language code is <code>{}</code>'
	url: str = '🔗  Your profile URL is {}'
