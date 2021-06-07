from collections import deque
import os
import asyncio

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)
from wechaty_puppet import MessageType

# Initialize a PaddleHub plato-mini model
import paddlehub as hub
model = hub.Module(name='plato-mini', version='1.0.0')
model._interactive_mode = True
model.max_turn = 10
model.context = deque(maxlen=model.max_turn)


async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    ### PaddleHub chatbot
    if isinstance(msg.text(), str) and len(msg.text()) > 0 \
        and msg._payload.type == MessageType.MESSAGE_TYPE_TEXT \
        and msg.text().startswith('[Test]'):  # Use a special token '[Test]' to select messages to respond.
        bot_response = model.predict(data=msg.text().replace('[Test]', ''))[0]
        await msg.say(bot_response)  # Return the text generated by PaddleHub chatbot
    ###


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    #
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()


asyncio.run(main())
