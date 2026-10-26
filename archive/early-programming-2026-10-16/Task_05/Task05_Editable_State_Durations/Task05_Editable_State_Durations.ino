#include <IO_Control.h>
#include "InputHelpers.h"

SerialLineReader inputReader;
int state = -1;
ulong_t stateDuration[] = {1000, 1500, 2000, 2500};
ulong_t stateEnteredAt = 0;
bool started = false;

DeclareHandler(setNextState, _ctrl, IOControl, {
  state = (state + 1) % 4;
  stateEnteredAt = _ctrl.getUpdateTime();
  Serial.print("entering state="); Serial.print(state);
  Serial.print(" at t="); Serial.print(stateEnteredAt);
  Serial.print(", duration = "); Serial.print(stateDuration[state]); Serial.println("ms");
  _ctrl.setTimeoutByRelTime(0, setNextState, stateDuration[state], true);
});
DeclareHandler(printCurrentState, _ctrl, IOControl, {
  Serial.print("current state="); Serial.print(state);
  Serial.print(" at time t="); Serial.println(_ctrl.getUpdateTime());
  _ctrl.setTimeoutByRelTime(1, printCurrentState, 500, true);
});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  if (!started) {
    started = true;
    _ctrl.setTimeoutByRelTime(0, setNextState, 0, true);
    _ctrl.setTimeoutByRelTime(1, printCurrentState, 0, true);
  }
  String input;
  if (!inputReader.read(input)) return;
  input.trim();
  if (input == "s") { // retain the original example's skip-state command
    _ctrl.stopTimeout(0);
    _ctrl.setTimeoutByRelTime(0, setNextState, 0, true);
    return;
  }
  long values[2];
  if (parseCsv(input, values, 2) != 2 || values[0] < 0 || values[0] > 3 || values[1] <= 0) {
    Serial.println("Error: enter <state 0..3>,<duration in ms >=1>, or s."); return;
  }
  int target = (int)values[0];
  stateDuration[target] = (ulong_t)values[1];
  Serial.print("Updated state "); Serial.print(target);
  Serial.print(" duration to "); Serial.print(stateDuration[target]); Serial.println("ms");
  if (target == state) {
    // Apply the new duration to the current visit, measured from state entry.
    ulong_t elapsed = _ctrl.getUpdateTime() - stateEnteredAt;
    ulong_t remaining = elapsed >= stateDuration[state] ? 0 : stateDuration[state] - elapsed;
    _ctrl.stopTimeout(0);
    _ctrl.setTimeoutByRelTime(0, setNextState, remaining, true);
  }
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  IO_Control.enableScheduler(100, 1, iocontrolHandler, 2);
}
void loop() {}
