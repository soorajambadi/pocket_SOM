__author__ = 'tintin'

# config file for Celery Daemon

# default RabbitMQ broker
BROKER_URL = 'amqp://'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'

# specify location of log files
#CELERYD_LOG_FILE="logs/celery.log"

CELERY_RESULT_SERIALIZER = 'json'

# The command is inside pocket directory run.
# env/bin/celery -A manager.celery worker -l info
# env/bin/celery flower -A manager.celery --address=127.0.0.1 --port=5555