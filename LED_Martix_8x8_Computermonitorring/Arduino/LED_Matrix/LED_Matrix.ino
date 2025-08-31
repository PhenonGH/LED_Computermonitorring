//This program, written by TS on 12.08.2012 (version 1.0),
//configures an 8×8 NeoPixel LED matrix on an RP2040, 
//receives 64‑bit LED‑state values via serial, renders 
//the matrix with color gradients, and toggles between 
//two display modes when the button is pressed.
#include <Adafruit_NeoPixel.h>
#include <EEPROM.h>

#define PIN        28       // GPIO28
#define NUM_LEDS   64        // 8x8 Matrix
#define BRIGHTNESS 4        // 1.6 % von 255 ≈ 4 
Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);
#define aktiv 0
#define BUTTON_PIN 29
#define DEBOUNCEDELAY 50 // in ms
uint64_t LED = 0;

volatile bool buttonPressed = false;

struct LED_LIST {   
  byte led1;         
  byte led2;       
  byte led3;           
  byte led4;       
  byte led5;       
  byte led6;       
  byte led7;       
  byte led8;       
}; 


//main
void setup() {
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  strip.show(); // All LEDs off
  Serial.begin(9600);
  EEPROM.begin(4);
 
  pinMode(BUTTON_PIN, INPUT_PULLUP); // intern Pull-up aktiv
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, FALLING);
}
void loop() {
  LED_LIST data;
 
  bool mode = false;
  const int addr = 0;
  mode = EEPROM.read(addr);   
  
  int64_t wert = is_String_nummer(input());
  data = convert(wert);
  if(buttonPressed)
  {
     mode = !mode;
     buttonPressed = false;
     EEPROM.write(addr, (byte)mode); 
     EEPROM.commit();
  }

  if(mode)
  {
    LED= all_led_prozent_in_hex2(data);
  }
  else
  {
    //LED =all_led_prozent2(data);
    LED =all_led_prozent_time_is_hex(data);
  }
  

  display_LED(LED);
 
}
//----------------------------------------
//display
int64_t  all_led_prozent2(LED_LIST data)
{
   int64_t all_led_in_one_value = 0;
   all_led_in_one_value = int64_t(prozent(data.led1))
    | (int64_t(prozent(data.led2)) << 8)
    | (int64_t(prozent(data.led3)) << 16)
    | (int64_t(prozent(data.led4)) << 24)
    | (int64_t(prozent(data.led5)) << 32)
    | (int64_t(prozent(data.led6)) << 40)
    | (int64_t(prozent(data.led7)) << 48)
    | (int64_t(prozent(data.led8)) << 56);

  return all_led_in_one_value;
}

int64_t  all_led_prozent_in_hex2(LED_LIST data)
{
   int64_t all_led_in_one_value = 0;

   all_led_in_one_value = int64_t(prozent_in_hex(data.led1))
    | (int64_t(prozent_in_hex(data.led2)) << 8)
    | (int64_t(prozent_in_hex(data.led3)) << 16)
    | (int64_t(prozent_in_hex(data.led4)) << 24)
    | (int64_t(prozent_in_hex(data.led5)) << 32)
    | (int64_t(prozent_in_hex(data.led6)) << 40)
    | (int64_t(prozent_in_hex(data.led7)) << 48)
    | (int64_t(prozent_in_hex(data.led8)) << 56);

  return all_led_in_one_value;
}

int64_t  all_led_prozent_time_is_hex(LED_LIST data)
{
   int64_t all_led_in_one_value = 0;

   all_led_in_one_value = int64_t(prozent(data.led1))
    | (int64_t(prozent(data.led2)) << 8)
    | (int64_t(prozent(data.led3)) << 16)
    | (int64_t(prozent(data.led4)) << 24)
    | (int64_t(prozent(data.led5)) << 32)
    | (int64_t(prozent(data.led6)) << 40)
    | (int64_t(prozent_in_hex(data.led7)) << 48)
    | (int64_t(prozent_in_hex(data.led8)) << 56);

  return all_led_in_one_value;
}

byte prozent(int value)
{
  float temp;
  byte num_of_led_prozent =0;
  if (value > 100)
  {
    value =100;
  }
  temp = float(value)/12.5; 
  num_of_led_prozent= byte(temp);
  if(!(num_of_led_prozent ==0))
  {
     num_of_led_prozent=(1<<(num_of_led_prozent)) -1;
  }
 
  if(num_of_led_prozent<0)
  {
    num_of_led_prozent = 0;
  }
  
  return num_of_led_prozent;
 
}

byte prozent_in_hex(int value)
{
  if (value < 0) value = 0;
  if (value > 255) value = 255;  // 8-Bit 255 is Max
  return byte(value);
}

// 8 led Lines 8 colors
int64_t change_color(int LED_Num)
{ 
 const int group = LED_Num / 8;

  switch (group)
  {
    case 0:
      return 0xFF0000; // Rot
    case 1:
     // return 0x00FF00; // Grün
      return 0xFF0000; // Rot
    case 2:
      //return 0x0000FF; // Blau
      return 0x00FF00; // Grün
    case 3:
      //return 0xFFFF00; // Gelb
      return 0x00FF00; // Grün
    case 4:
      return 0xFF00FF; // Magenta
    case 5:
      return 0xFF8000; // Orange
    case 6:
       return 0x404040; // Braun
    case 7:
      return 0xFFFFFF; // Weiß
     default:
      return 0;
  }
return 0;
}

//set colors and display led matrix
void display_LED(int64_t display_LEDs)
{
  for (int i = 0; i < NUM_LEDS; i++) {
    
    if((display_LEDs>>i) & 1)
    {
      int64_t colors = change_color(i);
      strip.setPixelColor(i, strip.Color((colors >> 16) & 0xFF, (colors >> 8) & 0xFF, colors & 0xFF));
    }
    else {
      strip.setPixelColor(i, strip.Color(0,0,0));
    }

    strip.show();
    delay(1);
  }
  delay(1000);
  
}

//------------------------

//input
uint64_t is_String_nummer(String eingabe)
{
  eingabe.trim();
  uint64_t wert = strtoll(eingabe.c_str(), nullptr, 10);  
  return wert;
}

String input(void)
{
  
  while(1)
  {
  if (Serial.available() > 0)
  {
    String inputline = Serial.readString(); 
    Serial.println("Input: ");
    Serial.println(inputline);
    return inputline;
  }
  else
  {
    return "0";
  
  }
  }

}

struct LED_LIST convert(uint64_t wert)
{
    //wert =0xFFFFFFFF;
  LED_LIST data;
  data.led1 = wert & 0x000000FF;
  data.led2 = (wert>>8) & 0x000000FF;
  data.led3 = (wert>>16) & 0x000000FF;
  data.led4 = (wert>>24) & 0x000000FF;
  data.led5 = (wert>>32) & 0x000000FF;
  data.led6 = (wert>>40) & 0x000000FF;
  data.led7 = (wert>>48) & 0x000000FF;
  data.led8 = (wert>>56) & 0x000000FF;
  return data;
}
//--------------------

//button ISR

void buttonISR() {
  static unsigned long lastInterruptTime = 0;
  unsigned long interruptTime = millis();

  // Debounce with ISR
  if (interruptTime - lastInterruptTime > DEBOUNCEDELAY) {  // 50 ms Debounce
    buttonPressed = true;
  }
  lastInterruptTime = interruptTime;
}




