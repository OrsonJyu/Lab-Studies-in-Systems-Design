# Task 5: Configurable FSM

Open `Task05_Configurable_FSM/Task05_Configurable_FSM.ino` in Arduino IDE. Keep SerialInput.h alongside the sketch where included.

Board: LuatOS ESP32C3 / ESP32C3 Dev Module. Serial Monitor: 115200 baud, Newline (or Both NL & CR). Use the supplied IO_Control_20260330b library and its dependencies.

## Test and evidence

Initial state durations are 1000,1500,2000,2500ms for states 0..3. Send `0,1200`, then wait for the next entry to state 0. Its entry log must show 1200ms and the next state must begin about 1200ms later. Also test `3,800` and verify the next state-3 dwell. Updates apply on NEXT ENTRY, so an already-running dwell is not retroactively changed. `s` retains the original skip-to-next-state command. Reject `4,100`, `0,-1`, `0,0`, `0,abc`, and `0,100,200`. State reports continue every 500ms. Required evidence: real Serial Monitor video showing commands, acknowledged settings and timed transitions.

## Submission

Upload the ZIP in this folder under the Task 5 heading on your sub-team submission page. Add the real evidence described above. `Evidence_To_Record` is reserved for your recordings; no hardware screenshots/videos have been fabricated.
