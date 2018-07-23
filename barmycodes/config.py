import os

class Config(object):
    DEBUG = False
    USE_CONSENT = os.getenv('USE_CONSENT', False)
    CONSENT_FLOW_ID = os.getenv('CONSENT_FLOW_ID', '')
    SHOW_ADS = os.getenv('SHOW_ADS', False)
    SHOW_PRIVACY_POLICY = os.getenv('SHOW_PRIVACY_POLICY', False)
    SCOUT_MONITOR = os.getenv('SCOUT_MONITOR', False)
    SCOUT_KEY = os.getenv('SCOUT_KEY', '')
    SCOUT_NAME = 'Barmycodes'
