import os

class Config(object):
    DEBUG = False
    USE_CONSENT = os.getenv('USE_CONSENT', False)
    CONSENT_FLOW_ID = os.getenv('CONSENT_FLOW_ID', '')
    SHOW_ADS = os.getenv('SHOW_ADS', False)
    AD_CLIENT = os.getenv('AD_CLIENT', '')
    AD_SLOT = os.getenv('AD_SLOT', '')
    SHOW_PRIVACY_POLICY = os.getenv('SHOW_PRIVACY_POLICY', False)
