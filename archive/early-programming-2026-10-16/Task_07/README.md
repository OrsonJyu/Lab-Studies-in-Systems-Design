# Task 7: Morse sequence playlist

## Implementation

Four comma-separated values select a one-shot playlist for IO12. 0 = X (-..-), 1 = Y (-.--), 2 = Z (--..). A dot is 200 ms, a dash is 600 ms, a within-letter gap is 200 ms and each letter ends with a 600 ms gap. -1 plays a LOW-only 2000 ms pause. A valid command received during a playlist is rejected as Busy; the active playlist finishes unchanged.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
Case 1: 0,2,1,2 -> X, Z, Y, Z
Case 2: 1,2,-1,0 -> Y, Z, OFF for 2000 ms, X
```

## Required evidence

Record a separate video for 0,2,1,2 and 1,2,-1,0. The second video must show the explicit 2000 ms pause. Show the selected input in each recording.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.

## Ambiguous instruction in the lecture

Lecture 6 p.40 explicitly describes a 2000 ms pause for -1; p.41 says 200 ms. This implementation follows the worked example on p.40. The pause is isolated in PAUSE_MS so it can be changed if the lecturer confirms 200 ms.
