from myOmni import MyOMNI
def getLevel(conn):
    conn.getStrength()
    conn.getAGCMode()
    conn.getVolume()
    conn.getPower()
    conn.getATT()
    conn.getSQL()
    
class Radio(object):
    def __init__(self, hostname="k8hsq.no-ip.biz", port=50020):
        self.rig = MyOMNI(hostname=hostname, port=port)
        self.vfoA = self.rig.getMainFreq()




