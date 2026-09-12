from utils.const import TESTING, TEST_REDIS_URL
import redis.asyncio as aioredis

redis = None


async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.from_url(TEST_REDIS_URL)


#
# if TESTING or IS_LOAD_TEST:
#     REDIS_CONNECTION_URL = TEST_REDIS_URL
# elif IS_PRODUCTION:
#     REDIS_CONNECTION_URL = REDIS_URL_PRODUCTION
# else:
#     REDIS_CONNECTION_URL = REDIS_URL
#
# redis = None
