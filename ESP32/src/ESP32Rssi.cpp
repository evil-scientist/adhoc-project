/*
    ESP32Rssi.cpp
    RSSI and distance measurement functions
*/
#include <WiFi.h>
#include <IPAddress.h>
#include <WiFiUdp.h>
#include <math.h>

#include "ESP32Adhoc.h"
#include "ESP32Rssi.h"


bool calibrating = false;
float eta;
long RSSI_ref1;
long RSSI_ref2;
char prev_dist = 0;


void send_to_server(char* data, unsigned char size)
{

    char packet[12];
    packet[0]                              = 0x80;           // Start marker
    packet[PACKET_START_BYTE_LOC +1]       = START_BYTE;
    packet[PACKET_SRC_LOC +1]              = Adhoc.ID_SELF;
    packet[PACKET_DST_LOC +1]              = 0;              // server
    packet[PACKET_INTERMEDIATE_SRC_LOC +1] = 0;
    packet[PACKET_INTERNAL_CMD_LOC +1]     = 0;
    packet[PACKET_COUNTER_HIGH_LOC +1]     = 0;
    packet[PACKET_COUNTER_LOW_LOC +1]      = 0;
    packet[PACKET_DATA_LENGTH_LOC +1]      = size;
    
    for (int i=0; i< size; i++) {
        packet[PACKET_DATA_LOC + 1 + i] = data[i];
    }
    
    packet[11]   = 0x81;                                     // End marker

    client.write(packet, sizeof(packet)); 
}


long avg_rssi(int n_samples)
{

    long avg_rssi = 0;
    for (int i=0; i < n_samples; i++) {

        // DEBUGGING
        long tmp = Adhoc.get_RSSI();
        avg_rssi += tmp;
        Serial.print("RSSI no. ");
        Serial.print(i);
        Serial.print(" = ");
        Serial.print(tmp);
        Serial.println("");

        delay(250);             // Sampling period hardcoded for now
    }

    avg_rssi = avg_rssi / n_samples;

    Serial.print("Avg RSSI: ");
    Serial.println(avg_rssi);
    return avg_rssi;
}


float calc_eta(long RSSI_ref1, long RSSI_ref2, int dist_1, int dist_2)
{
    return (RSSI_ref1 - RSSI_ref2) / (10*log10(dist_2/dist_1));
}