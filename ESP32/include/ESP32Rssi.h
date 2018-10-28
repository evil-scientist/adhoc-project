#ifndef ESP32RSSI_H
#define ESP32RSSI_H

/* Calibration messages */
#define NEXT_POSITION           0x66
#define CALIBRATION_DONE        0x67

extern bool calibrating;

void send_to_server(unsigned char *data, unsigned char size);

#endif