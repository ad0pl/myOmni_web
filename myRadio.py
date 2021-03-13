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

        # Loop through all the fields check to see if the getAll has it set
        #    Set a field of this object with it's approprate value
        for (f, c) in field2cmd.items():
            if all_settings.get(c, None) != None:
                setattr(self, f, all_settings[c])







