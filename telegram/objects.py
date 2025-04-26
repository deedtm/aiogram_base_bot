from aiogram import Router
from .middlewares.general import GeneralMW

router = Router()

router.message.middleware(GeneralMW())
router.callback_query.middleware(GeneralMW())
