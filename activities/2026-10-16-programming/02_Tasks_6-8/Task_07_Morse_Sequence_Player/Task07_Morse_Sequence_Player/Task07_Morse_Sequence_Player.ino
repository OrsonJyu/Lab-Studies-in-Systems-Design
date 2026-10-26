// SD5531 | In-Class Activity 6 | Task 7 | 16 Oct 2026
#include "SerialInput.h"
BinOutControl binOutCtrl0;
BinOutSequence binOutSeq0, binOutSeq1, binOutSeq2, pauseSeq;
int requested[4]; int position = 0; bool playing = false;
const uint32_t DOT_MS = 200;
const uint32_t PAUSE_MS = 2000; // Example 2 says 2000ms; slide 41 says 200ms.
void addMorse(BinOutSequence &seq, const char *pattern) {
  for (int i = 0; i < 4; ++i) {
    seq.addSetState(pattern[i] == '-' ? 3 * DOT_MS : DOT_MS, HIGH);
    seq.addSetState(i == 3 ? 3 * DOT_MS : DOT_MS, LOW);
  }
}
void playNext() {
  if (position == 4) { playing = false; Serial.println("Command complete."); return; }
  int number = requested[position++];
  Serial.print("Step "); Serial.print(position); Serial.print(": ");
  if (number == -1) Serial.println("LED OFF for 2000ms");
  else { Serial.print("play binOutSeq"); Serial.println(number); }
  Serial.print("at t="); Serial.println(binOutCtrl0.getUpdateTime());
  switch (number) {
    case -1: binOutCtrl0.playRelTime(pauseSeq, 0, 1); break;
    case 0: binOutCtrl0.playRelTime(binOutSeq0, 0, 1); break;
    case 1: binOutCtrl0.playRelTime(binOutSeq1, 0, 1); break;
    case 2: binOutCtrl0.playRelTime(binOutSeq2, 0, 1); break;
  }
}
DeclareHandler(binOutHandler, _ctrl, BinOutControl, {
  if (playing && _ctrl.isAllSeqEnded()) playNext();
});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input; if (!readCommand(input)) return;
  long v[4];
  if (parseCSV(input, v, 4) != 4) { Serial.println("Error: enter exactly four sequence numbers."); return; }
  for (int i = 0; i < 4; ++i) {
    if (v[i] < -1 || v[i] > 2) { Serial.println("Error: each number must be -1, 0, 1 or 2."); return; }
  }
  // Finish an accepted command in full; reject new commands while busy.
  if (playing) { Serial.println("Busy: wait for Command complete, then send again."); return; }
  for (int i = 0; i < 4; ++i) requested[i] = v[i];
  position = 0; playing = true;
  Serial.print("Accepted: "); Serial.println(input); playNext();
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  if (binOutCtrl0.init(12, LOW) != Control_OK) { Serial.println("GPIO initialization failed."); return; }
  addMorse(binOutSeq0, "-..-"); // X
  addMorse(binOutSeq1, "-.--"); // Y
  addMorse(binOutSeq2, "--.."); // Z
  pauseSeq.addSetState(PAUSE_MS, LOW);
  binOutCtrl0.enableScheduler(0, 1, binOutHandler);
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
