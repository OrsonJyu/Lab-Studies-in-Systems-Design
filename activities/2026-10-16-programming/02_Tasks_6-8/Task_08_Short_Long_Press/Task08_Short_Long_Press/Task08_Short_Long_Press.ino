// SD5531 | In-Class Activity 6 | Task 8 | 16 Oct 2026
#include <IO_Control.h>
BinInControl binInCtrl0;
const uint32_t DEBOUNCE_MS = 20;
int candidate = HIGH, stableState = HIGH;
uint32_t candidateTime = 0, pressedAt = 0;
bool pressRecorded = false;
DeclareHandler(binInHandler, _ctrl, BinInControl, {
  uint32_t now = _ctrl.getUpdateTime();
  // Retain edge timestamps; only accept a new state once stable for 20ms.
  if (_ctrl.isBinInTriggered()) {
    int edgeState = _ctrl.getInterruptState();
    if (edgeState != candidate) {
      candidate = edgeState; candidateTime = (uint32_t)_ctrl.getInterruptTime();
    }
  }
  int raw = _ctrl.read();
  if (raw != candidate) { candidate = raw; candidateTime = now; }
  if (candidate == stableState || (uint32_t)(now - candidateTime) < DEBOUNCE_MS) return;
  stableState = candidate;
  if (stableState == LOW) { pressedAt = candidateTime; pressRecorded = true; }
  else if (pressRecorded) {
    uint32_t duration = candidateTime - pressedAt;
    Serial.println(duration < 500 ? "short pressed" : "long pressed");
    pressRecorded = false;
  }
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  if (binInCtrl0.init(9, INPUT_PULLUP) != Control_OK) {
    Serial.println("GPIO initialization failed."); return;
  }
  candidate = stableState = binInCtrl0.read();
  // Ignore a button held at startup until it is released and pressed again.
  binInCtrl0.enableScheduler(0, 1, binInHandler);
  binInCtrl0.enableInterrupt(CHANGE);
}
void loop() {}
