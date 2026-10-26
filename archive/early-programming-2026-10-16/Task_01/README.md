# Task 1: Serial welcome

## Implementation

A scheduled handler named iocontrolHandler starts at 1500 ms after CPU start and prints the welcome message every 100 ms.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
No input. Expected first message: Welcome, current time since start = 1500
```

## Required evidence

Reset the board with the Serial Monitor already open. Capture the first lines around 1500, 1600, 1700 ms. Small scheduler jitter is normal.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
