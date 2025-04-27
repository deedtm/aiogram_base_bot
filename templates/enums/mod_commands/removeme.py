from dataclasses import dataclass


@dataclass
class Removeme:
	general: str = "❓  Are you sure you want to remove your data from the database?\n\n😴  Ignore this message, if you don't"
	yes: str = '✅  Your data has been removed from the database.\n\n❗️  You will be added to database again if you send any message to me'
