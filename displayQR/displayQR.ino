#include <qrcode.h>
#include <TFT.h>
#include <SPI.h>
#define cs 10
#define dc 9
#define rst 8
TFT screen = TFT(cs, dc, rst);
QRCode qrcode;

void setup() {
  Serial.begin(115200);
  screen.begin();
  screen.setRotation(2);
  screen.background(255,255,255);
  screen.setTextSize(2);
  screen.stroke(0,0,0);
  screen.fill(0,0,0);
}

void loop() {
  screen.background(255,255,255);
  uint8_t qrcodeData[qrcode_getBufferSize(3)];
  qrcode_initText(&qrcode, qrcodeData, 3, 0, "HELLO WORLD");
  for (uint8_t y = 0; y < qrcode.size; y++){
    for (uint8_t x = 0; x < qrcode.size; x++){
      if(qrcode_getModule(&qrcode, x, y)){
        screen.rect(5+(x*4), 40+(y*4), 4, 4);  
      }
    }
  }
  delay(10000);
  screen.background(255,255,255);
  qrcode_initText(&qrcode, qrcodeData, 3, 0, "hello world");
  for (uint8_t y = 0; y < qrcode.size; y++){
    for (uint8_t x = 0; x < qrcode.size; x++){
      if(qrcode_getModule(&qrcode, x, y)){
        screen.rect(5+(x*4), 40+(y*4), 4, 4);  
      }
    }
  }
  delay(10000);
}
