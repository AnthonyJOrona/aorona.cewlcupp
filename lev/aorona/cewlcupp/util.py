def init_logger(logging):
    logging.basicConfig()
    logger = logging.getLogger("lev")
    logger.setLevel(logging.DEBUG)
    return logger