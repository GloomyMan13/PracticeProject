import datetime
date = datetime.datetime.now().strftime('%D-%M-%Y %H:%M:%S')

config = {'version': 1,
          'formatters': {
              'file': {
                  'format': 'At %(asctime)s: %(levelname)s: %(message)s'
              }
          },
          'handlers': {
              'consolelog': {
                  'class': 'logging.StreamHandler',
                  'level': 'INFO',
                  'formatter': 'file',
                  'stream': 'ext://sys.stdout'
              },
              'filelog': {
                  'class': 'logging.handlers.RotatingFileHandler',
                  'level': 'WARNING',
                  'formatter': 'file',
                  'filename': './logs/logs.log',
                  'maxBytes': 3086,
                  'backupCount': 3
              }
          },
          'loggers': {
              'info_log': {
                  'level': 'INFO',
                  'handlers': ['consolelog'],
                  'propagete': 'False'
              },
              'debug_log': {
                  'level': 'WARNING',
                  'handlers': ['filelog'],
                  'propagete': 'False'
              }
          }
          }
