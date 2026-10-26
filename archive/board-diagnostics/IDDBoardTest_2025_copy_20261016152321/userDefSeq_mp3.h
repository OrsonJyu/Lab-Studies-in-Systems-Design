UARTControl hwUartCtrl_0;

DFPlayerMP3Control mp3Ctrl_0;

DFPlayerSequence mp3Seq_hello;
DFPlayerSequence mp3Seq_shake;

/*
  commands:
  addCommand(index, volume, duration_ms, loop_after_end, fade_in_time, fade_out_time)
  - index - index of the MP3 file in micro SD card; 0 for no audio, 1 refers to the first file, 2 for second, and so on
  - volume - from 0 to 30 (30 is maximum volume)
  - duration_ms - in milliseconds
  - loop_after_end - true if loop after end, false if not
  - fade_in_time - time in milliseconds for fade-in
  - fade_out_time - time in milliseconds for fade-out
  
  addPause(duration_ms);
  - duration_ms - in milliseconds
*/


err_t initMp3CtrlObjs() {
  err_t err;
  err = hwUartCtrl_0.init(1, 19, 18, -1, -1, 9600, UART_8N1);
  if (err != Control_OK) {
    Serial.print("Failed to init UARTControl (HW). Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          Serial.println("UARTControl is active already");
          break;
        }
    }
  }

  //  MP3 player is associated with IO19, IO18 and IO08
  err = mp3Ctrl_0.init(hwUartCtrl_0, 8);
  if (err) {
    return err;
  }
  mp3Ctrl_0.enableScheduler(0, 100, nullptr);

  return Control_OK;
}

err_t clearMp3CtrlObjs() {

  mp3Seq_hello.clearCommand();
  mp3Seq_shake.clearCommand();

  mp3Ctrl_0.release();
  hwUartCtrl_0.release();

  return Control_OK;
}

bool isAllFinish_mp3() {

  if (mp3Ctrl_0.isPlaying()) {
    return false;
  }
  return true;
}

err_t setMp3Sequences() {
  err_t err;

  //
  //  define mp3Seq_hello
  //
  //err = mp3Seq_hello.addCommand(2, 0, 600, true);
  err = mp3Seq_hello.addPause(600);
  if (err) {
    return err;
  }

  err = mp3Seq_hello.addCommand(2, 30, 500, true);
  if (err) {
    return err;
  }

  err = mp3Seq_hello.addCommand(3, 30, 500, true);
  if (err) {
    return err;
  }

  //
  //  define mp3Seq_shake
  //
  err = mp3Seq_shake.addCommand(1, 20, 4500, true);
  if (err) {
    return err;
  }
  return Control_OK;
}