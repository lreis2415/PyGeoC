import logging
import sys


def log_subprocess_output(out):
    for line in iter(out.readline, b''):  # b'\n'-separated lines
        logging.info('Subprocess: %r', line)


# 2 handlers for the same logger:
h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.DEBUG)
# filter out everything that is above INFO level (WARN, ERROR, ...)
h1.addFilter(lambda record: record.levelno <= logging.INFO)

h2 = logging.StreamHandler(sys.stderr)
# take only warnings and error logs
h2.setLevel(logging.WARNING)
h2.addFilter(lambda record: record.levelno > logging.INFO)

logging.basicConfig(
    format='%(message)s',
    handlers=[
        h1, h2
    ],
    level=logging.INFO
)
