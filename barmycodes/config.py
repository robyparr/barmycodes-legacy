import os

class Config(object):
    DEBUG = False
    USE_COOKIEBOT = os.getenv('USE_COOKIEBOT', False)
    COOKIEBOT_ID = os.getenv('COOKIEBOT_ID', '')
    SHOW_ADS = os.getenv('SHOW_ADS', False)
    AD_CLIENT = os.getenv('AD_CLIENT', '')
    SHOW_PRIVACY_POLICY = os.getenv('SHOW_PRIVACY_POLICY', False)
