# SD5531 - In-Class Activity 6 | 16 Oct 2026

All eight sketches compile for ESP32C3. Tasks 1-8 were run on the connected AirM2M ESP32C3, with real serial evidence captured. No assignment has been uploaded to Confluence. Task 8 still needs a real physical button demonstration.

| Task | Code | Real evidence | Status |
|---|---|---|---|
| 1 | ZIP ready | Serial Monitor PNG | Captured |
| 2 | Updated ZIP ready | All 6 timed messages in PNG | Captured |
| 3 | ZIP ready | Five input/result pairs in PNG | Captured |
| 4 | ZIP ready | Repeat counts and invalid inputs in MP4 | Captured |
| 5 | ZIP ready | State duration edits and invalid state in MP4 | Captured |
| 6 | ZIP ready | Three mandatory case MP4s plus independent-LED test | Captured |
| 7 | ZIP ready | Two mandatory case MP4s | Captured |
| 8 | ZIP ready | Serial PNG/MP4 captured; physical button must also appear in phone video | Pending physical-action footage |

## Organization and submission

- `00_Course_Materials`: all 6 lecture PDFs, all 7 supplied example ZIPs, and IO_Control_20260330b.zip.
- `01_Tasks_1-5`: deadline end of 23 Oct 2026.
- `02_Tasks_6-8`: deadline end of 30 Oct 2026.
- Each task has an identically named sketch folder, its ZIP, a README and `Evidence_To_Record`.
- `03_Validation` contains compiler logs. See VALIDATION.md and HARDWARE_PROGRESS.md for the distinction between compilation and hardware tests.

Submit one set per sub-team with headings Task 1 through Task 8. Upload each task ZIP plus its PNG or MP4 evidence. Task 6 videos are in `Task06_Recordings`, Task 7 videos in `Task07_Recordings`. Their filenames identify the exact mandatory input. The extra Task 6 video demonstrates simultaneous independent LEDs. Ignore the initial `RECORDING_REQUIRED.txt` placeholders where evidence now exists.

Videos contain actual ESP32C3 serial output captured from successive live Arduino IDE frames and encoded at their recorded wall-clock intervals. They are sampled screen recordings; no simulated or generated serial output is substituted.

## Task 8: final physical step

With its sketch uploaded and Serial Monitor at 115200 baud, press and release BOOT (IO09) briefly for `short pressed`; then hold about one second and release for `long pressed`. The short threshold is strictly <500ms; a 20ms debounce filter ignores very brief bounce. Use a phone to film the button and Serial Monitor together, and save that video in Task 8's Evidence_To_Record folder.

## Course ambiguities and chosen behavior

- Task 7's worked example says -1 means 2000ms OFF, while the subsequent slide says 200ms. This code follows the worked example (2000ms, PAUSE_MS).
- Task 5 duration changes apply on next entry to that state; `s` preserves the original skip-state command.
- Task 6 replaces only the selected LED's run. Task 7 rejects valid new commands while busy.
- Serial Monitor uses 115200 baud and Newline (or Both NL & CR). Keep SerialInput.h alongside each sketch where present.

## Sources

- https://www.designandmake.org/display/SD55312026S1/7.+Programming+with+IO_Control+Library
- https://www.designandmake.org/display/SD55312026S1/In-Class+Activity+6
- https://www.designandmake.org/display/DeFL/IO_Control+library+-+Installation+and+Compilation
- https://docs.arduino.cc/language-reference/en/variables/data-types/stringObject/Functions/toInt/
