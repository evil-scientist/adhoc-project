#ifndef ESP32RSSI_H
#define ESP32RSSI_H

/* Calibration messages */
#define CALIBRATE_BOT           0x11        // copied from server CommandList.h = ugly hack
#define GET_DISTANCE            0x12        // same
#define NEXT_POSITION           0x66
#define CALIBRATION_DONE        0x67

/* Global variables */
extern bool calibrating;            // calibration state flag
extern float eta;                   // pathloss exponent
extern long RSSI_ref1;              // reference RSSI @ distance 1
extern long RSSI_ref2;              // reference RSSI @ distance 2

extern ESP32Adhoc Adhoc;
extern WiFiClient client;

void send_to_server(char *data, unsigned char size);
long avg_rssi(int n_samples);
float calc_eta(long RSSI_ref1, long RSSI_ref2, int dist_1, int dist_2);


#endif