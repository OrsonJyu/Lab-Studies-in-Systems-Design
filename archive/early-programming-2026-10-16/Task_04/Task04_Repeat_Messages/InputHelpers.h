#pragma once
// Shared input helpers, copied into each sketch so every ZIP is self-contained.
// Read a complete LF / CR / CRLF line without blocking the scheduler.
class SerialLineReader {
  String pending;
  bool overflow = false;
public:
  bool read(String &line) {
    unsigned int budget = 64;
    while (Serial.available() > 0 && budget-- > 0) {
      char c = (char)Serial.read();
      if (c == '\r' || c == '\n') {
        if (overflow) {
          Serial.println("Error: input line is too long (maximum 127 characters).");
          pending = ""; overflow = false; continue;
        }
        if (pending.length() == 0) continue; // also consumes the LF in CRLF
        line = pending; pending = ""; return true;
      }
      if (pending.length() < 127 && !overflow) pending += c;
      else overflow = true;
    }
    return false;
  }
};
// Unlike String.toInt(), require the entire token to be a signed decimal integer.
// Accept surrounding spaces and +/-; reject decimals, missing fields and overflow.
bool parseInteger(String token, long &value) {
  token.trim();
  if (token.length() == 0) return false;
  unsigned int p = 0;
  bool negative = false;
  if (token[0] == '+' || token[0] == '-') {
    negative = token[0] == '-'; p++;
  }
  if (p == token.length()) return false;
  uint64_t magnitude = 0;
  const uint64_t limit = negative ? 2147483648ULL : 2147483647ULL;
  for (; p < token.length(); p++) {
    const char c = token[p];
    if (c < '0' || c > '9') return false;
    magnitude = magnitude * 10 + (c - '0');
    if (magnitude > limit) return false;
  }
  value = negative ? (long)(-(int64_t)magnitude) : (long)magnitude;
  return true;
}
int parseCsv(const String &line, long values[], int capacity) {
  int start = 0, count = 0;
  while (true) {
    if (count == capacity) return -1;
    int comma = line.indexOf(',', start);
    String token = comma < 0 ? line.substring(start) : line.substring(start, comma);
    if (!parseInteger(token, values[count])) return -1;
    count++;
    if (comma < 0) return count;
    start = comma + 1;
  }
}
