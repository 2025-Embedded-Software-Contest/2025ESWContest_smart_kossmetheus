# from gateway.rate_limit import MemoryRateLimiter, RateConfig
# import time


# def test_sliding_window():
#     rl = MemoryRateLimiter(RateConfig(limit=3, window_sec=1))
#     ident = "id"
    
#     assert rl.allow(ident)[0]
#     assert rl.allow(ident)[0]
#     assert rl.allow(ident)[0]
#     assert not rl.allow(ident)[0]
#     time.sleep(1.1)
#     assert rl.allow(ident)[0]