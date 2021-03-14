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

    @debug
    def getAll(self):
        resp = dict()
        try:
            self.sendQuery('*')
            reply = self.recv()
            for line in reply.split(b'\r'):
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
                resp[field] = float(resp[field][0])/127.0
            elif field ==  'V':
                pass
            elif field ==  'W':
                pass
            elif field == "C1A":
                pass
            elif field == "C1B":
                pass
            elif field == "C1C":
                pass
            elif field == "C1D":
                pass
            elif field == "C1E":
                pass
            elif field == "C1F":
                pass
            elif field == "C1G":
                pass
            elif field == "C1H":
                pass
            elif field == "C1I":
                pass
            elif field == "C1J":
                pass
            elif field == "C1K":
                pass
            elif field == "C1L":
                pass
            elif field == "C1M":
                pass
            elif field == "C1N":
                pass
            elif field == "C1O":
                pass
            elif field == "C1P":
                pass
            elif field == "C1Q":
                pass
            elif field == "C1R":
                pass
            elif field == "C1S":
                pass
            elif field == "C1T":
                pass
            elif field == "C1U":
                pass
            elif field == "C1V":
                pass
            elif field == "C1W":
                pass
            elif field == "C1X":
                pass
            elif field == "C1Y":
                pass
            elif field == "C1Z":
                pass
            elif field == "C2A":
                pass
            elif field == "C2B":
                pass
            elif field == "C2C":
                pass
            elif field == "C2D":
                pass
            elif field == "C2E":
                pass
            elif field == "C2F":
                pass
            elif field == "C2G":
                pass
            elif field == "C2H":
                pass
            elif field == "C2I":
                pass
            elif field == "C2J":
                pass
            elif field == "C2K":
                pass
            elif field == "C2L":
                pass
            elif field == "C2M":
                pass
            elif field == "C2N":
                pass
            elif field == "C2O":
                pass
            elif field == "VER":
                pass
            else:
                raise Exception('UnknownCMD_%s' % field)
        return resp
