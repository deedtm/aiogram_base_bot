from dataclasses import dataclass


@dataclass
class Exceptions:
	base: str = '❗️  An error has occurred:\n\n<pre>{}</pre>'
	no_data: str = "😢  I don't have such information"
	retry: str = '🔄  Try again, please'
