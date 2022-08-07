#define THRESHOLD 100

int trig1=23,echo1=22;
int trig2=25,echo2=24;
int trig3=27,echo3=26;
int trig4=29,echo4=28;
int trig5=31,echo5=30;
int trig6=33,echo6=32;
int trig7=35,echo7=34;

int motr1=2,motr2=3,motr3=4,motr4=5,motr5=6,motr6=7,motr7=8;

int amp1,amp2,amp3,amp4;

void getAmplitude(){
  int amp=0;
    digitalWrite(trig1,0);
    delayMicroseconds(2);
digitalWrite(trig1,1);
    delayMicroseconds(10);
    digitalWrite(trig1,0);

    digitalWrite(trig2,0);
    delayMicroseconds(2);
    digitalWrite(trig2,1);
    delayMicroseconds(10);
    digitalWrite(trig2,0);


        digitalWrite(trig3,0);
    delayMicroseconds(2);
digitalWrite(trig3,1);
    delayMicroseconds(10);
    digitalWrite(trig3,0);


    digitalWrite(trig4,0);
    delayMicroseconds(2);
digitalWrite(trig4,1);
    delayMicroseconds(10);
    digitalWrite(trig4,0);

        digitalWrite(trig5,0);
    delayMicroseconds(2);
digitalWrite(trig5,1);
    delayMicroseconds(10);
    digitalWrite(trig5,0);

        digitalWrite(trig6,0);
    delayMicroseconds(2);
digitalWrite(trig6,1);
    delayMicroseconds(10);
    digitalWrite(trig6,0);

        digitalWrite(trig7,0);
    delayMicroseconds(2);
digitalWrite(trig7,1);
    delayMicroseconds(10);
    digitalWrite(trig7,0);

  int duration1=pulseIn(echo1,1);
  int duration2=pulseIn(echo2,1);
  int duration3=pulseIn(echo3,1);
  int duration4=pulseIn(echo4,1);

  int distance1=duration1*0.034/2;
  int distance2=duration2*0.034/2;
  int distance3=duration3*0.034/2;
  int distance4=duration4*0.034/2;

  Serial.println("Distance 1: " + distance1);
  Serial.println("Distance 2: " + distance2);
  Serial.println("Distance 3: " + distance3);
  Serial.println("Distance 4: " + distance4);

  if(distance1<THRESHOLD){
    int d1=THRESHOLD-distance1;
    amp1=d1*254/100;
  }

  else{
    amp1=0;
  }


  if(distance2<THRESHOLD){
    int d2=THRESHOLD-distance2;
    amp2=d2*254/100;
  }

  else{
    amp2=0;
  }


  if(distance3<THRESHOLD){
    int d3=THRESHOLD-distance3;
    amp3=d3*254/100;
  }

  else{
    amp3=0;
  }


  if(distance4<THRESHOLD){
    int d4=THRESHOLD-distance4;
    amp4=d4*254/100;
  }

  else{
    amp4=0;
  }
}


void setup() {
  pinMode(trig1,OUTPUT);
  pinMode(echo1,INPUT);
  pinMode(trig2,OUTPUT);
  pinMode(echo2,INPUT);
  pinMode(trig3,OUTPUT);
  pinMode(echo3,INPUT);
  pinMode(trig4,OUTPUT);
  pinMode(echo4,INPUT);


  pinMode(motr1,OUTPUT);
  pinMode(motr2,OUTPUT);
  pinMode(motr3,OUTPUT);
  pinMode(motr4,OUTPUT);


  Serial.begin(9600);
}

void loop() {

  getAmplitude();


  analogWrite(motr1,amp1);
  analogWrite(motr2,amp2);
  analogWrite(motr3,amp3);
  analogWrite(motr4,amp4);
  analogWrite(motr5,amp5);
  analogWrite(motr6,amp6);
  analogWrite(motr7,amp7);


}
