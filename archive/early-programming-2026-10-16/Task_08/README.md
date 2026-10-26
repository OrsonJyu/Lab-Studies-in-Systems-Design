# Task 8: Short and long BOOT button presses

## Implementation

The BOOT button on IO09 is active LOW. Interrupts detect changes; a 20 ms stable-level check suppresses bounce. On release, a duration below 500 ms prints short pressed; a duration of 500 ms or longer prints long pressed. A button already held at startup is ignored until released because its actual press start time is unknown.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
~200 ms -> short pressed
~1000 ms -> long pressed
Exactly 500 ms -> long pressed
```

## Required evidence

Record both the physical BOOT button action and Serial Monitor in the same video. Press and release once for about 200 ms and once for about 1000 ms. Do not hold BOOT while resetting the board.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
