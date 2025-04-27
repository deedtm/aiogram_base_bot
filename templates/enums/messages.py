from dataclasses import dataclass


@dataclass
class Messages:
	text: str = '🗣  Echo says: <i>{}</i>'
	media: str = '👀  Nice {}!'
