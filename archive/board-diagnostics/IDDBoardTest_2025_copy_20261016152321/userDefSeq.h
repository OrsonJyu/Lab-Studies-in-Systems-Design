#include "userDefSeq_servo.h"
#include "userDefSeq_mp3.h"
#include "userDefSeq_addrLed.h"

struct SequenceSet {
  std::vector<ServoCtrlSeqPair> servoPairs;
  std::vector<AddrLEDCtrlSeqPair> addrLedPairs;
  DFPlayerSequence mp3Sequence;
};

SequenceSet sequenceSets[12];

uint8_t sequenceSetsCount = 0;

err_t initCtrlObjs() {
  err_t err;
  err = initServoCtrlObjs();
  if (err) {
    Serial.println("Error occurs when initializing ServoControl objects");
    return err;
  }
  err = initAddrLedCtrlObjs();
  if (err) {
    Serial.println("Error occurs when initializing AddrLEDControl objects");
    return err;
  }
  err = initMp3CtrlObjs();
  if (err) {
    Serial.println("Error occurs when initializing DFPlayerMP3Control objects");
    return err;
  }

  return Control_OK;
}

err_t releaseCtrlObjs() {
  for (int i = 0; i < 12; i++) {
    sequenceSets[i].servoPairs.clear();                // Empties the servoPairs vector
    sequenceSets[i].addrLedPairs.clear();              // Empties the addrLedPairs vector
    sequenceSets[i].mp3Sequence = DFPlayerSequence();  // Resets mp3Sequence to default
  }

  err_t err;

  err = clearServoCtrlObjs();

  if (err) {
    Serial.println("Error occurs when clearing ServoControl objects");
    return err;
  }

  err = clearAddrLedCtrlObjs();

  if (err) {
    Serial.println("Error occurs when clearing AddrLEDControl objects");
    return err;
  }

  err = clearMp3CtrlObjs();

  if (err) {
    Serial.println("Error occurs when clearing DFPlayerMP3Control objects");
    return err;
  }

  return Control_OK;
}

bool isAllFinish() {
  if (isAllFinish_servo() && isAllFinish_addrLed()/* && isAllFinish_mp3()*/) {
    return true;
  }
  return false;
}

err_t setSequences() {
  err_t err;

  err = setServoSequences();

  if (err) {
    Serial.println("Error occurs when setting servo sequences");
    return err;
  }

  err = setAddrLedSequences();

  if (err) {
    Serial.println("Error occurs when setting addrLed sequences");
    return err;
  }

  err = setMp3Sequences();

  if (err) {
    Serial.println("Error occurs when setting MP3 sequences");
    return err;
  }

  return Control_OK;
}

void playSetSequence(uint8_t index) {
  if (index > 11) {
    return;
  }

  mp3Ctrl_0.playRelTime(sequenceSets[index].mp3Sequence, 0, 1);

  for (int i = 0; i < sequenceSets[index].servoPairs.size(); i++) {
    sequenceSets[index].servoPairs[i].servoCtrl->playRelTime(sequenceSets[index].servoPairs[i].servoSeq, 0, 1);
  }

  for (int j = 0; j < sequenceSets[index].addrLedPairs.size(); j++) {
    addrLedCtrl_0.playRelTime(sequenceSets[index].addrLedPairs[j].targets, sequenceSets[index].addrLedPairs[j].addrLedSeq, 0, 1);
  }
}


ServoCtrlSeqPair& createServoSeq(ServoControl& _servoCtrl, ServoSequence& _servoSeq) {
  ServoCtrlSeqPair* seqPair = new ServoCtrlSeqPair();
  seqPair->servoCtrl = &_servoCtrl;
  seqPair->servoSeq = _servoSeq;
  return *seqPair;
}

AddrLEDCtrlSeqPair& createAddrLedSeq(const std::vector<int>& _targets, AddrLEDSequence& _addrLedSeq) {
  AddrLEDCtrlSeqPair* seqPair = new AddrLEDCtrlSeqPair();
  seqPair->targets = _targets;
  seqPair->addrLedSeq = _addrLedSeq;
  return *seqPair;
}

void addServoSeq(uint8_t index, ServoCtrlSeqPair _servoSeqPair) {
  if (index < 12) {
    sequenceSets[index].servoPairs.push_back(_servoSeqPair);
  }
  return;
}

void addAddrLedSeq(uint8_t index, AddrLEDCtrlSeqPair _addrSeqPair) {
  if (index < 12) {
    sequenceSets[index].addrLedPairs.push_back(_addrSeqPair);
  }
  return;
}

void addMP3Seq(uint8_t index, DFPlayerSequence _mp3Seq) {
  if (index < 12) {
    sequenceSets[index].mp3Sequence = _mp3Seq;
  }
  return;
}

err_t setupSequences() {
  err_t err = setSequences();
  if (err) {
    return err;
  }

  createAddrLedTargets();

  // define output sequences for touch point 0
  {
    ServoCtrlSeqPair servoPair_left = createServoSeq(servoCtrl_0, servoSeq_left);
    addServoSeq(0, servoPair_left);
    ServoCtrlSeqPair servoPair_nod = createServoSeq(servoCtrl_1, servoSeq_nod);
    addServoSeq(0, servoPair_nod);

    addMP3Seq(0, mp3Seq_hello);

    AddrLEDCtrlSeqPair addrLedPair_wink1 = createAddrLedSeq(targets_1, addrLedSeq_wink1);
    AddrLEDCtrlSeqPair addrLedPair_wink2 = createAddrLedSeq(targets_2, addrLedSeq_wink2);
    addAddrLedSeq(0, addrLedPair_wink1);
    addAddrLedSeq(0, addrLedPair_wink2);
  }

  // define output sequences for touch point 1
  {
    ServoCtrlSeqPair servoPair_leftright = createServoSeq(servoCtrl_0, servoSeq_leftright);
    ServoCtrlSeqPair servoPair_shake = createServoSeq(servoCtrl_1, servoSeq_shake);
    addServoSeq(1, servoPair_leftright);
    addServoSeq(1, servoPair_shake);

    addMP3Seq(1, mp3Seq_shake);

    AddrLEDCtrlSeqPair addrLedPair_shake = createAddrLedSeq(targets_0, addrLedSeq_shake);
    addAddrLedSeq(1, addrLedPair_shake);
  
  }

  return Control_OK;
}

//init Control objects

//add commands to sequence

/*ServoCtrlSeqPair servoPair_0 = createServoSeq(servoCtrl_0, servoSeq_0);

ServoCtrlSeqPair servoPair_1 = createServoSeq(servoCtrl_1, servoSeq_1);

std::vector<int> targets_0;
for (int i = 0; i < 10; i++) {
  targets_0.push_back(i);
}

AddrLEDCtrlSeqPair addrLedPair_0 = createAddrLedSeq(targets_0, addrLedSeq_0);

addServoSeq(0, servoPair_0);
addServoSeq(0, servoPair_1);
addAddrLedSeq(0, addrLedPair_0);
addMP3Seq(0, mp3Seq_0);*/