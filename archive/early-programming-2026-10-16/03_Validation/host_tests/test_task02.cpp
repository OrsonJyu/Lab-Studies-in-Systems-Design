#include "../../Task_02/Task02_Timed_FSM/Task02_Timed_FSM.ino"
int main(){setup();runUntil(8000);require(Serial.output=="At t = 2000, Hello\nAt t = 3000, from\nAt t = 3500, \"School\nAt t = 4000, of\nAt t = 4500, Design\"\nAt t = 5500, !!!\n","all six absolute times and quotes");
std::cout<<"PASS Task 2\n";}
