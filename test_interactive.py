#!/usr/bin/python3
handlers = {
        'a': 'getMainFreq',
        'b': 'getSubFreq',
        'g': 'getAGCMode',
        's': 'getStrength',
        'v': 'getVolume',
        'i': 'getPower',
        'j': 'getATT',
        'h': 'getSQL',
}

def getLevel():
    omni.getStrength()
    omni.getAGCMode()
    omni.getVolume()
    omni.getPower()
    omni.getATT()
    omni.getSQL()
if __name__ == "__main__":
    cr = '\r'
    crlf = '\r\n'

    try:
        # If we have a socket creation error within the MyOMNI __init__ function
        #    this will capture it.
        print('Socket to be Created - 76')
        omni = MyOMNI(hostname="k8hsq.no-ip.biz", port=50020)
        #omni = MyOMNI()
        print('Socket Created - 78')
    except socket.error:
        print ('Failed to create socket')
        sys.exit(1)

    while (True):
        try:
            z = input('Enter single letter message to send (Control-C to quit): '); 
            msg = z
            handler = handlers.get(z[0], None)
            if handler != None:
                ret_val = eval(f'omni.{handler}')()
                print("##############\n%s => %s\n##############" % ( handler, ret_val ))
            elif z[0] == 'l':
                getLevel()
            else:
                print('That command is not setup yet')
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)
        except TypeError:
            print("The message doesn't take arguments")

    sys.exit(0)