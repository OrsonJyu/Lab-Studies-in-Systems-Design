# Task 3: Convert input to integer and add 15

## Implementation

The sketch calls String.toInt() to convert a complete input line to a long, then adds 15 and prints the result. An int64_t intermediate prevents overflow during addition. The conversion itself follows the installed Arduino core behavior.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
10 -> 25; -5 -> 10; 0 -> 15; 123abc -> 138; abc -> 15; 3.14 -> 18
```

## Required evidence

Enter 10, -5, 0, 123abc, abc and 3.14 on separate lines. Capture the corresponding results.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.

## String.toInt() documentation

Arduino documents that toInt() returns a long, converts a numeric prefix and stops at the first non-numeric part. It returns 0 when no valid integer conversion can be made. Therefore it does not by itself validate a positive-integer-only command; Tasks 4-7 use strict token validation instead.

Official reference: https://docs.arduino.cc/language-reference/en/variables/data-types/stringObject/Functions/toInt/
