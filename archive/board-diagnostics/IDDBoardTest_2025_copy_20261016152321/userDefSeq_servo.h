struct ServoCtrlSeqPair {
  ServoControl* servoCtrl;
  ServoSequence servoSeq;
};

//  each ServoControl object corresponds to one servo motor
ServoControl servoCtrl_0;
ServoControl servoCtrl_1;

//  one ServoSequence object corresponds to angle of a servo motor at specific time
ServoSequence servoSeq_left;
ServoSequence servoSeq_leftright;
ServoSequence servoSeq_shake;
ServoSequence servoSeq_nod;

/*
  commands:
  
  addSetAngle(duration_ms, angle, ctrl)
  - duration_ms - in milliseconds
  - angle - in degree
  addMoveFromToAngle(duration_ms, start_angle, end_angle, ctrl)
  - duration_ms - in milliseconds
  - start_angle - starting angle, in degree
  - end_angle - ending angle, in degree
*/

err_t initServoCtrlObjs() {
  err_t err;
  //  associate servoCtrl_0 with IO12
  err = servoCtrl_0.init(8, true);
  if (err) {
    return err;
  }
  servoCtrl_0.enableScheduler(0, 100, nullptr);

  //  associate servoCtrl_1 with IO13
  err = servoCtrl_1.init(18, true);
  if (err) {
    return err;
  }
  servoCtrl_1.enableScheduler(0, 100, nullptr);

  //  Note that servoCtrl_0 and servoCtrl_1 are having the same angle range

  return Control_OK;
}

err_t clearServoCtrlObjs() {

  //  clear all ServoSequence objects
  servoSeq_left.clearCommand();
  servoSeq_leftright.clearCommand();
  servoSeq_shake.clearCommand();
  servoSeq_nod.clearCommand();

  //  release all ServoControl objects
  servoCtrl_0.release();
  servoCtrl_1.release();

  return Control_OK;
}

bool isAllFinish_servo() {

  if (servoCtrl_0.isPlaying()) {
    return false;
  }
  if (servoCtrl_1.isPlaying()) {
    return false;
  }

  return true;
}

err_t setServoSequences() {
  err_t err;

  //
  //  define servoSeq_left
  //
  err = servoSeq_left.addMoveFromToAngle(500, 80, 100, servoCtrl_0);
  if (err) {
    return err;
  }
  err = servoSeq_left.addSetAngle(1200, 100, servoCtrl_0);
  if (err) {
    return err;
  }
  err = servoSeq_left.addMoveFromToAngle(500, 100, 80, servoCtrl_0);
  if (err) {
    return err;
  }
  
  //
  //  define servoSeq_nod
  //
  err = servoSeq_nod.addSetAngle(600, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_nod.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_nod.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_nod.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_nod.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_nod.addSetAngle(600, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  
  //
  //  define servoSeq_leftright
  //
  err = servoSeq_leftright.addSetAngle(500, 80, servoCtrl_0);
  if (err) {
    return err;
  }
  err = servoSeq_leftright.addMoveFromToAngle(1000, 80, 100, servoCtrl_0);
  if (err) {
    return err;
  }
  err = servoSeq_leftright.addMoveFromToAngle(2000, 100, 60, servoCtrl_0);
  if (err) {
    return err;
  }
  err = servoSeq_leftright.addMoveFromToAngle(1000, 60, 80, servoCtrl_0);
  if (err) {
    return err;
  }
  
  //
  //  define servoSeq_shake
  //
  err = servoSeq_shake.addSetAngle(500, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 90, 45, servoCtrl_1);
  if (err) {
    return err;
  }
  err = servoSeq_shake.addMoveFromToAngle(250, 45, 90, servoCtrl_1);
  if (err) {
    return err;
  }

  return Control_OK;
}