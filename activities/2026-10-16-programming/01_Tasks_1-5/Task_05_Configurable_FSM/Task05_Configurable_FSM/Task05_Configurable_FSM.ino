// SD5531 | In-Class Activity 6 | Task 5 | 16 Oct 2026
#include "SerialInput.h"
int state = -1;
ulong_t stateDuration[4] = {1000, 1500, 2000, 2500};
DeclareHandler(printCurrentState, _ctrl, IOControl, {
  Serial.print("current state="); Serial.print(state);
  Serial.print(" at time t="); Serial.println(_ctrl.getUpdateTime());
  _ctrl.setTimeoutByRelTime(1, printCurrentState, 500, true);
});
DeclareHandler(setNextState, _ctrl, IOControl, {
  state = (state + 1) % 4;
  Serial.print("entering state="); Serial.print(state);
  Serial.print(" at t="); Serial.print(_ctrl.getUpdateTime());
  Serial.print(", duration = "); Serial.print(stateDuration[state]); Serial.println("ms");
  _ctrl.setTimeoutByRelTime(0, setNextState, stateDuration[state], true);
});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  if (!_ctrl.isTimeoutActive(0)) _ctrl.setTimeoutByRelTime(0, setNextState, 0, true);
  if (!_ctrl.isTimeoutActive(1)) _ctrl.setTimeoutByRelTime(1, printCurrentState, 0, true);
  String input;
  if (!readCommand(input)) return;
  if (input == "s") {
    _ctrl.stopTimeout(0); _ctrl.setTimeoutByRelTime(0, setNextState, 0, true); return;
  }
  long values[2];
  if (parseCSV(input, values, 2) != 2 || values[0] < 0 || values[0] > 3 || values[1] < 1) {
    Serial.println("Error: use <state 0..3>,<positive duration in ms>, or s."); return;
  }
  stateDuration[values[0]] = (ulong_t)values[1];
  Serial.print("Updated state "); Serial.print(values[0]);
  Serial.print(" duration to "); Serial.print(values[1]);
  Serial.println("ms (applies on next entry to that state).");
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  IO_Control.enableScheduler(100, 1, iocontrolHandler, 2);
}
void loop() {}
