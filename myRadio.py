from myOmni import MyOMNI
from cmd2field import cmd2field
from field2cmd import field2cmd

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
        all_settings = self.rig.getAll()

        self.vfoA = self.rig.getMainFreq()
        vfoB





