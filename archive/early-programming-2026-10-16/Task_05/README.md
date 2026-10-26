# Task 5: Edit state durations through Serial Monitor

## Implementation

The four-state FSM uses durations 1000, 1500, 2000 and 2500 ms initially. Commands state,duration update the selected duration. A change to the current state applies from the original state entry time; if its new duration has already elapsed, it advances immediately. The original s command still skips a state.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
0,1200; 1,700; s; 4,1000; 2,abc
```

## Required evidence

Enter 0,1200, then 1,700. Observe later state-entry timestamps and duration labels. Enter s to skip. Enter 4,1000 and 2,abc to demonstrate validation.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
