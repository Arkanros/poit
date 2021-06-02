#include <PID_v1.h>
double Input, Output;
double P = 1, I = 1, D = 1;
double  Napatie = 500;
double voltage;
char receivedChar;
boolean newData = false;

String A[10];
int count = 0;
String temp;

PID myPID(&Input, &Output, &Napatie, P, I, D, DIRECT);
void setup() {
  Serial.begin(9600);
  Input = analogRead(A3);
  Serial.println("Arduino je pripravene");


  //Adjust PID values
  myPID.SetTunings(P, I, D);
  myPID.Compute();

}

void loop() {
   Input = analogRead(A3);
  recvOneChar();

 // showNewData();


}

void recvOneChar() {

  if (Serial.available()>0) {
    receivedChar = Serial.read(); 
    A[count] = receivedChar;
   // newData = true;
    count++;
    if(A[count-1] == "x"){
      count = 0;
    pridaj();}



  }
}

void showNewData() {
  if (newData == true) {
   // Serial.print("This just in ... ");
    //Serial.println(receivedChar);
    newData = false;
  }
}

void pridaj() {
  // String Pi = A[0];
 // Serial.print("VOLAM FUNKCIU...");
  P = A[0].toDouble();
  I = A[1].toDouble();
  D = A[2].toDouble();


  if(A[6] == "x"){
  temp = A[3] + A[4] + A[5];
  Napatie = temp.toDouble();


  }else if(A[7] == "x"){
  temp = A[3] + A[4] + A[5] + A[6];
  Napatie = temp.toDouble();


  }
  Napatie = (Napatie/1023)*5;
 
  myPID.SetTunings(P, I, D);
  myPID.Compute();

//  Serial.print("p..");
//  Serial.println(P);
//  Serial.print("i..");
//  Serial.println(I);
//  Serial.print("d..");
//  Serial.println(D);
//  Serial.print("count..");
//  Serial.println(count);
//  Serial.print("napatie..");
//  Serial.println(Napatie);
voltage=analogRead(A3);
Serial.println("Napatie..");
 Serial.println(voltage/1023);

 Serial.println("Napatie na vstupe..");
 Serial.println(Napatie);
 // newData = false;
 

  for (int x = 0; x < sizeof(A) / sizeof(A[0]); x++)
{
  A[x] = "";
}


}
