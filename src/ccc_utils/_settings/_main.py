from ._env import env

class CONFIG:
    class SPREADSHEET:
        GOOGLE_CLOUD_JSON_CREDENTIALS = env.variable(
            'SPREADSHEETS_SERVICE_JSON_CREDENTIALS',
            str,
            'spreadsheets_service_credentials',
        )
