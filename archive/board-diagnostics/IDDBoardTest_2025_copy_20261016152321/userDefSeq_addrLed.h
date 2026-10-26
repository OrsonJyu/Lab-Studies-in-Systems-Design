struct AddrLEDCtrlSeqPair {
  std::vector<int> targets;
  AddrLEDSequence addrLedSeq;
};

//  addrLedCtrl_0 corresponds to the WS2812 LED strip
AddrLEDControl addrLedCtrl_0;

//  LED color sequence
AddrLEDSequence addrLedSeq_wink1;
AddrLEDSequence addrLedSeq_wink2;
AddrLEDSequence addrLedSeq_shake;

//  for defining each group of LED(s)
std::vector<int> targets_0;
std::vector<int> targets_1;
std::vector<int> targets_2;

/*
  commands:
  
  addSetRGB(duration_ms,R,G,B)
  - duration_ms - in milliseconds
  - R, G, B - RGB color value, from 0 to 255
  
  addSetHSV(duration_ms,H,S,V)
  - duration_ms - in millseconds
  - H - hue, from 0 to 359
  - S - saturation, from 0 to 100
  - V - value, from 0 to 100 
  - refer to https://learn.leighcotnoir.com/artspeak/elements-color/hue-value-saturation
  
  addInterpolateRGB(duration_ms,start_R,start_G,start_B,end_R,end_G,end_B)
  - duration_ms - in milliseconds
  - start_R, start_G, start_B - starting value of R, G and B
  - end_R, end_G, end_B - ending value of R, G and B
  
  addInterpolateHSV(duration_ms,start_H,start_S,start_V,end_H,end_S,end_V)
  - duration_ms - in milliseconds
  - start_H, start_S, start_V - starting value of H, S and V
  - end_H, end_S, end_V - ending value of H, S and V
  
*/

err_t initAddrLedCtrlObjs() {
  err_t err;

  err = addrLedCtrl_0.init(19, 20, true);
  //  WS2812 is associated with IO05, and with 20 LEDs on the strip
  if (err) {
    return err;
  }

  addrLedCtrl_0.enableScheduler(0, 100, nullptr);

  return Control_OK;
}

err_t clearAddrLedCtrlObjs() {

  addrLedSeq_wink1.clearCommand();

  addrLedSeq_wink2.clearCommand();

  addrLedSeq_shake.clearCommand();

  addrLedCtrl_0.setRGB(targets_0, 0, 0, 0);

  addrLedCtrl_0.release();

  return Control_OK;
}

bool isAllFinish_addrLed() {
  if (addrLedCtrl_0.seqObjs.size() == 0) {
    return false;
  }
  bool isAddrLedFinished = true;
  for (int i = 0; i < addrLedCtrl_0.seqObjs.size(); i++) {
    if (addrLedCtrl_0.seqObjs[i] != nullptr) {
      isAddrLedFinished = false;
      return false;
    }
  }

  return true;
}

err_t setAddrLedSequences() {
  err_t err;

  //
  //  define addrLedSeq_wink1
  //
  err = addrLedSeq_wink1.addSetRGB(500, 128, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink1.addSetRGB(50, 0, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink1.addSetRGB(50, 128, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink1.addSetRGB(1000, 128, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink1.addSetRGB(50, 0, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink1.addSetRGB(50, 128, 0, 0);
  if (err) {
    return err;
  }

  //
  //  define addrLedSeq_wink1
  //
  err = addrLedSeq_wink2.addSetRGB(500, 255, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink2.addSetRGB(50, 255, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink2.addSetRGB(50, 255, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink2.addSetRGB(1000, 255, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink2.addSetRGB(50, 0, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_wink2.addSetRGB(50, 255, 0, 0);
  if (err) {
    return err;
  }

  //
  //  define addrLedSeq_shake
  //
  err = addrLedSeq_shake.addSetRGB(500, 255, 0, 0);
  if (err) {
    return err;
  }
  err = addrLedSeq_shake.addInterpolateHSV(4000, 0, 80, 80, 340, 80, 80);
  if (err) {
    return err;
  }

  return Control_OK;
}

void createAddrLedTargets() {

  //  targets_0
  // targets_0.push_back(0);
  // targets_0.push_back(1);
  for (uint8_t i = 0; i < 7; i++) {
    targets_0.push_back(i);
  }


  //  targets_1
  targets_1.push_back(0);
  targets_1.push_back(1);
  targets_1.push_back(2);


  //  targets_2
  targets_2.push_back(3);
  targets_2.push_back(4);
  targets_2.push_back(5);
  targets_2.push_back(6);
}