from helpers.config import get_settings , Settings

class BaseDateModel:
    def __init__(self, db_client:object):
        self.db_client = db_client
        self.app_settings = get_settings()

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date