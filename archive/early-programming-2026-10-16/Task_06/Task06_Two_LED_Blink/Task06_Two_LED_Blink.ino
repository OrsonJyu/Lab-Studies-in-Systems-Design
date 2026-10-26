#include <IO_Control.h>
#include "InputHelpers.h"

BinOutControl leds[2]; // IO12 and IO13; initialized LOW (OFF)
SerialLineReader inputReader;
struct BlinkState {
  ulong_t onMS = 1000, offMS = 500;
  long requested = 0, completed = 0;
  bool active = false;
  int phase = 0; // 0 waiting for start; 1 ON; 2 OFF
};
BlinkState blink[2];

DeclareHandler(blinkStep, _ctrl, BinOutControl, {
  int index = (&_ctrl == &leds[0]) ? 0 : 1;
  BlinkState &b = blink[index];
  if (!b.active) return;
  if (b.phase == 2) {
    b.completed++; // count a FULL on + off cycle, including the final off duration
    if (b.requested > 0 && b.completed >= b.requested) {
      b.active = false;
      Serial.print("LED "); Serial.print(index); Serial.print(" done, cycles=");
      Serial.print(b.completed); Serial.print(" at t="); Serial.println(_ctrl.getUpdateTime());
      return;
    }
  }
  if (b.phase == 0 || b.phase == 2) {
    _ctrl.write(HIGH); b.phase = 1;
    Serial.print("LED "); Serial.print(index); Serial.print(" ON at t="); Serial.println(_ctrl.getUpdateTime());
    _ctrl.setTimeoutByRelTime(0, blinkStep, b.onMS, true);
  } else {
    _ctrl.write(LOW); b.phase = 2;
    Serial.print("LED "); Serial.print(index); Serial.print(" OFF at t="); Serial.println(_ctrl.getUpdateTime());
    _ctrl.setTimeoutByRelTime(0, blinkStep, b.offMS, true);
  }
});
DeclareHandler(ledHandler, _ctrl, BinOutControl, {});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (!inputReader.read(input)) return;
  long v[5]; int fields = parseCsv(input, v, 5);
  if (fields != 4 && fields != 5) {
    Serial.println("Error: use led,on,off,count OR led,start,on,off,count."); return;
  }
  int offset = fields == 5 ? 1 : 0;
  long relativeStart = fields == 5 ? v[1] : 0;
  if (v[0] < 0 || v[0] > 1 || relativeStart < 0 || v[1+offset] <= 0 || v[2+offset] <= 0 || v[3+offset] < 0) {
    Serial.println("Error: led must be 0/1; start/count >=0; on/off >=1 ms."); return;
  }
  int index = (int)v[0];
  // Replace only this LED's command; the other LED continues independently.
  leds[index].stopTimeout(0); leds[index].write(LOW);
  BlinkState &b = blink[index];
  b.onMS = v[1+offset]; b.offMS = v[2+offset];
  b.requested = v[3+offset]; b.completed = 0; b.phase = 0; b.active = true;
  Serial.print("Input: "); Serial.println(input);
  Serial.print("LED "); Serial.print(index); Serial.print(" start delay="); Serial.print(relativeStart);
  Serial.print("ms, on="); Serial.print(b.onMS); Serial.print("ms, off="); Serial.print(b.offMS);
  Serial.print("ms, count="); Serial.print(b.requested); Serial.println(" (0=infinite)");
  leds[index].setTimeoutByRelTime(0, blinkStep, (ulong_t)relativeStart, true);
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  for (int i = 0; i < 2; i++) {
    if (leds[i].init(i == 0 ? 12 : 13, LOW) != Control_OK) {
      Serial.println("Error initializing LED GPIO."); return;
    }
    leds[i].enableScheduler(0, 1, ledHandler, 1);
  }
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
