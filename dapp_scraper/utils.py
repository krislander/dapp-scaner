import os
import configparser
import requests

from scripts import rate_limiter
from bs4 import BeautifulSoup

# load config.ini
CFG = configparser.ConfigParser()
cfg_path = os.path.join(os.path.dirname(__file__), os.pardir, "config", "config.ini")
CFG.read(cfg_path)

def get_rate_limiter():
    if not hasattr(get_rate_limiter, "instance"):
        get_rate_limiter.instance = rate_limiter.DappRadarRateLimiter()
    return get_rate_limiter.instance

def get_database_url():
    return CFG["database"]["url"]

def get_api_key(service_name):
    return CFG[service_name]["api_key"]

def make_rate_limited_request(url, headers, params=None):
    """
    Make a rate-limited request to DappRadar API
    """
    rate_limiter_instance = get_rate_limiter()
    rate_limiter_instance.wait_if_needed()
    return requests.get(url, headers=headers, params=params)
