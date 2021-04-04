import socket   # for sockets
import struct
import functools
import math


# This is called a declarator, it gets called for any function that has the
#    the @debug on the line prior to the function definition.
def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        """Wrapper function around a function to print out what the arguments and return value of that function"""
        args_repr = [repr(a) for a in args[1:]]                  # string list of all the non-key word arguments
        kwargs_repr = ["%s=%s" % (k, repr(v)) for k, v in kwargs.items()]  # string list of all the keyword arguments
        signature = ", ".join(args_repr + kwargs_repr)           # concat all the arguments
        print("Calling %s(%s)"% (func.__name__, signature))
        value = func(*args, **kwargs)
        print("%s returned %s" % (repr(func.__name__), repr(value)))           # print out the return value of the function as a string
        return value          # Make sure to return the value that the function returned
    return wrapper_debug

def getValue(func):
    @functools.wraps(func)
    def wrapper_getValue(self, cmd):
        resp = None
        try:
            reply = self.transaction(cmd, data=None)
            resp_cmd = chr ( reply[0] )
            if resp_cmd != cmd:
                raise Exception('BadResponse')
            resp = func(reply[1:])
        except Exception as e:
            print("ERROR: %s: %s: %s" % (cmd, repr(reply[1:]), str(e)))
            raise e
        return resp

class AGCMode(object):
    """
    It's easier to set the AGCMode as it's own datatype so that
    it can be handled as a string or an integer however it needs to
    """
    def __init__(self, val):
        self.val = None
        if type(val) == type(0):  # Type int
            if val < 0:
                raise Exception('BadMode')
            elif val > 3:
                raise Exception('BadMode')
            self.val = val
        elif type(val) == type('string'):  # Type string
            if val == 'AGC_FAST':
                self.val = 3
            elif val == 'AGC_MEDIUM':
                self.val = 2
            elif val == 'AGC_SLOW':
                self.val = 1
            elif val == 'AGC_OFF':
                self.val = 0
            elif val == '3':
                self.val = 3
            elif val == '2':
                self.val = 2
            elif val == '1':
                self.val = 1
            elif val == '0':
                self.val = 0
            else:
                raise Exception('BadMode')
        else:
            raise Exception('BadType')
    def __str__(self):
        """Converting the type to a string"""
        mode = "AGC_OFF"
        if self.val == 3:
            mode = "AGC_FAST"
        elif self.val == 2:
            mode = "AGC_MEDIUM"
        elif self.val == 1:
            mode = "AGC_SLOW"
        return mode
    def __int__(self):
        """Handling the type as an integer"""
        return self.val

