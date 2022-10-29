#include "src/ConfigConstants.h"
#include "src/SeparatorReader.h"

#include <LiquidCrystal.h>
LiquidCrystal lcd(2, 3, 7, 6, 5, 4);

enum ProgState{
  WAITING,
  READY,
  PRINTING,
  CLEARING,
  STOPPED
};

String waitBuff = "";  // used to buffer the wait command
int scroll_len = 0;  // used to store the scroll length for the display
ProgState state = STOPPED;  // default state

SeparatorReader reader(&Serial);


void setup() {
  Serial.begin(BAUD_RATE);
  Serial.setTimeout(1000);
  Serial.println("Start");
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);

  stopAndWait();  // start out cleared and waiting like we just stopped
}

// switch between states
void loop() {
  switch (state) {
    case WAITING:
      checkProgReady();
      break;
    case READY:
      reader.Read();
      if(reader.readReady()){
        state = PRINTING;
      }else if(reader.isStopped()){
        state = STOPPED;
      }
      break;
    case PRINTING:
      printIdValBuff();
      break;
    case STOPPED:
      stopAndWait();
      break;
    case CLEARING:
      animateClear(scroll_len);
      break;
  }
}

void checkProgReady(){
  // send waiting and then listen for on a response for WAIT_TIME millis
  unsigned long currentmillis = millis();
  Serial.println(WAIT_TEXT);
  delay(1); // delay more 1ms makes this work for some reason
  while(millis() - currentmillis < WAIT_TIME){
    if(Serial.available() > 0){
      // load each char until into the buffer until we see a newline
      char c = Serial.read();
      waitBuff += c;
      if(c == NEWLINE){
        break;
      }
    }
  }

  // wait for "START_SUFFIX\n", this means the pc responded to the wait
  if(waitBuff.length() == 2 && waitBuff[0] == START_SUFFIX){
    // start command seen, we can clear the buffer now since this is the only place it's used
    waitBuff = "";
    digitalWrite(LED_BUILTIN, LOW);
    setReady();
  }
}

void setReady(){
    reader.Reset();
    lcd.clear();
    lcd.print(LCD_READY_TEXT);
    state = READY;
    Serial.println(READY_CHAR);
}

// function to print the buffer to the lcd
void printIdValBuff(){
  String key = reader.GetKey();
  String value = reader.GetValue();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(key);
  lcd.setCursor(0,1);
  lcd.print(value);

  if(key.length() > value.length()){
    scroll_len = key.length();
  }else{
    scroll_len = value.length();
  }
  reader.Reset();
  state = CLEARING;
}

// animated clear (for fun!)
void animateClear(int scroll_len){
  delay(LCD_PRINT_DELAY);
  for (int i=0; i<scroll_len; i++) {
    lcd.scrollDisplayLeft();
    delay(LCD_SCROLL_DELAY);
  }
  setReady();
}

// cleans up and starts waiting again
void stopAndWait(){
  reader.Reset();
  state = WAITING;
  digitalWrite(LED_BUILTIN, HIGH); // LED's for flash/debugging
  lcd.clear();
  lcd.print(LCD_WAIT_TEXT);
}

