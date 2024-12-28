import subprocess
import logging
import inspect
import argparse
from hackclock.config import configuration

logger = logging.getLogger('clock')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(console)

class ProcessStatus:
    RUNNING = "running"
    TERMINATED = "terminated"
    NOT_STARTED = "not_started"

class Clock:
    name = 'clock'
    keyword = 'clock'
    sourceFile = configuration.get('python_file')
    eventLoop = None

    def __init__(self):
        self.eventLoop = None
        self.stderr = None

    def __del__(self):
        self.close()

    def status(self):
        if self.eventLoop:
            return ProcessStatus.RUNNING if self.eventLoop.poll() is None else ProcessStatus.TERMINATED
        else:
            return ProcessStatus.NOT_STARTED

    def stop(self):
        logger.info("Terminating clock loop")
        if self.eventLoop:
            self.eventLoop.terminate()
            self.eventLoop.wait()

    def start(self):
        parser = argparse.ArgumentParser(description="The Hack Clock's custom code")
        parser.add_argument('--config', type=str, default='/etc/hack-clock.conf', help='path to configuration file')
        args = parser.parse_args()

        logger.info("Starting clock event loop")
        logger.info(self.sourceFile)
        logger.info(args.config)

        self.eventLoop = subprocess.Popen(["python3", self.sourceFile, "--config", args.config], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def restart(self):
        if self.status() == ProcessStatus.RUNNING:
            self.stop()
        self.start()

    def failures(self):
        if self.status() == ProcessStatus.TERMINATED and not self.stderr:
            self.stderr = self.eventLoop.stderr.read()
        elif self.status() != ProcessStatus.TERMINATED:
            self.stderr = None

        return self.stderr

    def setup(self, app):
        logger.info("Loading clock event loop")

        self.routes = app

        for other in app.plugins:
            if not isinstance(other, Clock):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another instance of the clock driver running!")

        self.start()

    def apply(self, callback, context):
        logger.info(context)
        #        conf = context.get('clock') or {}
        conf = getattr(context, 'config', {})  # Use context.config if it exists, otherwise an empty dict

        keyword = conf.get('keyword', self.keyword)

        args = inspect.getfullargspec(callback).args
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = self
            rv = callback(*args, **kwargs)
            return rv

        return wrapper

    def close(self):
        self.stop()

class PluginError(Exception):
    pass

Plugin = Clock

