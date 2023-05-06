#include <dht11.h>
#define DHT11PIN 4
const int IN_A0 = A1; // analog input
const int IN_D0 = 5; // digital input

dht11 DHT11;

void  setup()
{
  Serial.begin(9600);
  pinMode (IN_A0, INPUT);
  pinMode (IN_D0, INPUT);
}

void loop()
{
  int chk = DHT11.read(DHT11PIN);

  int value_A0 = analogRead(IN_A0); // reads the analog input from the IR distance sensor
  bool value_D0 = digitalRead(IN_D0);// reads the digital input from the IR distance sensor
  
  Serial.print(value_A0);
  Serial.print(",");
  Serial.print(value_D0);
  Serial.print(",");
  Serial.print((float)DHT11.humidity, 2);
  Serial.print(",");
  Serial.print((float)DHT11.temperature, 2);
  Serial.println();

  delay(2000);
}