import socket   # for sockets
import sys      # for exit
import struct
import functools
import math

# This is called a declarator, it gets called for any function that has the
#    the @debug on the line prior to the function definition.
def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args[1:]]                  # 1
        kwargs_repr = ["%s=%s" % (k, repr(v)) for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print("Calling %s(%s)"% (func.__name__, signature))
        value = func(*args, **kwargs)
        print("%s returned %s" % (repr(func.__name__), repr(value)))           # 4
        return value
    return wrapper_debug

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
    """
  # For python classes, the __init__ method/function is always called when a new
  #   Object is created
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
        print ('Trace 22')

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
        msg = cmd
        if data != None:
            msg += data
        try:
            self.sendQuery(msg)
            data = self.recv()
        except Exception as e:
            print ('ERROR: %s' % (str(e)) )
        return(data)

    @debug
    def getFreq(self, VFO):
        # Response will be <VFO>B1B2B3B4
        #   Where <VFO> will be the VFO queried
        #   B1B2B3B4 will be a 4 byte representation of the frequency
        freq = None
        try:
            reply = self.transaction(VFO)
            resp_cmd = chr( reply[0] )
            if resp_cmd != VFO:
                raise Exception("BadResponse")
            # Use the unpack to extract out all 4 bytes of the Integer for the frequency
            freq     = unpack_word(reply[1:5])
        except Exception("BadResponse"):
            # If we get a bad response from the radio, just return nothing
            pass
        except Exception as e:
            print("ERROR:getFreq: %s" % str(e))
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
        try:
            reply = self.transaction('G')
            if len(reply) < 4:
                raise Exception("SmallResponse")
            resp_cmd = chr( reply[0] )
            if resp_cmd != 'G':
                raise Exception("BadResponse")

            lvlbuf = AGCMode( chr( reply[1] ) )
            mode = str(lvlbuf)
        except Exception("BadResponse"):
            pass
        except Exception as e:
            print("ERROR:getAGCMode: %s" % str(e))
        return(mode)
    
    @debug
    def getStrength(self):
        try:
            reply = self.transaction('S')
            resp_cmd = chr( reply[0] )

            if resp_cmd != 'S':
                raise Exception("BadResponse")

            # top bit of of the 2nd byte will be set if TX
            if (reply[1] & 0x80) == 0x80:
                # If the rig is in TX the response should be
                #   byte1 == foward power
                #   byte2 == reflected power
                print("  DEBUG:Transmitting")
                swr = calc_swr(reply[1] & 0x7f, reply[2])

                if reply[2] > 0:
                    reflected = reply[2] - 1
                else:
                    reflected = 0
                strength = (reply[1] & 0x7f) - reflected # Transmit Power
                print("  DEBUG: reflected:{reflected} strength: {strength}")
                # convert watts to dbM
                if strength > 0:
                    val = (10 * int(math.log10(strength))) + 30
                    val += 73
                else:
                    val = 0
                print("  DEBUG: Strength: %duV" % val)
            else:
                # Response for the receiving is in the form S0944 for 44 db over S9 in ASCII
                print("  DEBUG:Receiving")
                # Each byte is an ASCII character of a digit
                #    NOTE: reply[1] => lvlbuf[0] 
                lvlbuf = [ int( chr(x) ) for x in reply[1:5] ]

                s_meter = (lvlbuf[0] * 10) + lvlbuf[1] # int(reply[1:3].decode())
                db_over = (lvlbuf[2] * 10) + lvlbuf[3] # int(reply[3:5].decode())
                print('  DEBUG: %s over S%s' % (db_over, s_meter))
                db_s9_rel = (s_meter - 9) * 6 # convert S meter to dBS9 relative
                print('  DEBUG: db relative to S9: %s', db_s9_rel)
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(None)

    @debug
    def getVolume(self):
        """Returns the AF setting
        """
        volume = 0
        try:
            reply = self.transaction('U')
            resp_cmd = chr( reply[0] )

            if resp_cmd != 'U':
                raise Exception("BadResponse")

            volume = float(reply[1])/127.0
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(volume)

    @debug
    def getPower(self):
        power = 0.0
        try:
            reply = self.transaction('I')
            resp_cmd = chr( reply[0] )

            if resp_cmd != 'I':
                raise Exception("BadResponse")

            power = float(reply[1])/127.0
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(power)

    @debug
    def getATT(self):
        att = 0.0
        try:
            reply = self.transaction('J')
            resp_cmd = chr( reply[0] )

            if resp_cmd != 'J':
                raise Exception("BadResponse")

            # Response is an ascii 1, 2 or 3
            #   1 => 6
            #   2 => 12
            #   3 => 18
            att = (reply[1]-ord('0')) * 6  # Turns out this is faster than casting int(chr(x))
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(att)

    @debug
    def getSQL(self):
        sql = 0.0
        try:
            reply = self.transaction('H')
            resp_cmd = chr( reply[0] )

            if resp_cmd != 'H':
                raise Exception("BadResponse")
            sql = float(reply[1])/127.0
        except Exception as e:
            print("ERROR: getStrength: %s" % str(e))
        return(sql)

    @debug
    def getGeneric(self, cmd, data=None):
        resp = None
        try:
            reply = self.transaction(cmd, data=data)
            resp_cmd = chr( reply[0] )
            if resp_cmd != cmd:
                raise Exception('BadResponse')
            buffer_len = len(reply[1:])
            print("RESPONSE: %s: %s" % ( resp_cmd, repr(reply[1:])))
        except Exception("BadResponse"):
            pass
        except Exception as e:
            print("ERROR:getGeneric: %s" % str(e))

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

    @debug
    def getAll(self):
        resp = dict()
        try:
            reply = self.transaction('*')
            for line in reply.split('\r'):
                field = None
                if line[0] == 0:
                    # The sequence is terminated by a null character, skip it
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
                resp[field] = unpack_word(all_settings[field])
            elif field == 'B':
                # VFO B Freq.
                resp[field] = unpack_word(all_settings[field])
            elif field ==  'F':
                pass
            elif field ==  'G':
                pass
            elif field ==  'H':
                # SQL
                all_settings[field] = float(all_settings[field][0])/127.0
            elif field ==  'I':
                # Power
                all_settings[field] = float(all_settings[field][0])/127.0
            elif field ==  'J':
                # ATT
                all_settings[field] = (all_settings[field][0] - ord('0')) * 6
            elif field ==  'K':
                pass
            elif field ==  'L':
                pass
            elif field ==  'M':
                pass
            elif field ==  'N':
                pass
            elif field ==  'P':
                pass
            elif field ==  'S':
                pass
            elif field ==  'T':
                pass
            elif field ==  'U':
                # Volume
                all_settings[field] = float(all_settings[field][0])/127.0
            elif field ==  'V':
                pass
            elif field ==  'W':
                pass
            else:
                raise Exception('UnknownCMD_%s' % field)
        return all_settings
