#ifndef ESP32RSSI_H
#define ESP32RSSI_H

/* Calibration messages */
#define NEXT_POSITION   0x66

bool calibrating = false;
long RSSI_ref; // SURY: Added reference variable for inital RSSI
int window = 10; // SURY : Expect a window variable to be set by calibration script, hardcoding it for now  
float eta = 3.14; // SRUY : Expect a value from calibration, hardcoding it for now
int count = 0;
const int window_size = 4;
long RSSI_window[window_size];
long my_distance = 0; 
long set_distance(); // Eggie: function sets (long) my_distance to current distance of car (once stable) 

void send_calibration_next();
void send_calibration_ok();
void check_RSSI(); // SURY : to probe RSSI
#endif