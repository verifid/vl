from .store.redis_store import RedisStore
from redis import Redis

redis = Redis(host='localhost', port=6379)
store = RedisStore(redis)
