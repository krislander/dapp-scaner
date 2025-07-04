import os
import configparser
import requests
from bs4 import BeautifulSoup

# load config.ini
CFG = configparser.ConfigParser()
cfg_path = os.path.join(os.path.dirname(__file__), os.pardir, "config", "config.ini")
CFG.read(cfg_path)

def get_database_url():
    return CFG["database"]["url"]

def get_api_key(service_name):
    return CFG[service_name]["api_key"]
