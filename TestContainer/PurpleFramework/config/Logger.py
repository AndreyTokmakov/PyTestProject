import logging.config
from logging import StreamHandler
from config.Configuration import Configuration

logging.config.fileConfig(fname=f'{Configuration.CONFIG_DIR}/logging.conf',
                          disable_existing_loggers=False)
NAME: str = "PurpleLog"


def getLogger():
    logger = logging.getLogger(NAME)
    logging.getLogger("paramiko.transport").setLevel(logging.WARNING)

    # FIXME: From 'requests'
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    # TODO: Check where its coming from ?
    logging.getLogger("faker.factory").setLevel(logging.WARNING)
    return logger


# TODO: Refactor
#       have to use 'config/logging.conf' somehow
def get_git_poller_logger() -> logging.Logger:
    handler: StreamHandler = logging.FileHandler('/tmp/polling.log')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger("GitPoller")
    logger.addHandler(handler)

    # Supress 'git.remote' and 'git.cmd' logs
    logging.getLogger("git.remote").setLevel(logging.WARNING)
    logging.getLogger("git.cmd").setLevel(logging.WARNING)

    return logger
