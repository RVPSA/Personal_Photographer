#if defined(ESP32)
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Servo.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#endif

//Provide the token generation process info.
#include <addons/TokenHelper.h>

//Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

/* 1. Define the WiFi credentials */
#define WIFI_SSID "HUAWEI nova Y70"
#define WIFI_PASSWORD "abcd1234"

//For the following credentials, see examples/Authentications/SignInAsUser/EmailPassword/EmailPassword.ino

/* 2. Define the API Key */
#define API_KEY "hOTV7ONnZ5nIGrnaq7MY9xE2xDkRoJ7wv7YYJruR"

/* 3. Define the RTDB URL */
#define DATABASE_URL "https://personalrobotcoordinate-default-rtdb.firebaseio.com/" //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app

#define LED 2
//Define Firebase Data object
FirebaseData fbdo;

Servo myservo;

FirebaseAuth auth;
FirebaseConfig config;


//String main="";


int  centerX, centerY;

void setup()
{

  Serial.begin(115200);
delay(2000);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;


  Firebase.begin(DATABASE_URL, API_KEY);
  myservo.attach(13);

  //Comment or pass false value when WiFi reconnection will control by your code or third party library
 // Firebase.reconnectWiFi(true);

  Firebase.setDoubleDigits(5);
  
  pinMode(LED,OUTPUT);

}

void loop()
{
 
  if (Firebase.ready()) 
  {
    Firebase.getInt(fbdo, "/centerX/a") ? String(fbdo.to<int>()).c_str() : fbdo.errorReason().c_str();
     centerX=fbdo.to<int>();
    //Firebase.getInt(fbdo, "/centerY") ? String(fbdo.to<int>()).c_str() : fbdo.errorReason().c_str();
     //centerY=fbdo.to<int>();

  if (centerX<=0) {
      myservo.write(0);
      digitalWrite(LED,HIGH);
      delay(25);
    } 
    else if (centerX>0 && centerX<180){
      myservo.write(centerX);
    } 
    else{
      myservo.write(180);
      digitalWrite(LED,HIGH);
      delay(50);
      }  

  Serial.println();
  Serial.print("centerX: ");
  Serial.print(centerX);
  Serial.println();
  //Serial.print("centerY: ");
  //Serial.print(centerY);
  //Serial.println();
  
  Serial.println();
  Serial.println("------------------");
  Serial.println();
  

  //delay(2000);
  }
}
