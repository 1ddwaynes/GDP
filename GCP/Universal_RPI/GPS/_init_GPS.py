import time
import SpeedCalculation
import _init_Serial
import threading


class numStore():
    def __init__(self):
        self.num_a = None
        self.num_b = None

    def numChange(self, a, b):
        self.num_a = a
        self.num_b = b

    def numStale(self, a , b):
        if self.num_a == a or self.num_b == b:
            return True

# class initGPS(threading.Thread):
class initGPS():
    def __init__(self):
        # threading.Thread.__init__(self)
        # number of satellites (can possible be used for strength of signal
        self.SatN = None
        # current latitude and longitude values
        self.c_lat_value = None
        self.c_lon_value = None
        # old latitude and longitude values
        self.o_lat_value = None
        self.o_lon_value = None
        # once start default to turned on
        self.collect = True
        self.empty = None

    def disable_GPS(self):
        collect = False

    def get_current_GPS_cord(self):
        return self.lat_value,self.lon_value

    def get_current_num_SatN(self):
        return self.SatN

    # serial data check, handshakes for certain data stream within serial
    # otherwise incorrect data can be passed, causing problems
    # could possible be expanded on or moved to _init_serial.py
    def check_instance(self, data):
        if b'Sat' in data:
            self.SatN = data
            self.waiting_satn = False
        if b'Lat' in data:
            self.c_lat_value = data
            self.waiting_lat = False
        if b'Lon' in data:
            self.c_lon_value = data
            self.waiting_lon = False
        else:
            self.empty = True

    def old_instance(self):
        self.o_lat_value = self.c_lat_value
        self.o_lon_value = self.c_lon_value

    # threading
#     def run(self):
#         _serial = _init_Serial.initSerial()
#         try:
#             while True:
#                 temp_holder = _serial.serial_event(str)
#                 self.check_instance(temp_holder)
#
# if __name__ == '__main__':
#     _serial = _init_Serial.initSerial()
#     try:
#         _serial.

def RUN_GPS():

        # initialize variables
        _serial = _init_Serial.initSerial()
        GPS = initGPS()

        # connects to serial if serial is NOT connected
        if _serial.connected == 0:
            _serial.connectSerial()

        # first time stamp to be stored
        # time.time() is used for linux


        # reads the string coming from serial
        event_data = _serial.serial_event(str)

        while GPS.collect is True:
            t_stamp1 = time.time()

            GPS.check_instance(event_data)
            event_data = _serial.serial_event(str)
            t_stamp2 = time.time()

            distance = SpeedCalculation.geod_distance(GPS.c_lat_value, GPS.c_lat_value, GPS.o_lon_value, GPS.o_lon_value)

        # try:
        #     time_delta = time_s2 - times_s
        # except AttributeError:
        #     raise AssertionError('Input variables should be strings')

        # _serial.outputStream(time_delta, False)

        # reads latitude coordinate
        new_lat = _serial.serial_event(float)

        # if the value is not valid wait for a valid value from serial port
        while _serial.check_val(new_lat) is False and len(new_lat) is not None:
            new_lat = _serial.serial_event(float)

            #new_lat = float(new_lat.decode('utf-8'))

        new_lon = _serial.serial_event(float)

        while _serial.check_val(new_lon) is False and len(new_lon) is not None:
            new_lon = _serial.serial_event(float)

            #new_lon = new_lon.decode('utf-8')

        # compare new and old coordinates
        # if the coordinates are the same (True), skip the computation to save process power
        # if not (False) compute the speed
        stale = check_Stale_Cord(new_lat, new_lon)


        if stale is False:
            old_lat = new_lat
            old_lon = new_lon

            #calls the computation function and passes the values to it
            distance = SpeedCalculation.geod_distance(new_lat,
                                                     new_lon,
                                                     old_lat,
                                                     old_lon)

            #calculateds the change of time
            time_delta = times_s - time.time() / times_s;
            speed_mps = distance / time_delta
            speed_kph = (speed_mps * 3600.0) / 1000.0
            print(speed_mps)

        #insert value into local variable
        if stale is True:
            old_lat = new_lat
            old_lon = new_lon

        # s[0] = "asf"
        # print (s[0]
        #deubggin purposes
        print (stale)
        print (avail_sat.decode('utf-8'))
        print (new_lat)#.decode('utf-8'))
        print (new_lon)#.decode('utf-8'))



# check is see if the number is the same as the last number, returns a bool value
def check_Stale_Cord(number1, number2):
    c = numStore()
    if c.num_a == number1 or c.num_b == number2:
        c.add_num(number1)
        c.add_num(number2)
        return None

    else:
        return True

#checks for a valid value, invalid values are sent as a * byte
#def check_val(data):
 #   if b'*' in data:
  #      return False
   # else:
    #    return True

#loops the main loop
#if __name__ == '__main__':
 #   main()
