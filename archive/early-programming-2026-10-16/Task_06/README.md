# Task 6: Two independent LED blink controllers

## Implementation

LED 0 is IO12 and LED 1 is IO13. The four-field form starts immediately. The five-field form adds a relative start delay. Count 0 means repeat indefinitely. Every full ON plus OFF interval counts as one cycle; finite sequences end LOW. A new valid command replaces only the addressed LED, immediately drives it LOW, then honors the new start delay.

## Board and monitor

- Board: AirM2M CORE ESP32C3 (Luatos ESP32C3).
- Arduino ESP32 core: 3.3.12; installed course IO_Control library.
- USB CDC On Boot: Disabled (board uses its USB-to-UART bridge).
- Serial Monitor: 115200 baud; New Line or Both NL & CR.
- Open the .ino inside the same-named sketch folder.

## Test inputs and expected behavior

```text
Case 1: 0,1000,500,10
Case 2: 1,500,1000,0 (then 1,100,100,1)
Case 3: 0,1000,1000,500,10
Independent: 0,100,200,3 and 1,150,250,4
```

## Required evidence

Record one video for each of the three required examples. Let the finite examples reach cycles=10. For the infinite example, record several cycles and send 1,100,100,1 to show that it can be replaced. Add a fourth test with both LEDs to demonstrate independence.

Screenshots / recordings must come from a real board run. Expected output descriptions and host tests are not substitutes for the required evidence. See the root README for the final evidence status.
