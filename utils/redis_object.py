from utils.const import TESTING, TEST_REDIS_URL, IS_LOAD_TEST, REDIS_URL
import redis.asyncio as aioredis

#
# redis = None
#
#
# async def check_test_redis():
#     global redis
#     if TESTING or IS_LOAD_TEST:
#         redis = await aioredis.from_url(TEST_REDIS_URL)


if TESTING or IS_LOAD_TEST:
    REDIS_CONNECTION_URL = TEST_REDIS_URL
else:
    REDIS_CONNECTION_URL = REDIS_URL

redis = None