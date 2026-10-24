#include <Servo.h>

Servo servoX;
Servo servoY;

const int trigPin = 9;
const int echoPin = 10;
const int grid_size = 10;

void setup()
{
    Serial.begin(9600);
    servoX.attach(5);
    servoY.attach(6);

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

void loop()
{
    Serial.println("=== ½ºÄµ ½ÃÀÛ ===");

    for (int y = 0; y < grid_size; y++)
    {
        for (int x = 0; x < grid_size; x++)
        {
            servoX.write(map(x, 0, grid_size-1, 60, 120));
            servoY.write(map(y, 0, grid_size-1, 60, 120));
            delay(500);

            digitalWrite(trigPin, LOW);
            delayMicroseconds(2);
            digitalWrite(trigPin, HIGH);
            delayMicroseconds(10);
            digitalWrite(trigPin, LOW);
            
            long duration = pulseIn(echoPin, HIGH);
            float distance = duration * 0.034 / 2;
            
            Serial.print(x); Serial.print(",");
            Serial.print(y); Serial.print(",");
            Serial.println(distance);
        }
    }

    Serial.println("=== ½ºÄµ Á¾·á ===");
    while(1);
}