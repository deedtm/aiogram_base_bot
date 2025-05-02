from dataclasses import dataclass


@dataclass
class Admin:
	general: str = '🥑  <b>Admin panel</b>\n\n{}'
	commands_list_fmt: str = '<i>{command} {args}</i>— {description}'
	users: str = "👤  <b>Users</b>\n\n{}\n\n<b>Total: {}</b>\n<i>Enter the user's first name to find them</i>"
	users_list_fmt: str = '<b>{id}.</b> {name} — <code>{user_id}</code>'
	random_users: str = '🤹  Added {} users'
	getuser: str = '👤  <b>User</b>\n\n{}'
	user_fmt: str = '<b>{}</b>: {}'
	access: str = '🔑  Changed access <b>{}</b> ➝ <b>{}</b> for <i>{}</i>'
