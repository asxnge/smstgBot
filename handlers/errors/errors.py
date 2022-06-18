from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, InvalidQueryID, \
    ChatNotFound, BadRequest, MessageToEditNotFound, BotBlocked, TelegramAPIError, MessageCantBeDeleted, \
        RetryAfter
from loader import vip



@vip.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, MessageNotModified):
        return True
    
    if isinstance(exception, BadRequest):
        return True

    if isinstance(exception, MessageToEditNotFound):
        return True
    
    if isinstance(exception, BotBlocked):
        return True

    if isinstance(exception, ChatNotFound):
        return True

    if isinstance(exception, MessageCantBeDeleted):
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        return True

    if isinstance(exception, InvalidQueryID):
        return True

    if isinstance(exception, RetryAfter):
        return True

    if isinstance(exception, TelegramAPIError):
        return True

'''

@vip.errors_handler(exception=MessageNotModified)
async def user_floods_callback_requests(update, exception):
    """
    This error occurs when the user simultaneously
    pressed the same inline button in a short time.
    """
    return True

@vip.errors_handler(exception=BotBlocked)
async def user_bot_blocked(update, exception):
    """
    This error occurs when the user simultaneously
    pressed the same inline button in a short time.
    """
    return True

@vip.errors_handler(exception=TelegramAPIError)
async def user_tg_api_error(update, exception):
    """
    This error occurs when the user simultaneously
    pressed the same inline button in a short time.
    """
    return True

@vip.errors_handler(exception=MessageToEditNotFound)
async def user_floods_callback_edit_not(update, exception):
    """
    This error occurs when the user simultaneously
    pressed the same inline button in a short time.
    """
    return True


@vip.errors_handler(exception=MessageToDeleteNotFound)
async def user_msg_delete_not(update, exception):
    """ 
    This error occurs if no message for deletion is found
    """
    return True

@vip.errors_handler(exception=InvalidQueryID)
async def invalid_query_id(update, exception):
    """ 
    This error occurs if invalid query id
    """
    return True

@vip.errors_handler(exception=ChatNotFound)
async def user_chat_not(update, exception):
    """ 
    This error occurs if chat not found
    """
    return True

@vip.errors_handler(exception=BadRequest)
async def user_bad_request(update, exception):
    """ 
    This error occurs if Bad Request
    """
    return True
'''