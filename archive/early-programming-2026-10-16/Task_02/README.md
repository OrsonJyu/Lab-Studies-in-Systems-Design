# Task 2: Timed finite state machine

## Implementation

A six-state FSM prints one message at each absolute target time: 2000, 3000, 3500, 4000, 4500 and 5500 ms. It then stays idle until reset. Double quotation marks are included around School of Design, as shown in the brief.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
No input. Expected: At t = 2000, Hello; 3000, from; 3500, "School; 4000, of; 4500, Design"; 5500, !!!
```

## Required evidence

Reset with Serial Monitor open. Wait until the final !!! at approximately 5500 ms, then capture all six lines.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
