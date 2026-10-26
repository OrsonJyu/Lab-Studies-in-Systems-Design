#include "../../Task_05/Task05_Editable_State_Durations/Task05_Editable_State_Durations.ino"
int main(){setup();sendAt(500,"0,1200");runUntil(1300);require(state==1,"current state updated relative to original entry");require(stateDuration[0]==1200,"new duration stored");sendAt(1400,"4,1000");sendAt(1500,"2,abc");require(stateDuration[2]==2000,"invalid duration cannot change state2");sendAt(1600,"s");require(state==2,"skip preserved");sendAt(1700,"2,1");require(state==3,"elapsed exceeds new duration advances now");
std::cout<<"PASS Task 5\n";}
