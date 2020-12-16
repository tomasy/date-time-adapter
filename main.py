"""DateTime addon for WebThings Gateway."""

from os import path
import functools
import logging
import signal
import sys
import time
import traceback

sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from pkg.date_adapter import DateTimeAdapter


_DEBUG = False
_ADAPTER = None

print = functools.partial(print, flush=True)


def cleanup(signum, frame):
    """Clean up any resources before exiting."""
    logging.info('CLEANUP exception handler')
    if _ADAPTER is not None:
        _ADAPTER.close_proxy()

    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(
        level=10
        , format="%(filename)s:%(lineno)s %(levelname)s %(message)s"
        , stream = sys.stdout
    )
    logging.info('Starting DateTime Addon')

    try:
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)
        _ADAPTER = DateTimeAdapter(verbose=_DEBUG)

        # Wait until the proxy stops running, indicating that the gateway shut us
        # down.
        while _ADAPTER.proxy_running():
            time.sleep(2)
    except Exception as ex:
        print('EXECPTION')
        print(ex)
        print(ex.args)
        print(traceback.format_exception(None, # <- type(e) by docs, but ignored
                                         ex, ex.__traceback__), file=sys.stdout)
    logging.info('STOPPED DateTime Addon')
