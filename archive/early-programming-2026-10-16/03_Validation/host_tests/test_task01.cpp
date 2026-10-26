#include "../../Task_01/Task01_Serial_Welcome/Task01_Serial_Welcome.ino"
int main(){setup();runUntil(1499);require(Serial.output.empty(),"silent before 1500");runUntil(1700);require(Serial.output=="Welcome, current time since start = 1500\nWelcome, current time since start = 1600\nWelcome, current time since start = 1700\n","1500 first / 100ms interval");
std::cout<<"PASS Task 1\n";}
