#pragma once
#include <IO_Control.h>
#include <limits.h>
// Non-blocking newline input: never stall the IO_Control scheduler.
// Select Newline or Both NL & CR, 115200 baud in Serial Monitor.
String serialLine;
bool lineOverflow = false;
bool readCommand(String &command) {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\r') continue;
    if (c == '\n') {
      if (lineOverflow) {
        Serial.println("Error: command too long.");
        lineOverflow = false; serialLine = ""; continue;
      }
      command = serialLine; serialLine = "";
      command.trim(); return true;
    }
    if (!lineOverflow) {
      if (serialLine.length() >= 120) { lineOverflow = true; serialLine = ""; }
      else serialLine += c;
    }
  }
  return false;
}
// Strict integer validation, including overflow (unlike String::toInt()).
bool parseInteger(String text, long &value) {
  text.trim(); if (!text.length()) return false;
  unsigned int i = 0; bool negative = false;
  if (text[0] == '-' || text[0] == '+') { negative = text[0] == '-'; i++; }
  if (i == text.length()) return false;
  unsigned long n = 0;
  const unsigned long limit = negative ? (unsigned long)LONG_MAX + 1UL : LONG_MAX;
  for (; i < text.length(); ++i) {
    if (text[i] < '0' || text[i] > '9') return false;
    unsigned int digit = text[i] - '0';
    if (n > (limit - digit) / 10UL) return false;
    n = n * 10UL + digit;
  }
  value = negative ? (n == (unsigned long)LONG_MAX + 1UL ? LONG_MIN : -(long)n) : (long)n;
  return true;
}
int parseCSV(const String &line, long *values, int capacity) {
  int start = 0, count = 0;
  while (true) {
    if (count >= capacity) return -1;
    int comma = line.indexOf(',', start);
    String part = comma < 0 ? line.substring(start) : line.substring(start, comma);
    if (!parseInteger(part, values[count++])) return -1;
    if (comma < 0) return count;
    start = comma + 1;
  }
}
