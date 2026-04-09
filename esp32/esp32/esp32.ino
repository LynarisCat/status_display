#define ENABLE_GxEPD2_GFX 1
#include <GxEPD2_4G_4G.h>
#include <GxEPD2_4G_BW.h>
#include <SPI.h>

#include "GxEPD2_4G_display_selection_new_style.h"

#include <WiFi.h>
#include <HTTPClient.h>

#include "secrets.h"
#define BITMAP_BYTES  9472

static uint8_t test_src[9472];
static uint8_t bw[4736];
static uint8_t red[4736];

void connectWiFi() {
    //Serial.print("Connecting to WiFi");
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        //Serial.print(".");
    }

    //Serial.println();
    //Serial.println("Connected. IP: " + WiFi.localIP().toString());
}


bool fetchBytemap(uint8_t *buf) {
    HTTPClient http;
    http.begin(SERVER_URL);

    int status = http.GET();
    if (status != HTTP_CODE_OK) {
        //Serial.printf("HTTP error: %d\n", status);
        http.end();
        return false;
    }

    int contentLen = http.getSize();
    if (contentLen != -1 && contentLen != BITMAP_BYTES) {
        //Serial.printf("Wrong size: got %d, need %d\n", contentLen, BITMAP_BYTES);
        http.end();
        return false;
    }

    WiFiClient *stream = http.getStreamPtr();
    int received = 0;
    unsigned long deadline = millis() + 5000;

    while (received < BITMAP_BYTES && millis() < deadline) {
        int available = stream->available();
        if (available > 0) {
            int toRead = min(available, BITMAP_BYTES - received);
            stream->readBytes(buf + received, toRead);
            received += toRead;
        }
        else {
            yield();
        }
    }

    http.end();

    if (received != BITMAP_BYTES) {
        //Serial.printf("Short read: %d / %d bytes\n", received, BITMAP_BYTES);
        return false;
    }

    //Serial.printf("Fetched %d bytes\n", received);
    return true;
}


void printToScreen(uint8_t *buf){
    display.clearScreen();

    display.writeImage_4G(buf, 2, 0, 0, 128, 296);
    display.refresh(false);
    display.hibernate();
}



void setup() {
    delay(2000);
    //Serial.begin(115200);
    display.init();
    display.clearScreen();

    Serial.println("Display ready");
    connectWiFi();
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
    }
    if (fetchBytemap(test_src)) {
        printToScreen(test_src);
    } else {
        //Serial.println("Fetch failed, skipping display update");
    }
    
    //Serial.println("Going to sleep...");
    esp_sleep_enable_timer_wakeup(3600ULL * 1000000ULL);
    esp_deep_sleep_start();
}
