import os

class Config(object):
    DEBUG = False
    SHOW_PRIVACY_POLICY = os.getenv('SHOW_PRIVACY_POLICY', False)
    SCOUT_MONITOR = os.getenv('SCOUT_MONITOR', False)
    SCOUT_KEY = os.getenv('SCOUT_KEY', '')
    SCOUT_NAME = 'Barmycodes'
    GOOGLE_ANALYTICS_CODE = os.getenv('GOOGLE_ANALYTICS_CODE', '')
