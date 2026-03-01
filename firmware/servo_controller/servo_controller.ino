/*
 * Servo Controller — Receives angle commands from Raspberry Pi over serial
 * and drives servos via PCA9685 PWM driver board.
 *
 * Hardware:
 *   - Arduino Mega 2560
 *   - PCA9685 16-channel servo driver (I2C: SDA=20, SCL=21)
 *   - Up to 8 MG996R servos on channels 0-7
 *   - 6V dedicated servo power supply on PCA9685 V+ terminal
 *
 * Serial Protocol:
 *   Receives: <S0:90,S1:45,S2:180,S3:30,S4:60,S5:90,S6:120,S7:90>
 *   Each S# is a servo channel (0-7) with an angle value (0-180).
 *   Messages are framed with < and > for reliable parsing.
 *
 * Dependencies:
 *   - Adafruit PWM Servo Driver Library (install via Arduino Library Manager)
 *   - Wire.h (built-in)
 */

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

// PCA9685 I2C address (default 0x40)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Number of active servo channels
#define NUM_SERVOS 8

// Default pulse width range (in PCA9685 ticks, 0-4095)
// These are safe defaults — run calibration to find exact values per servo
#define DEFAULT_SERVO_MIN 150   // ~0.5ms pulse → ~0 degrees
#define DEFAULT_SERVO_MAX 550   // ~2.5ms pulse → ~180 degrees

// Per-servo calibration (min/max ticks)
// Update these after running scripts/calibrate_servos.py
uint16_t servoMin[NUM_SERVOS] = {150, 150, 150, 150, 150, 200, 150, 150};
uint16_t servoMax[NUM_SERVOS] = {550, 550, 550, 550, 550, 450, 550, 550};

// Current and target angles for each servo
int currentAngle[NUM_SERVOS] = {90, 90, 90, 90, 90, 90, 90, 90};
int targetAngle[NUM_SERVOS]  = {90, 90, 90, 90, 90, 90, 90, 90};

// Smoothing: max degrees per update cycle (reduces jitter)
#define MAX_STEP 5

// Serial parsing
#define SERIAL_BAUD 115200
#define MSG_BUF_SIZE 128
char msgBuffer[MSG_BUF_SIZE];
int msgIndex = 0;
bool receiving = false;

// ---------------------------------------------------------------------------
// Setup
// ---------------------------------------------------------------------------

void setup() {
    Serial.begin(SERIAL_BAUD);

    // Initialize PCA9685
    pwm.begin();
    pwm.setOscillatorFrequency(27000000);  // Internal oscillator calibration
    pwm.setPWMFreq(50);  // 50 Hz = standard servo frequency (20ms period)

    delay(10);

    // Move all servos to center position on startup
    for (int i = 0; i < NUM_SERVOS; i++) {
        setServoAngle(i, 90);
    }

    Serial.println("READY");  // Signal to Pi that Arduino is initialized
}

// ---------------------------------------------------------------------------
// Main Loop
// ---------------------------------------------------------------------------

void loop() {
    // Read and parse serial commands
    readSerial();

    // Smoothly move servos toward target angles
    updateServos();

    // Small delay to control update rate (~50 Hz servo updates)
    delay(20);
}

// ---------------------------------------------------------------------------
// Serial Parsing
// ---------------------------------------------------------------------------

void readSerial() {
    while (Serial.available() > 0) {
        char c = Serial.read();

        if (c == '<') {
            // Start of message
            receiving = true;
            msgIndex = 0;
        } else if (c == '>') {
            // End of message — parse it
            if (receiving) {
                msgBuffer[msgIndex] = '\0';
                parseCommand(msgBuffer);
                receiving = false;
            }
        } else if (receiving) {
            // Accumulate message characters
            if (msgIndex < MSG_BUF_SIZE - 1) {
                msgBuffer[msgIndex++] = c;
            } else {
                // Buffer overflow — discard message
                receiving = false;
                msgIndex = 0;
            }
        }
    }
}

void parseCommand(const char* cmd) {
    // Parse format: S0:90,S1:45,S2:180,...
    // Tokenize by comma
    char buf[MSG_BUF_SIZE];
    strncpy(buf, cmd, MSG_BUF_SIZE - 1);
    buf[MSG_BUF_SIZE - 1] = '\0';

    char* token = strtok(buf, ",");
    while (token != NULL) {
        // Each token is "S#:value"
        if (token[0] == 'S') {
            int channel = -1;
            int angle = -1;

            // Parse channel number and angle value
            if (sscanf(token, "S%d:%d", &channel, &angle) == 2) {
                if (channel >= 0 && channel < NUM_SERVOS && angle >= 0 && angle <= 180) {
                    targetAngle[channel] = angle;
                }
            }
        }
        token = strtok(NULL, ",");
    }
}

// ---------------------------------------------------------------------------
// Servo Control
// ---------------------------------------------------------------------------

void setServoAngle(int channel, int angle) {
    if (channel < 0 || channel >= NUM_SERVOS) return;
    angle = constrain(angle, 0, 180);

    // Map angle (0-180) to pulse ticks using per-servo calibration
    uint16_t pulse = map(angle, 0, 180, servoMin[channel], servoMax[channel]);
    pwm.setPWM(channel, 0, pulse);
    currentAngle[channel] = angle;
}

void updateServos() {
    // Smoothly move each servo toward its target angle
    for (int i = 0; i < NUM_SERVOS; i++) {
        if (currentAngle[i] != targetAngle[i]) {
            int diff = targetAngle[i] - currentAngle[i];

            // Limit step size for smooth motion
            if (abs(diff) > MAX_STEP) {
                diff = (diff > 0) ? MAX_STEP : -MAX_STEP;
            }

            setServoAngle(i, currentAngle[i] + diff);
        }
    }
}
