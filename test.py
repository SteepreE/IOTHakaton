from redis import Redis

host="localhost"
port=6379

red = Redis(host=host, port=port, decode_responses=True)


a = red.lrange("rpush", 0, 0)

print(a)