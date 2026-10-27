#include <Servo.h>

Servo servoX;
Servo servoY;

const int trigPin = 9;
const int echoPin = 10;
const int grid_size = 10;

const float baseline[10][10] = {
  { 3.79, 3.84, 3.88, 3.91, 4.23, 4.33, 4.30, 4.63, 4.64, 4.95 },
  { 3.84, 3.89, 3.89, 3.96, 4.37, 4.37, 4.77, 4.74, 5.09, 5.41 },
  { 3.83, 3.88, 3.90, 3.95, 4.41, 4.36, 4.82, 5.19, 5.54, 5.85 },
  { 3.91, 3.96, 4.00, 4.03, 4.47, 4.47, 4.86, 4.83, 5.19, 5.91 },
  { 3.92, 3.97, 4.01, 4.05, 4.48, 4.47, 4.87, 4.85, 5.20, 5.51 },
  { 3.53, 3.57, 4.01, 4.05, 4.47, 4.49, 4.45, 4.85, 5.21, 5.52 },
  { 3.52, 3.56, 3.60, 4.03, 4.05, 4.05, 4.45, 4.41, 4.79, 5.41 },
  { 3.50, 3.54, 3.57, 4.01, 4.02, 4.02, 4.43, 4.80, 4.76, 5.48 },
  { 3.85, 3.90, 3.94, 3.97, 4.40, 4.40, 4.37, 4.76, 5.11, 5.79 },
  { 3.85, 3.90, 3.94, 3.98, 4.38, 4.38, 4.78, 4.75, 5.09, 5.74 }
};

void setup() {
  Serial.begin(9600);
  servoX.attach(5);
  servoY.attach(6);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

float getFilteredDistance() {
  float readings[5];

  for (int i = 0; i < 5; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH, 30000);
    float dist = duration * 0.034 / 2.0;

    if (dist > 400) dist = 400.0;

    readings[i] = dist;
    delay(10);
  }

  for (int i = 0; i < 4; i++)
    for (int j = i + 1; j < 5; j++)
      if (readings[i] > readings[j]) {
        float temp = readings[i];

        readings[i] = readings[j];
        readings[j] = temp;
      }

  return readings[2];
}

void loop() {
  Serial.println("=== Scan Start ===");

  for (int y = 0; y < grid_size; y++) {
    for (int x = 0; x < grid_size; x++) {
      int angleX = map(x, 0, grid_size - 1, 75, 105);
      int angleY = map(y, 0, grid_size - 1, 75, 105);

      servoX.write(angleX);
      servoY.write(angleY);
      delay(1500);

      float raw_distance = getFilteredDistance();

      if (raw_distance > 200.0) raw_distance = 200.0;

      float radX = abs(angleX - 90) * PI / 180.0;
      float radY = abs(angleY - 90) * PI / 180.0;
      float z_distance = raw_distance * cos(radX) * cos(radY);

      float calibrated_z = z_distance - (baseline[y][x] - 4.00);

      Serial.print(x);
      Serial.print(",");
      Serial.print(y);
      Serial.print(",");
      Serial.println(calibrated_z);
    }
  }

  Serial.println("=== Scan End ===");
  while (1);
}