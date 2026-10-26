// SD5531 | In-Class Activity 6 | Task 6 | 16 Oct 2026
#include "SerialInput.h"
BinOutControl led0, led1;
struct BlinkSettings {
  ulong_t onMS = 1000, offMS = 500;
  long remaining = 0;
  bool forever = false, active = false, waiting = false;
};
BlinkSettings settings[2];
DeclareHandler(changeLED, _ctrl, BinOutControl, {
  int i = (&_ctrl == &led0) ? 0 : 1;
  BlinkSettings &s = settings[i];
  if (!s.active) return;
  if (s.waiting) {
    s.waiting = false; _ctrl.write(HIGH);
    Serial.print("LED "); Serial.print(i); Serial.print(" ON at t="); Serial.println(_ctrl.getUpdateTime());
    _ctrl.setTimeoutByRelTime(0, changeLED, s.onMS, true);
  } else if (_ctrl.read() == HIGH) {
    _ctrl.write(LOW);
    Serial.print("LED "); Serial.print(i); Serial.print(" OFF at t="); Serial.println(_ctrl.getUpdateTime());
    // Include the final OFF interval in every complete on/off cycle.
    _ctrl.setTimeoutByRelTime(0, changeLED, s.offMS, true);
  } else {
    if (!s.forever && --s.remaining == 0) {
      s.active = false;
      Serial.print("LED "); Serial.print(i); Serial.print(" complete at t="); Serial.println(_ctrl.getUpdateTime());
    } else {
      s.waiting = true; _ctrl.setTimeoutByRelTime(0, changeLED, 0, true);
    }
  }
});
DeclareHandler(ledHandler, _ctrl, BinOutControl, { /* Timeout handlers control blinking. */ });
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input; if (!readCommand(input)) return;
  long v[5]; int n = parseCSV(input, v, 5);
  if ((n != 4 && n != 5) || v[0] < 0 || v[0] > 1) {
    Serial.println("Error: led[,delay],on,off,count; led=0 or 1."); return;
  }
  int offset = (n == 5) ? 1 : 0;
  long delayMS = offset ? v[1] : 0;
  long onMS = v[1+offset], offMS = v[2+offset], count = v[3+offset];
  if (delayMS < 0 || onMS < 1 || offMS < 1 || count < 0) {
    Serial.println("Error: delay/count >= 0; on/off > 0."); return;
  }
  int i = v[0]; BinOutControl &led = i == 0 ? led0 : led1;
  // Override only the selected LED, including any pending delayed start.
  led.stopTimeout(0); led.write(LOW);
  settings[i].onMS = onMS; settings[i].offMS = offMS;
  settings[i].remaining = count; settings[i].forever = count == 0;
  settings[i].active = true; settings[i].waiting = true;
  Serial.print("Accepted: "); Serial.println(input);
  led.setTimeoutByRelTime(0, changeLED, delayMS, true);
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  if (led0.init(12, LOW) != Control_OK || led1.init(13, LOW) != Control_OK) {
    Serial.println("GPIO initialization failed."); return;
  }
  led0.enableScheduler(0, 1, ledHandler);
  led1.enableScheduler(0, 1, ledHandler);
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
