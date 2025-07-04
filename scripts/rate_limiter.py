import time
import threading

class DappRadarRateLimiter:
    """
    Rate limiter for DappRadar API - ensures max 4 requests per second
    """
    def __init__(self, max_requests_per_second=4):
        self.max_requests_per_second = max_requests_per_second
        self.min_interval = 1.0 / max_requests_per_second  # 0.25 seconds between requests
        self.last_request_time = 0
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        """Wait if necessary to maintain rate limit"""
        with self.lock:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            
            if time_since_last_request < self.min_interval:
                sleep_time = self.min_interval - time_since_last_request
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()
