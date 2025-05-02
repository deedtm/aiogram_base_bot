from dataclasses import dataclass


@dataclass
class Exceptions:
	base: str = '❗️  An error has occurred:\n\n<pre>{}</pre>'
	no_data: str = "😢  I don't have such information"
	retry: str = '🔄  Try again, please'
	no_args: str = '⭕️  No arguments provided'
	wrong_args: str = '❌  Wrong arguments provided'
	user_not_found: str = '🔎  User not found'
	low_access: str = "🔒  You don't have enough access to do this"
	low_access_to_set: str = '🔒  You cannot change the access level of a user whose access level is greater than or equal to yours'
	own_access: str = '🔒  You cannot change your own access level'
	over_access_set: str = '🔒  You cannot set an access level greater than your own'
