from mqttreceiver.mqttreceiver import MqttReceiver
from threading import Thread
from database.database import LimitsDatabase
from aiogram import Bot, types, Dispatcher, executor


TOKEN = ""
ADMIN_LIST = []

users_to_notify = []

bot = Bot(TOKEN)
dp = Dispatcher(bot)


def validate(func):
    def wrapper(message):
        if message.from_user.id in ADMIN_LIST:
            return func(message)
        else:
            return

    return wrapper


@dp.message_handler(commands=["start", "subscribe"])
@validate
async def subscribe(message: types.Message) -> None:
    users_to_notify.append(message.from_user.id)
    await message.reply("Вы подписаны на уведомления!")


@dp.message_handler(commands=["add"])
@validate
async def add_sensor(message: types.Message) -> None:
    """add new sensor"""


@dp.message_handler(commands=["unsubscribe"])
@validate
async def unsubscribe(message: types.Message) -> None:
    users_to_notify.remove(message.from_user.id)
    await message.reply("Вы отписаны от уведомлений!")


async def notify(message: str) -> None:
    for user in users_to_notify:
        await bot.send_message(user, message)


def main():

    limits_database = LimitsDatabase()
    mqtt_receiver = MqttReceiver(limits_database, notify)

    Thread(target=executor.start_polling, args=dp).start()
    Thread(target=mqtt_receiver.start).start()


if __name__ == '__main__':
    main()
