#include <IO_Control.h>

BinInControl binInCtrl0;
const ulong_t DEBOUNCE_MS = 20;
const ulong_t LONG_PRESS_MS = 500;
int candidateState = HIGH, stableState = HIGH;
ulong_t candidateSince = 0, pressedAt = 0;
bool trackingPress = false;

DeclareHandler(binInHandler, _ctrl, BinInControl, {
  // Preserve the example's interrupt-based change detection and timestamp.
  if (_ctrl.isBinInTriggered()) {
    int rawState = _ctrl.getInterruptState();
    if (rawState != candidateState) {
      candidateState = rawState;
      candidateSince = (ulong_t)_ctrl.getInterruptTime();
    }
  }
  // Require the new level to remain stable for 20 ms before accepting it.
  ulong_t now = _ctrl.getUpdateTime();
  if (candidateState != stableState && _ctrl.read() == candidateState &&
      (ulong_t)(now - candidateSince) >= DEBOUNCE_MS) {
    stableState = candidateState;
    if (stableState == LOW) {
      pressedAt = candidateSince; trackingPress = true;
    } else if (trackingPress) {
      ulong_t duration = candidateSince - pressedAt;
      trackingPress = false;
      Serial.println(duration < LONG_PRESS_MS ? "short pressed" : "long pressed");
      Serial.print("duration="); Serial.print(duration); Serial.println("ms");
    }
  }
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  if (binInCtrl0.init(9, INPUT_PULLUP) != Control_OK) {
    Serial.println("Error initializing BOOT button at IO09."); return;
  }
  candidateState = stableState = binInCtrl0.read();
  candidateSince = millis();
  // If already held at startup, ignore the first release: duration is unknown.
  binInCtrl0.enableInterrupt(CHANGE);
  binInCtrl0.enableScheduler(0, 1, binInHandler);
  Serial.println("Task 8 ready: press and release BOOT (IO09).");
}
void loop() {}