class MyOMNI(object):
    """This class is to communicate with the OMNI across the network
    The request/response was figured out from
    https://github.com/Hamlib/Hamlib/blob/master/rigs/tentec/omnivii.c
    and
    http://www.tentec.com/wp-content/uploads/2016/05/tt_588_program_ref_v1.009.pdf
    """

    @debug
    def __init__(self, hostname="omni", port=50020):
        """The init method can take named parameters with defaults as follows
    hostname="omni"
    port=50020
    """
        # Create an element called "s" to hold our socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(2)
        # We seem to need a start sequence when sending commands
        self.startcmd = "09"
        # A couple more elements to hold our destination
        self.destination = (hostname, port)
        self.cmd2field = {
      "A": {
          "label": "vfoA",
          "unpack": lambda x: struct.unpack("!L", x)[0],
          "len": 4
          },
      "B": { 
          "label": "vfoB",
          "unpack": lambda x: struct.unpack("!L", x)[0],
          "len": 4
          },
      "G": { 
          "label": "agc",
          "unpack": lambda x: AGCMode(x[0]-ord('0')),
          "len": 1
          },
      "H": { 
          "label": "sql",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "I": { 
          "label": "rfgain",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "J": { 
          "label": "att",
          "unpack": lambda x: (x[0]-ord('0'))*6,
          "len": 1
          },
      "K": { 
          "label": "noise",
          "unpack": self.unpack_noise,
          "len": 3
          },
      "L": {
         "label": "rit_xit",
          "unpack": self.unpack_ritxit,
          "len": 3
         },
      "M": { 
          "label": "radio_mode",
          "unpack": self.unpackMode,
          "len": 2
          },
      "N": { 
          "label": "split_state",
          "unpack": lambda x: "Off" if x[0] == 0 else "On",
          "len": 1
          },
      "P": { 
          "label": "passband",
          "unpack": lambda x: struct.unpack("!H", x)[0],
          "len": 2
          },
      "U": { 
          "label": "volume",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "W": { 
          "label": "rx_filter",
          "unpack": self.unpack_filter,
          "len": 1
          },
      "S": { 
          "label": "strength",
          "unpack": self.unpack_signal,
          "len": 4
          },
      "F": { 
          "label": "strength",
          "unpack": self.unpack_signal,
          "len": 4
          },
      "C1A": { 
          "label": "audio_source",
          "unpack": self.unpack_au_source,
          "len": 1
          },
      "C1B": { 
          "label": "keyloop",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "T": { 
          "label": "eth_settings",
          "unpack": self.unpack_eth,
          "len": 18
          },
      "C1C": { 
          "label": "cw_time",
          "unpack": lambda x: x[0] + 3,
          "len": 1
          },
      "C1D": { 
          "label": "mic_gain",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1E": { 
          "label": "line_gain",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1F": { 
          "label": "speech_proc",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1G": { 
          "label": "ctcss_tone", # Who's going to use this rig for FM?
          "unpack": lambda x: x[0],
          "len": 1
          },
      "C1H": { 
          "label": "rx_eq",
          "unpack": lambda x: int( (x[0]-1)/3.097560975 ) - 20,
          "len": 1
          },
      "C1I": { 
          "label": "tx_eq",
          "unpack": lambda x: int( (x[0]-1)/3.097560975 ) - 20,
          "len": 1
          },
      "C1J": { 
          "label": "xmit_rolloff",
          "unpack": lambda x: (x[0] * 10) + 70,
          "len": 1
          },
      "C1K": { 
          "label": "t_r_delay",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1L": { 
          "label": "sidetone_freq",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1M": { 
          "label": "cw_delay",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1N": { 
          "label": "xmit_enable",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C1O": { 
          "label": "sideband_bw",
          "unpack": lambda x: 2500 if x[0] == 8 else 4000-(x[0] * 200) if x[0] < 8 else 4000-((x[0]-1)*200),
          "len": 1
          },
      "C1P": { 
          "label": "auto_tuner",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C1Q": { 
          "label": "sidetone_vol",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1R": { 
          "label": "spot_vol",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1S": {
         "label": "fsk_mark",
          "unpack": lambda x: x[0],
          "len": 1
         },
      "C1T": { 
          "label": "if_filter",
          "unpack": self.unpack_if,
          "len": 2
          },
      "C1U": { 
          "label": "if_filter_enable",
          "unpack": self.unpack_if_filter_enable,
          "len": 1
          },
      "C1V": { 
          "label": "antenna",
          "unpack": lambda x: x[0],
          "len": 1
          },
      "C1W": { 
          "label": "monitor",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C1X": { 
          "label": "power",
          "unpack": lambda x: int( ((x[0]/127.0)*100)+0.5 ), # we can get the fwd/rev power from ?S, ignore it from here
          "len": 3
          },
      "C1Y": { 
          "label": "spot",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C1Z": { 
          "label": "preamp",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2A": { 
          "label": "tuner",
          "unpack": self.unpack_tune_state,
          "len": 1
          },
      "C2B": { 
          "label": "split_state2",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2C": { 
          "label": "vox_trip",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C2D": { 
          "label": "anti_vox",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C2E": { 
          "label": "vox_hang",
          "unpack": lambda x: (x[0]/127.0),
          "len": 1
          },
      "C2F": { 
          "label": "cw_keyer_mode",
          "unpack": self.unpack_keyer,
          "len": 1
          },
      "C2G": { 
          "label": "cw_weight",
          "unpack": lambda x: (x[0]/127.0)/2.0,
          "len": 1
          },
      "C2H": { 
          "label": "manual_notch",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2I": { 
          "label": "manual_notch_freq",
          "unpack": lambda x: (40*x[0])+20,
          "len": 1
          },
      "C2J": { 
          "label":  "manual_notch_width",
          "unpack": lambda x: x[0]*( (315-10) / (127-1) ),
          "len": 1
          },
      "C2K": { 
          "label":  "cw_2_xmit",
          "unpack": lambda x: x[0],
          "len": 1
          },
      "C2L": { 
          "label": "keyer_speed",
          "unpack": lambda x:  int( (x[0] * 63/127)+0.5),
          "len": 1
          },
      "C2M": { 
          "label": "vox",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2N": { 
          "label": "display",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2O": { 
          "label": "speaker",
          "unpack": lambda x: False if x[0] == 0 else True,
          "len": 1
          },
      "C2P": { 
          "label": "trip_gain" # Doesn't seem to be supported by the Omni-Vii
          },
      "VER": {
          "label": "version"
      }
        }


    @debug
    def sendQuery(self, msg):
        # Remember destination is a list already of (host, port)
        msg = "%s?%s\r" % (self.startcmd, msg)
        print ("    Debug msg 01--> " + repr(msg)) #diagnostic message
        bytes_sent = self.s.sendto(msg.encode(), self.destination) # Using encode to convert to a byte string
        return (bytes_sent)
  
    @debug
    def recv(self, buff_len=1024):
        """Receive up to buff_len bytes from socket.  buffer will be of type bytes.  Referencing a particular
        position in the byte string will return the byte as an integer.
        """
        buffer = self.s.recv(buff_len)
        return (buffer)

    @debug
    def transaction(self, cmd, data=None):
        """Sends the Omni a query using the command cmd and reads back the response.
        """
        reply = None
        msg = cmd
        if data != None:
            msg += data
        try:
            self.sendQuery(msg)
            data = self.recv()
            if cmd[0] == 'C':
                resp_cmd = data[0:3].decode()
                reply = data[3:]
            else:
                resp_cmd = chr( data[0] )
                reply = data[1:]
            if resp_cmd != cmd:
                raise Exception('BadResponse')
        except Exception as e:
            print ('ERROR: transaction: %s' % (str(e)) )
        return(reply)

    @debug
    def newRecv(self):
        response = dict()
        buffer = self.recv()
        while len(buffer) > 0:
            data_len = -1
            field = None
            if buffer[0] == 0:
               # The sequence is terminated by a null character, skip it
                buffer = buffer[1:]
            elif chr( buffer[0] ) == 'C':
                # The fields that begin with a C are 3 characters in length
                field = buffer[0:3].decode()
                data_start = 3
                data_len = self.cmd2field[field].get('len', -1)
            elif chr( buffer[0] ) == "V":
                # Version string is kinda tricky since it's terminated by a null
                field = buffer[0:3].decode()
                # We will handle movement through the buffer so flag it to skip that part further down
                data_start = 4
                data_end = buffer.find(b'\x00')
                data = buffer[ data_start:data_end ]
                value = data.decode()
                # move the buffer up past the null and past the field sep. ('\r')
                buffer = buffer[data_end + 1 + 1:]
            else:
                field = chr( buffer[0] )
                data_start = 1
                data_len = self.cmd2field[field].get('len', -1)

            if data_len > 0:
                # Validate we are properly terminated
                #print("DEBUG: data_len: %d" % data_len)

                data_end   = data_start + data_len
                if buffer[data_end] != ord('\r'):
                    print("DEBUG:BADDATA: (%s)(%d:%d): " % (field, data_len, data_end), repr(buffer[data_end]))
                    raise Exception('BadData')
                data = buffer[ data_start:data_end ]
                value = self.cmd2field[ field ]["unpack"]( data )
                # Move to the next field
                buffer = buffer[data_end+1:]
            if field != None:
                #print("DEBUG: %s" % field)
                if field == 'U':
                    print("DEBUG: VOLUME")
                if field == 'W':
                    print("DEBUG: RX FILTER")
                if field == 'T':
                    print("DEBUG: ETHERNET")
                label = self.cmd2field[field]['label']
                response[label] = value
            #print("DEBUG: buffer_len: %d" % len(buffer))
        return response

    
    @debug
    def getFreq(self, VFO):
        # Response will be <VFO>B1B2B3B4
        #   Where <VFO> will be the VFO queried
        #   B1B2B3B4 will be a 4 byte representation of the frequency
        freq = self.transaction(VFO)
        if freq != None:
            # Use the unpack to extract out all 4 bytes of the Integer for the frequency
            freq = self.unpack_word(freq[:-1])
        return freq

    @debug
    def getMainFreq(self):
        return self.getFreq('A')

    @debug
    def getSubFreq(self):
        return self.getFreq('B')

    @debug
    def getAGCMode(self):
        """Queries for the AGC mode.  Response will be G<d> where <d> is the ascii representation of a number
        0-3.  This matches for AGC to be off, slow, medium or fast
        """
        mode = None
        reply = self.transaction('G')
        if reply != None:
            mode = AGCMode( chr( reply[0][0] ) )
        return(mode)
    
    @debug
    def getStrength(self):
        try:
            reply = self.transaction('S')

            # top bit of of the 2nd byte will be set if TX
            if (reply[0] & 0x80) == 0x80:
                # If the rig is in TX the response should be
                #   byte1 == foward power
                #   byte2 == reflected power
                print("  DEBUG:Transmitting")
                swr = calc_swr(reply[0] & 0x7f, reply[1])

                if reply[1] > 0:
                    reflected = reply[1] - 1
                else:
                    reflected = 0
                strength = (reply[0] & 0x7f) - reflected # Transmit Power
                print("  DEBUG: reflected:{reflected} strength: {strength}")
                # convert watts to dbM
                if strength > 0:
                    val = (10 * int(math.log10(strength))) + 30
                    val += 73
                else:
                    val = 0
                print("  DEBUG: Strength: %duV" % val)
                # FIXME - What do we return?
            else:
                # Response for the receiving is in the form S0944 for 44 db over S9 in ASCII
                print("  DEBUG:Receiving")
                # Each byte is an ASCII character of a digit
                # Convert the bytes to strings and cast to an integer
                s_meter = int( reply[0:2].decode() )
                db_over = int( reply[2:3].decode() )
                print('  DEBUG: %s over S%s' % (db_over, s_meter))
                db_s9_rel = (s_meter - 9) * 6 # convert S meter to dBS9 relative
                print('  DEBUG: db relative to S9: %s', db_s9_rel)
                # FIXME - What do we return?
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(None)

    @debug
    def getVolume(self):
        """Returns the AF setting
        """
        volume = 0
        reply = self.transaction('U')
        if reply != None:
            volume = float(reply[0])/127.0
        return(volume)

    @debug
    def getPower(self):
        power = 0.0
        reply = self.transaction('I')
        if reply != None:
            power = float(reply[0])/127.0
        return(power)

    @debug
    def getATT(self):
        att = 0.0
        reply = self.transaction('J')
        if reply != None:
            # Response is an ascii 1, 2 or 3
            #   1 => 6
            #   2 => 12
            #   3 => 18
            att = (reply[0]-ord('0')) * 6  # Turns out this is faster than casting int(chr(x))
        return(att)

    @debug
    def getSQL(self):
        sql = 0.0
        reply = self.transaction('H')
        if reply != None:
            sql = float(reply[0])/127.0
        return(sql)

    @debug
    def getGeneric(self, cmd, data=None):
        resp = None
        reply = self.transaction(cmd, data=data)
        print("RESPONSE: %s: %s" % ( resp_cmd, repr(reply)))


    @staticmethod
    def calc_swr(b1, b2):
        swr = 99.9

        fwd = float(b1 & 0x7f)
        refl = float(b2)
        print("  DEBUG:fwd:%.3f -> refl:%.3f" % ( fwd, refl ))
        if fwd > 0.0:
            val = refl / fwd
            swr = (1.0 + val) / (1.0 - val)
        return swr

    @staticmethod
    def unpack_word(val):
        return struct.unpack(">I", val)[0]

    @staticmethod
    def unpack_noise(val):
        return { "nb": val[0], "nr": val[1], "an": val[2] }

    @staticmethod
    def unpack_ritxit(val):
        ret = { "xit": 0, "rit": 0 }
        if val[0] == 1:
            ret["rit"] = (val[2] * 256) | val[3]
        elif val[0] == 2:
            ret["xit"] = (val[2] * 256) | val[3]
        else:
            x = (val[1] * 256) | val[2]
            ret = { "xit": x, "rit": x }
        return ret

    @staticmethod
    def radioMode(val):
        modes = {
            0: "AM",
            1: "USB",
            2: "LSB",
            3: "CW",
            5: "CWR",
            4: "FM"
        }
        return modes.get(val, None)

    @debug
    def unpackMode(self,val):
        ret = dict()
        # val will be 2 bytes in length, each byte will be an integer but in ascii
        # (x-ord('0') for x in val) => for each byte in val, convert char to integer
        # zip( listA, listB ) => creates a new list interpolating elements from listA with listB 
        for k,v in zip( ("vfoA_mode", "vfoB_mode"), (x-ord('0') for x in val) ):
            # 'k' will either be vfoA_mode or vfoB_mode
            # 'v' will be the integer value of either the first or second byte
            # Lookup the coresponding mode for the value of the 'v' byte
            mode = self.radioMode(v)
            # Make sure it's a valid mode (i.e. a number between 0-5
            if v == None:
                raise Exception("BadMode")
            ret[k] = mode
        return ret

    @staticmethod
    def matchFilter(width):
        filters = {
            0: 12000,
            1: 9000,
            2: 8000,
            3: 7500,
            4: 7000,
            5: 6500,
            6: 6000,
            7: 5500,
            8: 5000,
            9: 4500,
            10: 4000,
            11: 3800,
            12: 3600,
            13: 3400,
            14: 3200,
            15: 3000,
            16: 2800,
            17: 2600,
            18: 2500,
            19: 2400,
            20: 2200,
            21: 2000,
            22: 1800,
            23: 1600,
            24: 1400,
            25: 1200,
            26: 1000,
            27: 900,
            28: 800,
            29: 700,
            30: 600,
            31: 500,
            32: 450,
            33: 400,
            34: 350,
            35: 300,
            36: 250,
            37: 200
        }
        return filters.get(width, None)

    def unpack_filter(self, val):
        filter = self.matchFilter(val[0])
        if filter == None:
            raise Exception('BadFilter')
        return filter

    @staticmethod
    def unpack_eth(val):
        # b'001945001602\x00\xc0\xa8\x01'
        # MAC Address, 
        # RIP In Progress, 
        # RIP IP, 
        # Compression Level Supported
        mac_addr          = val[0:12].decode()
        rip_in_use        = val[12]
        rip_ip            = socket.inet_ntoa(val[13:17])
        compression_level = val[17]
        return { 'mac': mac_addr, 'rip': rip_in_use, 'ip': rip_ip, 'compression': compression_level }

    @staticmethod
    def matchAudioSource(val):
        source = {
            0: "MIC",
            1: "LINE",
            2: "BOTH"
         }
        return source.get(val, None)

    @debug
    def unpack_au_source(self, val):
        source = self.matchAudioSource(val[0])
        if source == None:
            raise Exception('BadSource')
        return source
    @staticmethod
    def unpack_signal(val):
        ret = dict()
        if val[0] & 0x80 == 0x80:
            # Transmitting
            fwd = val[0] & 0x7f
            rev = val[1]
            ret['swr'] = calc_swr(fwd, rev)

            strength = fwd - rev
            dbW = (10 * int(math.log10(strength))) + 30
            ret['dbm'] = dbW + 73
        else:
            # Receiving
            s_meter = int( val[0:2].decode() )
            db_over = int( val[2:3].decode() )
            ret['dbS9rel'] = (s_meter - 9) * 6 # convert S meter to dBS9 relative
        return ret

    @staticmethod
    def unpack_if(val):
        if_sel = {
            0: "20kHz",
            1: "6kH",
            2: "2.5kHz",
            3: "500H",
            4: "300Hz"
         }
        return if_sel.get(val[0], "Auto")

    @staticmethod
    def unpack_if_filter_enable(val):
        ret = {"300": False, "500": False}
        if val[0] & 0x01 == 0x01:
            ret["300"] = True
        if val[0] & 0x02 == 0x02:
            ret["500"] = True
        return ret

    @staticmethod
    def unpack_tune_state(val):
        ret = { 
            "enabled": False,
            "tuning": False,
            "tuned": False
         }
        if val[0] & 0x01 == 0x01:
            ret['enabled'] = True
        if val[0] & 0x02 == 0x02:
            ret['tuning'] = True
        if val[0] & 0x04 == 0x04:
            ret['tuned'] = True
        return ret

    @staticmethod
    def unpack_keyer(val):
        ret = {
            "curtis_mode_a": False,
            "curtis_mode_b": False,
            "keyer": False
        }
        if val[0] & 0x01 == 0x01:
            ret['curtis_mode_a'] = True
        if val[0] & 0x02 == 0x02:
            ret['curtis_mode_b'] = True
        if val[0] & 0x04 == 0x04:
            ret['keyer'] = True
        return ret
    
    @debug
    def getSettings(self):
        response = dict()
        all_settings = self.queryAll()
        for (c, value) in all_settings.items():
#            if self.cmd2field.get(c, None) != None:
#                f = self.cmd2field[c]
#                response[f] = value
            pass
        response = all_settings
        return response

    @debug
    def queryAll(self):
        reply = dict()
        try:
            self.sendQuery('*')
            reply = self.newRecv()
        except Exception as e:
            print("ERROR: queryAll: %s" % str(e))
            raise e
        return reply

    @debug
    def getAll(self):
        resp = dict()
        try:
            self.sendQuery('*')
            reply = self.recv()
            # FIXME: We need to figure a better way to parse through the response
            #    There are responses that could very well map into a 13 which happens to be the separater
            #    so splitting on the \r is a bad idea.  Works for now but this will have to be redone
            for line in reply.split(b'\r'):
                field = None
                if line[0] == 0:
                    # The sequence is terminated by a null character, skip it
                    pass
                elif line[0] == 7:
                    # This is odd that it just started showing up
                    pass
                elif chr( line[0] ) == 'C':
                    # The fields that begin with a C are 3 characters in length
                    field = line[0:3].decode()
                    data = line[3:]
                elif chr( line[0] ) == 'V':
                    # There is a version string
                    field = line[0:3].decode()
                    data = line[0:-1] # Version string is Null terminated, we don't want the null
                else:
                    field = chr( line[0] )
                    data = line[1:]

                if field != None:
                    resp[field] = data

        except Exception as e:
            print("ERROR: getAll: %s" % str(e))

        for field in resp:
            if field == 'A':
                # VFO A Freq.
                resp[field] = self.unpack_word(resp[field])
            elif field == 'B':
                # VFO B Freq.
                resp[field] = self.unpack_word(resp[field])
            elif field ==  'F':
                pass
            elif field ==  'G':
                resp[field] = AGCMode( chr(resp[field][0]) )
            elif field ==  'H':
                # SQL
                resp[field] = float(resp[field][0])/127.0
            elif field ==  'I':
                # Power
                resp[field] = float(resp[field][0])/127.0
            elif field ==  'J':
                # ATT
                resp[field] = (resp[field][0] - ord('0')) * 6
            elif field ==  'K': # noise
                pass
            elif field ==  'L': # rit_xit
                # resp[field] = self.unpack_rit_xit(resp[field])
                pass
            elif field ==  'M': # radio_mode
                # resp[field] = self.unpackMode(resp[field])
                pass
            elif field ==  'N': # split_state
                pass
            elif field ==  'P': # passband
                pass
            elif field ==  'S': # Signal Strength
                pass
            elif field ==  'T': # xmit/eth_settings
                pass
            elif field ==  'U': # volume
                # Volume
                resp[field] = float(resp[field][0])/127.0
            elif field ==  'V': 
                pass
            elif field ==  'W': # rx_filter
                pass
            elif field == "C1A": # audio_source
                resp[field] = resp[field][0]
            elif field == "C1B": # keyloop
                resp[field] = resp[field][0]
            elif field == "C1C": # cw_time
                resp[field] = resp[field][0]
            elif field == "C1D": # mic_gain
                resp[field] = resp[field][0]
            elif field == "C1E": # line_gain
                resp[field] = resp[field][0]
            elif field == "C1F": # speech_proc
                resp[field] = resp[field][0]
            elif field == "C1G": # ctcss_tone
                resp[field] = resp[field][0]
            elif field == "C1H": # rx_eq
                resp[field] = resp[field][0]
            elif field == "C1I": # tx_eq
                resp[field] = resp[field][0]
            elif field == "C1J": # xmit_rolloff
                resp[field] = resp[field][0]
            elif field == "C1K": # t_r_delay
                resp[field] = resp[field][0]
            elif field == "C1L": # sidetone_freq
                resp[field] = resp[field][0]
            elif field == "C1M": # cw_delay
                resp[field] = resp[field][0]
            elif field == "C1N": # xmit_enable
                resp[field] = resp[field][0]
            elif field == "C1O": # sideband_bw
                resp[field] = resp[field][0]
            elif field == "C1P": # auto_tuner
                if resp[field][0] == 1:
                    resp[field] = True
                else:
                    resp[field] = False
            elif field == "C1Q": # sidetone_vol
                resp[field] = resp[field][0]
            elif field == "C1R": # spot_vol
                resp[field] = resp[field][0]
            elif field == "C1S": # fsk_mark
                resp[field] = resp[field][0]
            elif field == "C1T": # if_filter
                resp[field] = resp[field][0]
            elif field == "C1U": # if_filter_enable
                resp[field] = resp[field][0]
            elif field == "C1V": # antenna
                resp[field] = resp[field][0]
            elif field == "C1W": # monitor
                resp[field] = resp[field][0]
            elif field == "C1X": # power
                resp[field] = resp[field][0]
            elif field == "C1Y": # spot
                resp[field] = resp[field][0]
            elif field == "C1Z": # preamp
                resp[field] = resp[field][0]
            elif field == "C2A": # tuner
                resp[field] = resp[field][0]
            elif field == "C2B": # split_state2
                resp[field] = resp[field][0]
            elif field == "C2C": # vox_trip
                resp[field] = resp[field][0]
            elif field == "C2D": # anti_vox
                resp[field] = resp[field][0]
            elif field == "C2E": # vox_hang
                resp[field] = resp[field][0]
            elif field == "C2F": # cw_keyer_mode
                resp[field] = resp[field][0]
            elif field == "C2G": # cw_weight
                resp[field] = resp[field][0]
            elif field == "C2H": # manual_notch
                if resp[field][0] == 1:
                    resp[field] = True
                else:
                    resp[field] = False
            elif field == "C2I": # manual_notch_freq
                resp[field] = resp[field][0]
            elif field == "C2J": # manual_notch_width
                resp[field] = resp[field][0]
            elif field == "C2K": # cw_2_xmit
                resp[field] = resp[field][0]
            elif field == "C2L": # keyer_speed
                resp[field] = int(resp[field][0]/2)
            elif field == "C2M": # vox
                if resp[field][0] == 1:
                    resp[field] = True
                else:
                    resp[field] = False
            elif field == "C2N": # display
                if resp[field][0] == 1:
                    resp[field] = True
                else:
                    resp[field] = False
            elif field == "C2O": # speaker
                if resp[field][0] == 1:
                    resp[field] = True
                else:
                    resp[field] = False
            elif field == "C2P": # trip_gain
                pass
            elif field == "VER": # VERSION
                resp[field] = resp[field].decode()
            else:
                raise Exception('UnknownCMD_%s' % repr(field))
        return resp


