import logging, sys

def configure_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.handlers = [h]
