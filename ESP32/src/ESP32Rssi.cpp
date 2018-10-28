/*
    ESP32Rssi.cpp
    RSSI and distance measurement functions
*/
#include <WiFi.h>
#include <IPAddress.h>
#include <WiFiUdp.h>

#include "ESP32Adhoc.h"
#include "ESP32Rssi.h"

extern ESP32Adhoc Adhoc;
extern WiFiClient client;

void send_to_server(unsigned char* data, unsigned char size)
{

    unsigned char packet[11];
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
    
    packet[10]                             = 0x81;           // End marker

    client.write(packet, sizeof(packet));
    
}