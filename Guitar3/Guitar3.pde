import themidibus.*; //Import the library
PrintWriter output;
//MidiBusクラスの変数「myBus」を作成。複数MIDIコンを使いたい場合には、myBus1,myBus2等、複数作れば良い…はず。
MidiBus myBus; // The MidiBus
boolean noteOns=false;
int gen;
int fret;
int beginTime;
int noteTime;
int count=0;
int [][] otoCount=new int[6][25];
int [][] otoLong=new int[6][25];
int [] pitchCount=new int[200];
void setup() {
  for (int i=0; i<6; i++) {
    for (int t=0; t<25; t++) {
      otoCount[i][t]=0;
      otoLong[i][t]=0;
    }
  }
  
  output= createWriter("playg.csv");
  size(1850,1000);
  background(0);
  frameRate(60);
  //つながっているMIDI関係機器を表示。このリストの番号で、後ほどのIn Outの設定をする。
  MidiBus.list(); // List all available Midi devices on STDOUT. This will show each device's index and name.

  //
  // Either you can
  //                   Parent In Out
  //                     |    |  |
  //myBus = new MidiBus(this, 0, 1); // Create a new MidiBus using the device index to select the Midi input and output devices respectively.

  // or you can ...
  //                   Parent         In                   Out
  //                     |            |                     |
  //myBus = new MidiBus(this, "IncomingDeviceName", "OutgoingDeviceName"); // Create a new MidiBus using the device names to select the Midi input and output devices respectively.

  //先ほど表示したリストから番号か、もしくは名前で指定。毎回同じ機材を使うのであれば名前で指定したほうがいいのか？
  //In Outのうち使わないところには-1を指定すれば良い模様。

  // or for testing you could ...
  //                 Parent  In        Out
  //                   |     |          |
  myBus = new MidiBus(this, "i2M musicport", "i2M musicport"); // Create a new MidiBus with no input device and the default Java Sound Synthesizer as the output device.
}

void draw() {
  background(200);
  //ノートを送る。
  //myBus.sendNoteOn(channel, pitch, velocity); // Send a Midi noteOn
  //delay(200);
  //myBus.sendNoteOff(channel, pitch, velocity); // Send a Midi nodeOff

  //int number = 0;
  //int value = 90;

  //コントロールチェンジを送る
  // myBus.sendControllerChange(channel, number, value); // Send a controllerChange
  fill(255);
  textSize(20);
  //text(gen+"   "+fret, 100, 100);
  c();
  for (int i=0; i<6; i++) {
    for (int t=0; t<25; t++) {
      //println(i+1+" "+t+1+" "+otoCount[i][t]);
      //println(i+1+" "+t+1+" "+otoLong[i][t]);
      if (otoCount[i][t]>60) {
        text(i+1+" "+(t+1), i*30, t*20);
      }
      fill(0);
      text(t,83+t*70,80);
      noStroke();
      fill(otoCount[i][t]*2,255-otoCount[i][t]*2,0);
      rect(65+t*70,100+i*50,70,50);
      stroke(0);
      line(100+t*70,100,100+t*70,400);
      line(100,125+i*50,100+25*70,125+i*50);
    }
  }
  delay(10);
}
void c() {
  if (noteOns==true) {
    if (gen>0&&gen<=6&&fret>0&&fret<=24) {
      otoCount[gen-1][fret-1]=otoCount[gen-1][fret-1]+1;
      otoLong[gen-1][fret-1]=otoLong[gen-1][fret-1]+noteTime;
    }
  }
}
//ノートオンが来たときに起きる関数
void noteOn(int channel, int pitch, int velocity) {
  // Receive a noteOn
  println();
   println("Note On:");
   println("--------");
   println("Channel:"+channel);
   println("Pitch:"+pitch);
   println("Velocity:"+velocity);
  if (noteOns==true) {
    count=count+1;
    noteTime=millis()-beginTime;
    //println(count+","+pitch+","+gen+","+fret+","+noteTime);
    if(noteTime>0){
    output.println(count+","+pitch+","+gen+","+fret+","+noteTime);
    output.flush();
    }
    noteOns=false;
    //otoCount[gen-1][fret-1]=otoCount[gen-1][fret-1]+1;
    //otoLong[gen-1][fret-1]=otoLong[gen-1][fret-1]+noteTime;
  }
  if (noteOns==false) {
    gen=channel+1;
    if (gen==6) {
      fret=pitch-40;
    } else if (gen==5) {
      fret=pitch-45;
    } else if (gen==4) {
      fret=pitch-50;
    } else if (gen==3) {
      fret=pitch-55;
    } else if (gen==2) {
      fret=pitch-59;
    } else if (gen==1) {
      fret=pitch-64;
    }
    noteOns=true;
    beginTime=millis();
  }
}

//ノートオフが来たときに起きる関数
void noteOff(int channel, int pitch, int velocity) {
  // Receive a noteOff
  /*println();
   println("Note Off:");
   println("--------");
   println("Channel:"+channel);
   println("Pitch:"+pitch);
   println("Velocity:"+velocity);
   */
}

//コントロールチェンジが来たときに起きる関数
void controllerChange(int channel, int number, int value) {
  // Receive a controllerChange
  /*println();
   println("Controller Change:");
   println("--------");
   println("Channel:"+channel);
   println("Number:"+number);
   println("Value:"+value);*/
}

void delay(int time) {
  int current = millis();
  while (millis () < current+time) Thread.yield();
}

void dispose() {


  output.close();
}