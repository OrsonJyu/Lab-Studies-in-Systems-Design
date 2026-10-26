# In-Class Activity 6

Programming with the IO_Control library, 16 October 2026.

## Task 1

A scheduled handler named iocontrolHandler starts at 1500 ms after CPU start and prints the welcome message every 100 ms.

**Test cases:**

```text
No input. Expected first message: Welcome, current time since start = 1500
```

**Source archive:** `Task01_Sketch.zip`.

## Task 2

A six-state FSM prints one message at each absolute target time: 2000, 3000, 3500, 4000, 4500 and 5500 ms. It then stays idle until reset. Double quotation marks are included around School of Design, as shown in the brief.

**Test cases:**

```text
No input. Expected: At t = 2000, Hello; 3000, from; 3500, "School; 4000, of; 4500, Design"; 5500, !!!
```

**Source archive:** `Task02_Sketch.zip`.

## Task 3

The sketch calls String.toInt() to convert a complete input line to a long, then adds 15 and prints the result. An int64_t intermediate prevents overflow during addition. The conversion itself follows the installed Arduino core behavior.

**Test cases:**

```text
10 -> 25; -5 -> 10; 0 -> 15; 123abc -> 138; abc -> 15; 3.14 -> 18
```

**Source archive:** `Task03_Sketch.zip`.

## Task 4

The sketch is silent while idle after startup. A positive integer N starts exactly N repetitions of the three-message sequence, one message per second. Invalid input prints an instruction to enter a positive integer. A new valid input restarts the sequence. Invalid input does not interrupt a running sequence.

**Test cases:**

```text
Valid: 2 -> hello / world / !!! / hello / world / !!!, then silence. Invalid: 0, -1, 1.5, abc.
```

**Source archive:** `Task04_Sketch.zip`.

## Task 5

The four-state FSM uses durations 1000, 1500, 2000 and 2500 ms initially. Commands state,duration update the selected duration. A change to the current state applies from the original state entry time; if its new duration has already elapsed, it advances immediately. The original s command still skips a state.

**Test cases:**

```text
0,1200; 1,700; s; 4,1000; 2,abc
```

**Source archive:** `Task05_Sketch.zip`.

## Task 6

LED 0 is IO12 and LED 1 is IO13. The four-field form starts immediately. The five-field form adds a relative start delay. Count 0 means repeat indefinitely. Every full ON plus OFF interval counts as one cycle; finite sequences end LOW. A new valid command replaces only the addressed LED, immediately drives it LOW, then honors the new start delay.

**Test cases:**

```text
Case 1: 0,1000,500,10
Case 2: 1,500,1000,0 (then 1,100,100,1)
Case 3: 0,1000,1000,500,10
Independent: 0,100,200,3 and 1,150,250,4
```

**Source archive:** `Task06_Sketch.zip`.

## Task 7

Four comma-separated values select a one-shot playlist for IO12. 0 = X (-..-), 1 = Y (-.--), 2 = Z (--..). A dot is 200 ms, a dash is 600 ms, a within-letter gap is 200 ms and each letter ends with a 600 ms gap. -1 plays a LOW-only 2000 ms pause. A valid command received during a playlist is rejected as Busy; the active playlist finishes unchanged.

**Test cases:**

```text
Case 1: 0,2,1,2 -> X, Z, Y, Z
Case 2: 1,2,-1,0 -> Y, Z, OFF for 2000 ms, X
```

**Source archive:** `Task07_Sketch.zip`.

## Task 8

The BOOT button on IO09 is active LOW. Interrupts detect changes; a 20 ms stable-level check suppresses bounce. On release, a duration below 500 ms prints short pressed; a duration of 500 ms or longer prints long pressed. A button already held at startup is ignored until released because its actual press start time is unknown.

**Test cases:**

```text
~200 ms -> short pressed
~1000 ms -> long pressed
Exactly 500 ms -> long pressed
```

**Source archive:** `Task08_Sketch.zip`.
