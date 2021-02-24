from example_timer import RepeatedTimer
from myOmni import MyOMNI
from time import sleep

mo = MyOMNI(hostname="k8hsq.no-ip.biz", port=50020)
rt = RepeatedTimer(2, mo.getAll)

sleep(10)

rt.stop()
