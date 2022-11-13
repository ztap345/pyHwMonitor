#include <ezButton.h>
#include <LiquidCrystal.h>

#include "src/ConfigConstants.h"
#include "src/MessageReceiver.h"
#include "src/SeparatorHandler.h"

LiquidCrystal lcd(2, 3, 7, 6, 5, 4);
int scroll_len = 0;  // used to store the scroll length for the display

int buttonPin = 12;
ezButton btn(buttonPin);

enum ListenState{
  HANDSHAKING,  // need to handshake
  WAITING,  // waiting on a command
  PROCESSING  // processing command
};
ListenState state = HANDSHAKING;  // default state

String handshakeBuff = "";

int last_poll = 0;
const int polling_interval = 10*1000;  // 1 second in millis

// display labels loaded after handshaking
int label_count = 0;
int topLabelIndex = 0;
String labels[MAX_LABEL_COUNT];
String values[MAX_LABEL_COUNT];

// current command also the buffer
String cmd = "";
MessageReceiver msgRecvr(START_STRING, END_STRING);
SeparatorHandler sepHandler;

void setup() {
  Serial.begin(BAUD_RATE);
  Serial.setTimeout(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);
  // Serial.println("Waiting...");
  btn.setDebounceTime(50);
}

// switch between states
void loop() {
  switch (state) {
    case HANDSHAKING:
      handshake();
      // state = WAITING;
      break;
    case PROCESSING:
      processCmd();
      break;
    case WAITING:
      readBtn();

      poll();

      if(Serial.available() > 0){
        char c = Serial.read();

        if(c != NEWLINE){
          cmd += c;
        }else{
          Serial.println(cmd);
          state = PROCESSING;
        }
      }
      break;
  }
}

void handshake(){
  Serial.println("handshaking");
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Connecting...");
  // if we're handshaking do nothing else
  while (state == HANDSHAKING)
  {
    if(Serial.available() > 0){
      char c = Serial.read();

      if(c != NEWLINE){
        // didn't see a newline, add to the buffer
        handshakeBuff += c;
      }else{
        if (handshakeBuff == WAKE_STRING){
          // saw a newline and found the wake command
          state = WAITING;
        }
        // state was set or a line was read and the wake string was not found
        handshakeBuff = "";
      }
    }
  }
  Serial.println(ACK_STRING);
}

void processCmd(){
  if(cmd == "blink"){
    Serial.println("Blinking");
    test_output();
    test_output();
    test_output();
  }else if(cmd == "ld_lbls"){
    handleLoadLabels();
  }else if(cmd == "ld_values"){
    handleLoadValues();
  }else if(cmd == "close"){
    Serial.println("Closing conenction");
    state = HANDSHAKING;
    return;
  }
  cmd = "";
  Serial.println(ACK_STRING);
  state = WAITING;
}

void handleLoadLabels(){
  // Serial.println("Loading Labels");
  sepHandler.init(LIST_SEPARATOR, NEWLINE, MAX_LABEL_COUNT);
  while(!msgRecvr.isFinished()){
    if(Serial.available() > 0){
      msgRecvr.readChar(Serial.read(), &sepHandler);
    }
  }

  loadLabels(sepHandler.get());
  msgRecvr.clear();
}

void loadLabels(String* newLabels){
  label_count = 0;
  for(int i=0; i<MAX_LABEL_COUNT; i++){
    labels[i] = newLabels[i];
    if(labels[i] != ""){
      label_count++;
    }
  }

  topLabelIndex = 0;
  incrementLabels();
}

void handleLoadValues(){
  Serial.println("Loading Values");
  sepHandler.init(KEY_VAL_SEPARATOR, NEWLINE, 2);
  while(!msgRecvr.isFinished()){
    if(Serial.available() > 0){
      msgRecvr.readChar(Serial.read(), &sepHandler);
    }
  }
  
  msgRecvr.clear();
}

void incrementLabels(){
  refreshLabels();
  if(label_count > 1){
    topLabelIndex = (topLabelIndex + 1) % label_count;
  }
}

void refreshLabels(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(labels[topLabelIndex] + ":" + values[topLabelIndex]);
  if(label_count > 1){
    int bottomLabelIndex = (topLabelIndex + 1) % label_count;
    lcd.setCursor(0,1);
    lcd.print(labels[bottomLabelIndex] + ":" + values[bottomLabelIndex]);
  }
}

void readBtn(){
  btn.loop();

  if(btn.isPressed()){
    // Serial.println("incrementing!");
    incrementLabels();
  }
}

void poll(){
  int diff = millis() - last_poll;
  if(diff > polling_interval){  // or poll command
    Serial.print("polling: "); Serial.println(diff);
    last_poll = millis();  // fix me
  }
}

// animated clear (for fun!)z
void animateClear(int scroll_len){
  delay(LCD_PRINT_DELAY);
  for (int i=0; i<scroll_len; i++) {
    lcd.scrollDisplayLeft();
    delay(LCD_SCROLL_DELAY);
  }
}

void test_output(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
