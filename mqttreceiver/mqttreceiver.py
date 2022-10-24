import paho.mqtt.client as mqtt
from database.database import LimitsDatabase


class MqttReceiver:

    def __init__(self, database: LimitsDatabase, notifier_func, broker_host: str = 'localhost', port: int = 1883):
        self.database = database
        self.notifier_func = notifier_func

        self.receiver = mqtt.Client()

        self.receiver.on_connect = lambda *args: print("CONNECTED")
        self.receiver.connect(broker_host, port)

        self.receiver.on_message = self.on_message

    def subscribe_new_sensor(self, topic_name: str) -> None:
        self.receiver.subscribe(topic_name)

    def start(self) -> None:
        self.receiver.loop_forever()

    def on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage) -> None:
        topic = message.topic

        message_data = message.payload.decode()
        sensors = message_data.split('\n')

        for sensor in sensors:
            sensor_data = sensor.split(' ')

            sensor_name = f"{topic}-{sensor_data[0]}"
            sensor_temp = sensor_data[1]

            self.database.set_sensor_temp(sensor_name, sensor_temp)

            if not self.validate_temp(sensor_name, sensor_temp):
                self.notifier_func(
                    f"""КРИТИЧЕСКОЕ ЗАНЧЕНИЕ {sensor_name}: {sensor_temp}"""
                )

    def validate_temp(self, sensor: str, temp: str):
        limits = self.database.get_sensor_limits(sensor)

        if int(limits["lower"]) < int(temp) < int(limits["upper"]):
            return True

        return False
