# Validation environment

- Date: 2026-10-16 (Hong Kong).
- Arduino CLI bundled with Arduino IDE 2.3.10.
- FQBN: esp32:esp32:AirM2M_CORE_ESP32C3:PartitionScheme=huge_app
- ESP32 core 3.3.12; local course IO_Control 1.0.0, precompiled ESP32C3 archive.
- Each submitted sketch compiles against the actual installed library.
- Host tests include the actual submitted .ino files and run deterministic scheduler / serial / GPIO adapters; these do not test the binary library, electrical behavior or real serial timing.
- Host tests cover exact first invocation, timed FSM sequence and quotes, +15 conversion, silent startup, positive integer validation, exact repetition count, current-state duration edits, independent LEDs, delayed start, full cycle count, infinite repeat replacement, Morse order, invalid playlists, 500 ms threshold and contact bounce.

The local course example Example3_2 deliberately contains an invalid floating-point modulo expression; it is preserved unchanged as teaching material and is not a submitted solution.
