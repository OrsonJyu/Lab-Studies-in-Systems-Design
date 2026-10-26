#pragma once
#include <string>
#include <vector>
#include <deque>
#include <iostream>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <algorithm>
using ulong_t=unsigned long;
using err_t=int;
const int Control_OK=0,HIGH=1,LOW=0,INPUT_PULLUP=2,CHANGE=3;
unsigned long fakeNow=0;
unsigned long millis(){return fakeNow;}
class String {
 std::string s;
public:
 String(const char *x=""):s(x){} String(std::string x):s(x){}
 size_t length()const{return s.length();}
 char operator[](size_t p)const{return s[p];}
 String& operator+=(char c){s+=c;return *this;}
 bool operator==(const char*x)const{return s==x;}
 void trim(){auto a=s.find_first_not_of(" \t\r\n");if(a==std::string::npos){s.clear();return;}auto b=s.find_last_not_of(" \t\r\n");s=s.substr(a,b-a+1);}
 int indexOf(char c,int p=0)const{auto n=s.find(c,p);return n==std::string::npos?-1:(int)n;}
 String substring(int a,int b=-1)const{return s.substr(a,b<0?std::string::npos:b-a);}
 long toInt()const{return (int32_t)strtol(s.c_str(),nullptr,10);}
 friend std::ostream&operator<<(std::ostream&o,const String&v){return o<<v.s;}
};
struct FakeSerial {
 std::deque<char> input;
 std::string output;
 void begin(int){}
 int available(){return input.size();}
 int read(){int c=input.front();input.pop_front();return c;}
 template<class T>void print(T v){std::ostringstream o;o<<v;output+=o.str();}
 template<class T>void println(T v){print(v);output+='\n';}
 void println(){output+='\n';}
 template<class...A>void printf(const char*f,A...a){char b[512];snprintf(b,sizeof b,f,a...);output+=b;}
 void send(std::string s){for(char c:s)input.push_back(c);}
} Serial;
class Control;
using Handler=void(*)(Control&);
std::vector<Control*> controls;
class Control {
 struct Timeout{bool active=false;unsigned long due=0;Handler h=nullptr;};
 std::vector<Timeout> timeouts;
 Handler handler=nullptr;unsigned long next=0,interval=1;
public:
 unsigned long updated=0;
 virtual ~Control(){}
 unsigned long getUpdateTime(){return updated;}
 int enableScheduler(unsigned long start,unsigned long every,Handler h,int count=1){handler=h;next=start;interval=every;timeouts.resize(count);controls.push_back(this);return 0;}
 int setTimeoutByRelTime(int id,Handler h,unsigned long dt,bool immediate){if(id>=(int)timeouts.size())return -1;timeouts[id]={true,updated+dt,h};if(dt==0&&immediate){timeouts[id].active=false;h(*this);}return 0;}
 int stopTimeout(int id){if(id<(int)timeouts.size())timeouts[id].active=false;return 0;}
 bool isTimeoutActive(int id){return timeouts[id].active;}
 virtual void pre(){}
 void tick(){if(!handler||fakeNow<next)return;updated=fakeNow;next=fakeNow+interval;pre();for(auto&t:timeouts)if(t.active&&fakeNow>=t.due){auto h=t.h;t.active=false;h(*this);}handler(*this);}
};
#define DeclareHandler(name,obj,cls,...) void name(Control& base){cls& obj=static_cast<cls&>(base);__VA_ARGS__}
class IOControl:public Control{public:void begin(){}} IO_Control;
struct BinOutSequence{std::vector<std::pair<unsigned long,int>> seq;int addSetState(unsigned long t,int s){seq.push_back({t,s});return 0;}};
struct BinOutControl:Control {
 int val=LOW;bool ended=false,playing=false;BinOutSequence*sequence=nullptr;int step=0;unsigned long due=0;
 int init(int,int v){val=v;return 0;}
 int read(){return val;}
 int write(int v){val=v;return 0;}
 bool isAllSeqEnded(){return ended;}
 int playRelTime(BinOutSequence&s,unsigned long start,int){sequence=&s;step=0;due=fakeNow+start;playing=true;ended=false;return 0;}
 void pre()override{ended=false;if(playing&&fakeNow>=due){if(step==(int)sequence->seq.size()){playing=false;ended=true;}else{auto cmd=sequence->seq[step++];val=cmd.second;due=fakeNow+cmd.first;}}}
};
struct BinInControl:Control{int val=HIGH;bool triggered=false;unsigned long event=0;int init(int,int){return 0;}int read(){return val;}int enableInterrupt(int){return 0;}bool isBinInTriggered(){bool b=triggered;triggered=false;return b;}int getInterruptState(){return val;}int getInterruptTime(){return event;}void inject(int v){val=v;triggered=true;event=fakeNow;}};
void runUntil(unsigned long end){for(;fakeNow<=end;fakeNow++){for(auto*c:controls)c->tick();}}
void sendAt(unsigned long at,const char*s){runUntil(at-1);Serial.send(std::string(s)+"\n");runUntil(at+2);}
void require(bool ok,const char*msg){if(!ok){std::cerr<<"FAIL: "<<msg<<"\n";std::exit(1);}}
int occurrences(const std::string&text,const std::string&token){int n=0;size_t p=0;while((p=text.find(token,p))!=std::string::npos){n++;p+=token.size();}return n;}
