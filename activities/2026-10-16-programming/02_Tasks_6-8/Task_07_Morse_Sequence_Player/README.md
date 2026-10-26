# Task 7: Morse Sequence Player

Open `Task07_Morse_Sequence_Player/Task07_Morse_Sequence_Player.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Three Morse sequences use dot=200ms, dash=600ms, inter-symbol OFF=200ms, final inter-letter OFF=600ms. X=-..-, Y=-.--, Z=--..
Record separate real Serial Monitor videos for:
1. `0,2,1,2`: X, Z, Y, Z, then Command complete.
2. `1,2,-1,0`: Y, Z, LED OFF for 2000ms, X, then Command complete.
Sequence logs identify each step and its start time. Invalid commands must not play anything; send `0,3,1,2`, `0,1,2`, and `a,1,2,0`. While a command is playing, a new valid command is rejected as Busy; send it again after completion.
IMPORTANT SOURCE CONFLICT: slide 40 specifies 2000ms for -1; slide 41 says 200ms. This implementation follows the worked example on slide 40 (2000ms), exposed as PAUSE_MS for an instructor-directed adjustment. Required evidence: one real Serial Monitor video for each mandatory command; show the LED too if possible.

## Submission

Upload the ZIP in this folder under the Task 7 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
