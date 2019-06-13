import ddf.minim.*;
//ライブラリをインポート
import themidibus.*; //Import the library
PrintWriter output;

//MidiBusクラスの変数「myBus」を作成。複数MIDIコンを使いたい場合には、myBus1,myBus2等、複数作れば良い…はず。
MidiBus myBus; // The MidiBus
int[][] ActiveStringTime = new int[7][40];
int[][] ActiveFret = new int[7][40];
int[][] ActivePitch = new int[7][40];

Minim minim;
AudioInput in;
AudioPlayer[] player;
AudioRecorder[] recorder;
AudioRecorder[] phraserecorder;
AudioMetaData[] meta;

float [] zikan;
int flag =0;
int phraseFlag=0;
float start;
int phraseStart=0;
int tempo=110;
void setup() {
  size(1500, 1000);
  minim = new Minim(this);
  in = minim.getLineIn(Minim.STEREO, 512);
  recorder = new AudioRecorder[64];
  phraserecorder = new AudioRecorder[64];
  meta = new AudioMetaData[64];
  zikan = new float[64];
  for (int i=0; i<64; i++) {
    recorder[i] = minim.createRecorder(in, "myrecording"+(i+1)+".wav", true);
    phraserecorder[i] = minim.createRecorder(in, "phraserecording"+(i+1)+".wav", true);
  }
  player = new AudioPlayer[8];
  for (int i=0; i<8; i++) {
    player[i] = minim.loadFile((i+1)+".mp3");
    meta[i] = player[i].getMetaData();
    zikan[i] = meta[i].length();
  }
  textFont(createFont("Arial", 12));
  String filename = nf(year(), 4) + nf(month(), 2) + nf(day(), 2) + nf(hour(), 2) + nf(minute(), 2) ;
  output = createWriter(filename + ".csv");
  //つながっているMIDI関係機器を表示。このリストの番号で、後ほどのIn Outの設定をする。
  MidiBus.list();
  myBus = new MidiBus(this, 0, 2); // Create a new MidiBus with no input device and the default Java Sound Synthesizer as the output device.

}

void draw() {
  background(0);
  if ( recorder[flag].isRecording()&& player[flag].isPlaying()==false ) {
    recorder[flag].endRecord();
    recorder[flag].save();
    if (flag==7) {
      flag=0;
    } else {
      flag++;
    }
  } else {
    recorder[flag].beginRecord();
    player[flag].play();
    start=millis();
  }
}

void keyReleased() {
  if ( key == 'r' ) {
  }
}

void stop() {
  for (int i=0; i<8; i++ ) {
    player[i].close();
  }
  in.close(); 
  minim.stop(); 
  super.stop();
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
  int string=channel+1;
  int fret=0;
  if (string==6) {
    fret=pitch-40;
  } else if (string==5) {
    fret=pitch-45;
  } else if (string==4) {
    fret=pitch-50;
  } else if (string==3) {
    fret=pitch-55;
  } else if (string==2) {
    fret=pitch-59;
  } else if (string==1) {
    fret=pitch-64;
  }
  if (fret>0&&fret<25&&string>0&&string<7) {
    ActiveStringTime[string][fret]=millis();
    ActiveFret[string][fret]=fret;
    ActivePitch[string][fret]=pitch;
  }
}

//ノートオフが来たときに起きる関数
void noteOff(int channel, int pitch, int velocity) {
  int string=channel+1;
  int fret=0;
  if (string==6) {
    fret=pitch-40;
  } else if (string==5) {
    fret=pitch-45;
  } else if (string==4) {
    fret=pitch-50;
  } else if (string==3) {
    fret=pitch-55;
  } else if (string==2) {
    fret=pitch-59;
  } else if (string==1) {
    fret=pitch-64;
  }
  if (fret>0&&fret<25&&string>0&&string<7) {
    int PhoneticValue=millis()-ActiveStringTime[string][fret];
    output.println(ActiveStringTime[string][fret]+","+PhoneticValue+","+string+","+ActiveFret[string][fret]+","+ActivePitch[string][fret]);
    rect(ActiveStringTime[string][fret]/100, ActivePitch[string][fret]*10, PhoneticValue/100, 20);
  }
  // Receive a noteOff
  println();
  println("Note Off:");
  println("--------");
  println("Channel:"+channel);
  println("Pitch:"+pitch);
  println("Velocity:"+velocity);
}

//コントロールチェンジが来たときに起きる関数
void controllerChange(int channel, int number, int value) {
  // Receive a controllerChange
  println();
  println("Controller Change:");
  println("--------");
  println("Channel:"+channel);
  println("Number:"+number);
  println("Value:"+value);
}

void delay(int time) {
  int current = millis();
  while (millis () < current+time) Thread.yield();
}

void dispose() {
  output.flush();
  output.close();
  exit();
}