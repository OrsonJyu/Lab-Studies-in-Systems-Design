# Real hardware validation

Board: AirM2M_CORE_ESP32C3 in Arduino IDE 2.3.10; connected USB serial /dev/cu.usbmodem5B141410681; 115200 baud.

| Task | Code | Real evidence | Status |
|---|---|---|---|
| 1 | ZIP ready | Serial Monitor PNG | Captured |
| 2 | Updated ZIP ready | All 6 timed messages in PNG | Captured |
| 3 | ZIP ready | Five input/result pairs in PNG | Captured |
| 4 | ZIP ready | Repeat counts and invalid inputs in MP4 | Captured |
| 5 | ZIP ready | State duration edits and invalid state in MP4 | Captured |
| 6 | ZIP ready | Three mandatory case MP4s plus independent-LED test | Captured |
| 7 | ZIP ready | Two mandatory case MP4s | Captured |
| 8 | ZIP ready | Real short/long serial PNG/MP4 captured; phone footage of physical action still needed | Pending physical-action footage |

Observed results:

- Task 1: Welcome text and 100ms intervals after the scheduled 1500ms start. The saved screenshot documents steady output, rather than the exact first invocation.
- Task 2: all six exact targets appeared: 2000 Hello; 3000 from; 3500 "School; 4000 of; 4500 Design"; 5500 !!!. A leading blank line was added to separate text from ROM boot bytes; source and ZIP match.
- Task 3: 10 -> 25; -20 -> -5; 0 -> 15; 123abc -> 138; abc -> 15.
- Task 4: silent until input; 2 produced two sequences, 0 and 2.5 produced errors, 1 produced one sequence.
- Task 5: state 0 changed to 1200ms; state 3 to 800ms; observed transitions included t=107700 entering state 3 and t=108500 entering state 0, then t=109700 entering state 1. Invalid state 4 was rejected; s retained next-state behavior.
- Task 6: finite runs showed exactly ten ON/OFF cycles and completed; count 0 continued until replaced; delayed case waited before starting. An additional run exercised both LEDs together. Small scheduler jitter of a few milliseconds is visible in timestamps.
- Task 7: 0,2,1,2 played 0/2/1/2 then completed; 1,2,-1,0 played 1/2/pause/0 then completed. The second case paused from t=89732 to t=91735 (~2003ms).
- Task 8: compiled and uploaded successfully; both short pressed and long pressed were subsequently observed repeatedly from the real board. A real output PNG and MP4 were saved. The first 30-second window had no events; subsequent output was captured separately. Physical button motion is outside the screen capture, so the assignment still needs phone footage showing the button and screen together.

No screenshot or video has simulated serial text inserted. GPIO light emission was not optically filmed in Tasks 6-7; their requested Serial Monitor output was recorded. Task 8 specifically requires the button action in the frame.
