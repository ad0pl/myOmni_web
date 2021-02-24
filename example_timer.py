from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        """Intialize the Timer object, set the fields to store the interval, the function to call and any arguments"""
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        """Get called after an interval of second, 
            we turn off the timer and start it again and call our function)
        """
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """Check to make sure that we're not already running and if not create a Timer object 
        to kick off every interval (seconds) and call our run function
            As well as mark that we've been called already"""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Disable our timer and turn ourself off"""
        self._timer.cancel()
        self.is_running = False

from time import sleep

def hello(name):
    print("Hello %s!" % name)

if __name__ == "__main__":
    print("starting...")
    rt = RepeatedTimer(2, hello, "World") # it auto-starts, no need of rt.start()
    try:
        sleep(10) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!
