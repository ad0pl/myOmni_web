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
        all_settings = self.rig.getSettings()

        # Loop through all the fields check to see if the getAll has it set
        #    Set a field of this object with it's approprate value
        for (f, c) in field2cmd.items():
            if all_settings.get(f, None) != None:
                setattr(self, f, all_settings[f])

    def getEthernetSettings(self):
        # b'001945001602\x00\xc0\xa8\x01'
        # MAC Address, 
        # RIP In Progress, 
        # RIP IP, 
        # Compression Level Supported
        mac_addr          = self.rig.eth_settings[0:12].decode()
        rip_in_use        = self.rig.eth_settings[12]
        rip_ip            = socket.inet_ntoa(self.rig.eth_settings[13:17])
        compression_level = self.rig.eth_settings[17]
        return { 'mac': mac_addr, 'rip': rip_in_use, 'ip': rip_ip, 'compression': compression_level }

    def updateSettings(self):
        all_settings = self.rig.getSettings()
        for (f, c) in field2cmd.items():
            if all_settings.get(f, None) != None:
                if f == "radio_mode":
                    mode_a, mode_b = self.rig.unpackMode( all_settings[f])
                    setattr(self, 'vfoA_mode', mode_a)
                    setattr(self, 'vfoB_mode', mode_b)
                elif f == "eth_settings":
                    setattr(self, 'eth_settings', self.getEthernetSettings())
                else:
                    setattr(self, f, all_settings[f])







