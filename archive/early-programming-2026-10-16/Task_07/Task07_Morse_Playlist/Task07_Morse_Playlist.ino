#include <IO_Control.h>
#include "InputHelpers.h"

BinOutControl binOutCtrl0;
BinOutSequence binOutSeq0, binOutSeq1, binOutSeq2, pauseSequence;
BinOutSequence *sequences[] = {&binOutSeq0, &binOutSeq1, &binOutSeq2};
SerialLineReader inputReader;
const ulong_t DOT_MS = 200;
// Lecture 6 p.40 says 2000 ms; p.41 says 200 ms. Follow the explicit example.
const ulong_t PAUSE_MS = 2000; // change this single constant if clarified by tutor
int playlist[4];
int nextItem = 0;
bool playing = false;
void startNextItem();

void addMorse(BinOutSequence &seq, const char *pattern) {
  for (int i = 0; pattern[i]; i++) {
    seq.addSetState(pattern[i] == '-' ? 3 * DOT_MS : DOT_MS, HIGH);
    seq.addSetState(pattern[i+1] ? DOT_MS : 3 * DOT_MS, LOW);
  }
}
void startNextItem() {
  if (nextItem == 4) {
    playing = false; binOutCtrl0.write(LOW);
    Serial.print("Playlist finished at t="); Serial.println(binOutCtrl0.getUpdateTime());
    return;
  }
  int item = playlist[nextItem++];
  Serial.print("Item "); Serial.print(nextItem); Serial.print("/4: ");
  if (item == -1) {
    Serial.print("LED OFF for "); Serial.print(PAUSE_MS); Serial.println("ms");
    binOutCtrl0.playRelTime(pauseSequence, 0, 1);
  } else {
    Serial.print("binOutSeq"); Serial.print(item);
    Serial.print(" (Morse "); Serial.print((char)('X'+item)); Serial.println(")");
    binOutCtrl0.playRelTime(*sequences[item], 0, 1);
  }
  Serial.print("item start t="); Serial.println(binOutCtrl0.getUpdateTime());
}
DeclareHandler(binOutHandler, _ctrl, BinOutControl, {
  if (playing && _ctrl.isAllSeqEnded()) startNextItem();
});
DeclareHandler(iocontrolHandler, _ctrl, IOControl, {
  String input;
  if (!inputReader.read(input)) return;
  long values[4];
  if (parseCsv(input, values, 4) != 4) {
    Serial.println("Error: enter exactly four sequence numbers, each -1, 0, 1 or 2."); return;
  }
  for (int i = 0; i < 4; i++) {
    if (values[i] < -1 || values[i] > 2) {
      Serial.println("Error: each sequence number must be -1, 0, 1 or 2."); return;
    }
  }
  if (playing) { Serial.println("Busy: wait for the current playlist to finish."); return; }
  for (int i = 0; i < 4; i++) playlist[i] = (int)values[i];
  Serial.print("Input: "); Serial.println(input);
  nextItem = 0; playing = true; startNextItem();
});
void setup() {
  IO_Control.begin(); Serial.begin(115200);
  if (binOutCtrl0.init(12, LOW) != Control_OK) { Serial.println("Error initializing IO12."); return; }
  addMorse(binOutSeq0, "-..-"); // X
  addMorse(binOutSeq1, "-.--"); // Y
  addMorse(binOutSeq2, "--.."); // Z
  pauseSequence.addSetState(PAUSE_MS, LOW);
  binOutCtrl0.enableScheduler(0, 1, binOutHandler);
  IO_Control.enableScheduler(0, 1, iocontrolHandler);
}
void loop() {}
