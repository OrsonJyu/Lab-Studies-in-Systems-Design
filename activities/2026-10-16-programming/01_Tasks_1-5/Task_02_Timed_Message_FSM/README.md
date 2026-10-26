# Task 2: Timed Message FSM

Open `Task02_Timed_Message_FSM/Task02_Timed_Message_FSM.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Reset the board and capture all six output lines. Due times/messages: 2000 Hello; 3000 from; 3500 "School; 4000 of; 4500 Design"; 5500 !!!. Nothing further is printed. Timestamps report actual execution time, with normal scheduler jitter. Required evidence: one real Serial Monitor screenshot.

## Submission

Upload the ZIP in this folder under the Task 2 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
