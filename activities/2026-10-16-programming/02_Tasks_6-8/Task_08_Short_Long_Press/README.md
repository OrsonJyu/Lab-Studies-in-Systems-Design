# Task 8: Short Long Press

Open `Task08_Short_Long_Press/Task08_Short_Long_Press.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

After boot, press and release the BOOT button at IO09. Hold about 200ms: one `short pressed`. Hold about 800ms: one `long pressed`. The threshold is strictly <500ms for short, so exactly 500ms is long. Classification is printed on RELEASE, not while held. A 20ms stable-state filter suppresses switch bounce; taps shorter than that filter are ignored. A button held at startup is ignored until released and pressed again. Required evidence: ONE real video showing BOTH the physical button action and Serial Monitor output for short and long presses. Boundary testing needs measured/synthetic GPIO timing; a hand press cannot establish exactly 500ms.

## Submission

Upload the ZIP in this folder under the Task 8 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
