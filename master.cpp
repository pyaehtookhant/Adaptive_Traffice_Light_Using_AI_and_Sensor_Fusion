//master code for traffic light system 
#include <Arduino.h>
#include <time.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <stdio.h>
#include <stdlib.h>
//Setting up host and token
#include<FirebaseESP8266.h>

#define FIREBASE_HOST "https://traffic-db-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH "fbR9h4vBmzjn36KNONMHEZQkrqaRBtPqzCau8Gja"

#define R1L "/Road1/left_lane/"
#define R1R "/Road1/right_lane/"
#define R2L "/Road2/left_lane/"
#define R2R "/Road2/right_lane/"

String path[4] = { R1L, R1R, R2L, R2R };

FirebaseData fb;

#define trigPin1 3 //trig pin of 1st sensor
#define echoPin1 4 //
#define trigPin2 5 //trigpin of 2nd sensor
#define echoPin2 6 //
#define trigPin3 7 //trigpin for 3rd sensor
#define echoPin3 8 //
#define trigPin4 9 //trigger pin for 4th sensor
#define echoPin4 10 //



//variables for ultrasonic sensor
long duration1, distance1; //duration and distance for 1st sensor
long duration2, distance2; //duration and distance for 2nd sensor
long duration3, distance3; //duration and distance for 3rd sensor
long duration4, distance4; //duration and distance for 4th sensor

//variables for traffic light
int red = 0; //red led
int green = 0; //green led
int blue = 0; //blue led

//variables for traffic light 2
int red1 = 0; //red led
int green1 = 0; //green led
int blue1 = 0; //blue led

//array for combinded all ultrasonic sensors
long arr[4] = {0, 0, 0, 0};

//GP var
int i = 0; //for loop
int sensoramount = 4; //amount of sensors

//wifi
const char* ssid = "SSID"; //wifi name
const char* password = "PASSWORD"; //wifi password



int fb_get_Int(String PATH){
  if(Firebase.getInt(fb, PATH)){
    if(fb.dataType() == "int"){
      int val = fb.intData();
      Serial.print("value of " + fb.dataPath() + " ");
      Serial.println(val);
      return val;
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fb.errorReason());
    }
  }
  return -1;
}

void fb_set_Int(String PATH, int data){
    if (Firebase.setInt(fb, PATH, data)){
      Serial.println("Successfully to set " + fb.dataPath());
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fb.errorReason());
    }
}


//function for all ultrasonic sensors
void setup(){
  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT); //trig pin of 1st sensor
  pinMode(echoPin1, INPUT); //
  pinMode(trigPin2, OUTPUT); //trigpin of 2nd sensor
  pinMode(echoPin2, INPUT); //
  pinMode(trigPin3, OUTPUT); //trigpin for 3rd sensor
  pinMode(echoPin3, INPUT); //
  pinMode(trigPin4, OUTPUT); //trigger pin for 4th sensor
  pinMode(echoPin4, INPUT); //


  //wifi
  WiFi.begin("SSID", "PASSWORD"); //wifi name and password
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  // Print the IP address
   // Setting up wifi . . .
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

}

void loop(){
  
  //first sensor
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  duration1 = pulseIn(echoPin1, HIGH);
  distance1 = duration1*0.034/2; //distance calculation by duration of the pulse and speed of sound divided by 2
  Serial.print("Distance1: ");
  Serial.println(distance1);

  //second sensor
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  duration2 = pulseIn(echoPin2, HIGH);
  distance2 = duration2*0.034/2;
  Serial.print("Distance2: ");
  Serial.println(distance2);

  //third sensor
  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);
  duration3 = pulseIn(echoPin3, HIGH);
  distance3 = duration3*0.034/2;
  Serial.print("Distance3: ");
  Serial.println(distance3);

  //fourth sensor
  digitalWrite(trigPin4, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin4, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin4, LOW);
  duration4 = pulseIn(echoPin4, HIGH);
  distance4 = duration4*0.034/2;
  Serial.print("Distance4: ");
  Serial.println(distance4);

  //array for combinded all ultrasonic sensors
  arr[0] = distance1;
  arr[1] = distance2;
  arr[2] = distance3;
  arr[3] = distance4;

  Serial.printf("arr[0] = %d\n", arr[0]); //front ultrasonic sensor in lane 1
  Serial.printf("arr[1] = %d\n", arr[1]); //rear ultrasonic sensor in lane 1
  Serial.printf("arr[2] = %d\n", arr[2]); //front ultrasonic sensor in lane 2
  Serial.printf("arr[3] = %d\n", arr[3]); //rear ultrasonic sensor in lane 2

  

  //arr0-1 is lane 1 and arr2-3 is lane 2
  //check for occupancy based on distance

  //lane 1
  switch(arr[0].distance1){
    case 0(distance1 < 10): //if distance is less than 10cm
      fb_set_Int("lane1", 1) //set lane 1 to true
    case 1(distance1 > 10 && distance1 < 20): //if distance is between 10cm and 20cm
      fb_set_Int("lane1", 1) //set lane 1 to false
    case 2(distance1 >20);
      fb_set_Int("lane1", 0);
  }

  switch(arr[1].distance2){
    case 0(distance2 < 10): //if distance is less than 10cm
      fb_set_Int("lane1", 3); //set lane 1 to true
    case 1(distance2 > 10 && distance2 < 20): //if distance is between 10cm and 20cm
      fb_set_Int("lane1", 2); //set lane 1 to false
    case 2(distance2 >20);
      fb_set_Int("lane1", 0);
  }

  switch(arr[2].distance2){
    case 0(distance3 < 10): //if distance is less than 10cm
      fb_set_Int("lane2", 1); //set lane 2 to true
    case 1(distance3 > 10 && distance3 < 20): //if distance is between 10cm and 20cm
      fb_set_Int("lane2", 0); //set lane 2 to false
    case 2(distance3 >20);
      fb_set_Int("lane2", 0);
  }

  switch(arr[3].distance2){
    case 0(distance4 < 10): //if distance is less than 10cm
      fb_set_Int("lane2", 3); //set lane 2 to true
    case 1(distance4 > 10 && distance4 < 20): //if distance is between 10cm and 20cm
      fb_set_Int("lane2", 2); //set lane 2 to false
    case 2(distance4 >20);
      fb_set_Int("lane2", 0);
  }
  
}


