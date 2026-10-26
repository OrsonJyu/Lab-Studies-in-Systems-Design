# Task 4: Repeat hello / world / !!!

## Implementation

The sketch is silent while idle after startup. A positive integer N starts exactly N repetitions of the three-message sequence, one message per second. Invalid input prints an instruction to enter a positive integer. A new valid input restarts the sequence. Invalid input does not interrupt a running sequence.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
Valid: 2 -> hello / world / !!! / hello / world / !!!, then silence. Invalid: 0, -1, 1.5, abc.
```

## Required evidence

Record an initial idle interval. Enter 2 and wait for exactly two complete sequences. Enter 0, -1, 1.5 and abc to show rejection, then enter 1 to show recovery.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
