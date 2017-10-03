#include <TinyGPS++.h>
#include <SoftwareSerial.h>
static const int RX_Pin = 11, TX_Pin = 10;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial GPS_SS(RX_Pin, TX_Pin);

unsigned long last = 0UL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  GPS_SS.begin(GPSBaud);

  //Serial.write("Debug mode");
}

void loop() {
  while (GPS_SS.available()>0)
    gps.encode(GPS_SS.read());
    
  // put your main code here, to run repeatedly:
    printInt(gps.satellites.value(), gps.satellites.isValid(), 5);
    
    float num_val = printFloat(gps.location.lat(), gps.location.isValid(), 11, 6);
    //Serial.print(", ");
    float num_val2 = printFloat(gps.location.lng(), gps.location.isValid(), 12, 6);
     
    String lonlat = (((String)num_val + ", ") + (String)num_val2);

smartDelay(1000);
}



static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (GPS_SS.available())
      gps.encode(GPS_SS.read());
  } while (millis() - start < ms);
}

static void printInt(unsigned long val, bool valid, int len)
{
  char sz[32] = "*****************";
  if (valid)
    sprintf(sz, "%ld", val);
  sz[len] = 0;
  for (int i=strlen(sz); i<len; ++i)
    sz[i] = ' ';
  if (len > 0) 
    sz[len-1] = ' ';
  Serial.println(sz);
  smartDelay(0);
}

static float printFloat(float val, bool valid, int len,  int prec)
{
   if (!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    Serial.println(' ');
  }
  else
  {
    
    Serial.println(val, prec);
    int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    //for (int i=flen; i<len; ++i)
     // Serial.print(' ');
  }
  return val;
  
}

