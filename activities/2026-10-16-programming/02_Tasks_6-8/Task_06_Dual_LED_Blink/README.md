# Task 6: Dual LED Blink

Open `Task06_Dual_LED_Blink/Task06_Dual_LED_Blink.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Record a separate real Serial Monitor video for EACH mandatory case, stating the exact input in the filename/caption:
1. `0,1000,500,10`: IO12 ON 1000ms/OFF 500ms, 10 complete cycles, then stays OFF.
2. `1,500,1000,0`: IO13 ON 500ms/OFF 1000ms continuously. End recording after several cycles; a later valid command for LED 1 replaces this run.
3. `0,1000,1000,500,10`: IO12 first goes HIGH about 1000ms after acceptance, then ON 1000ms/OFF 500ms for 10 cycles.
Additional checks: run both LEDs together; changing LED 0 must not reset LED 1. `1,200,200,2` overrides LED 1 and ends OFF after 2 cycles. Reject bad LED index, negative delay/count, zero/negative ON or OFF, non-integers and wrong field counts. A new command overrides only its selected LED and cancels its pending timer. The last OFF interval counts as part of the last full cycle.

## Submission

Upload the ZIP in this folder under the Task 6 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
