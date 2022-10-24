from redis import Redis

LOWER_LIMIT = 0
UPPER_LIMIT = 1

TYPE = 0
TEMP = 1


class LimitsDatabase:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port

    def _connect(self) -> Redis:
        return Redis(host=self.host, port=self.port, decode_responses=True)

    def add_new_sensor(self, sensor: str, sensor_type: str, temp: str = 0):
        db = self._connect()

        db.rpush(sensor, sensor_type, temp)

        db.close()

    def set_sensor_type(self, sensor: str, sensor_type: str) -> None:
        db = self._connect()

        db.lset(sensor, TYPE, sensor_type)

        db.close()

    def set_sensor_temp(self, sensor: str, temp: str) -> None:
        db = self._connect()

        db.lset(sensor, TEMP, temp)

        db.close()

    def add_new_type(self, sensor_type: str, lower_limit: str = 0, upper_limit: str = 0) -> None:
        db = self._connect()

        db.rpush(sensor_type, lower_limit, upper_limit)

        db.close()

    def set_lower_type_limit(self, sensor_type: str, limit: str) -> None:
        db = self._connect()

        db.lset(sensor_type, LOWER_LIMIT, limit)

        db.close()

    def set_upper_type_limit(self, sensor_type: str, limit: str) -> None:
        db = self._connect()

        db.lset(sensor_type, UPPER_LIMIT, limit)

        db.close()

    def get_sensor_limits(self, sensor) -> dict:
        db = self._connect()

        sensor_type = self.get_sensor_type(sensor)
        limits = db.lrange(sensor_type, LOWER_LIMIT, UPPER_LIMIT)

        db.close()

        return {"lower": limits[LOWER_LIMIT], "upper": limits[UPPER_LIMIT]}

    def get_sensor_type(self, sensor) -> str:
        db = self._connect()

        sensor_type = db.lrange(sensor, TYPE, TYPE)[0]

        db.close()

        return sensor_type
