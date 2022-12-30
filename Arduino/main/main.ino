#include <ezButton.h>
#include <LiquidCrystal.h>

#define BAUD_RATE 115200
#define DEBOUNCE_DELAY 50

#define LCD_WAIT_TEXT "WAITING"
#define LCD_READY_TEXT "READY"
#define LCD_PRINT_DELAY 5000
#define LCD_SCROLL_DELAY 150

LiquidCrystal lcd(2, 3, 7, 6, 5, 4);
int scroll_len = 0;  // used to store the scroll length for the display

int buttonPin = 12;
ezButton btn(buttonPin);

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);
  btn.setDebounceTime(50);
}

// switch between states
void loop() {
}

void readBtn(){
  btn.loop();

  if(btn.isPressed()){
    // Serial.println("incrementing!");
  }
}

// void poll(){
//   int diff = millis() - last_poll;
//   if(diff > polling_interval){  // or poll command
//     Serial.print("polling: "); Serial.println(diff);
//     last_poll = millis();  // fix me
//   }
// }

// animated clear (for fun!)z
void animateClear(int scroll_len){
  delay(LCD_PRINT_DELAY);
  for (int i=0; i<scroll_len; i++) {
    lcd.scrollDisplayLeft();
    delay(LCD_SCROLL_DELAY);
  }
}
