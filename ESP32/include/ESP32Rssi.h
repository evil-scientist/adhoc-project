#ifndef ESP32RSSI_H
#define ESP32RSSI_H

/* Calibration messages */
#define NEXT_POSITION   0x66

bool calibrating = false;

void send_calibration_next();
void send_calibration_ok();

#endif