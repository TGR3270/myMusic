int flag=0;//画面遷移
int port = 10001; // 適当なポート番号を設定
String [] suisen;
String [] suisen_mod;
PImage[] img;
Table a;
String [] a_mod;
import ddf.minim.*;
Minim minim;
AudioSample[] player;
int nagasa;
Boolean Saisei = true;
Boolean start = false;
void setup() {
  background(255);
  size(2500, 1400);
  img = new PImage[500];
  minim = new Minim(this);
  player = new AudioSample[500];
  PFont font = createFont("Yu Gothic", 48, true);
  textFont(font);
  textSize(60);
  //csv read
  a = loadTable("suisen.csv");
  nagasa = a.getColumnCount();
  a_mod = new String[nagasa];
  for (int i =0; i<nagasa; i++) {
    a_mod[i] = splitTokens(a.getString(0, i), ".")[0];
    if (loadImage(a_mod[i]+".PNG")!=null&&minim.loadSample(a_mod[i]+".wav")!=null) {
      img[i] = loadImage(a_mod[i]+".PNG");
      player[i] = minim.loadSample(a_mod[i]+".wav");
    }
  }
}

void draw() {
  background(255);
  if (flag<nagasa&&start) {
    if (loadImage(a_mod[flag]+".PNG")!=null) {
      image(img[flag], width/2-img[flag].width/2-200, height/3-img[flag].height/2, img[flag].width*1.3, img[flag].height*1.3);
    }
    if (Saisei) {
      if (minim.loadSample(a_mod[flag]+".wav")!=null) {
        player[flag].trigger();
      }
      Saisei = false;
    }
    textSize(70);
    fill(0);
    text("EX-"+(flag+1), 150, 200);
    textSize(55);
    //text("Enterキーを押すと楽譜が表示され", width/7-100, height-height/5);
    //text("演奏したときの音源が再生されます", width/7-100, height-height/5+100);
    text("↓キーで次のフレーズへ", width/2-400, height-height/5);
    text("スペースキーで音源を再度再生", width/2-400, height-height/5+100);
    text("↑キーで前のフレーズへ", width/2-400, height-height/5+200);
    //line(width/2, height-height/5-50, width/2, height-35);
  } else {
    flag=0;
    start = false;
    textSize(80);
    fill(0);
    text("Enterキーを押すと楽譜が表示され", width/4, height/4);
    text("演奏したときの音源が再生されます", width/4, height/4+100);
    text("↑キーで前のフレーズへ", width/4, height/4+300);
    text("スペースキーで音源を再度再生", width/4, height/4+400);
    text("↓キーで次のフレーズへ", width/4, height/4+500);
  }
}
void keyPressed() {
  if (keyCode == ENTER) {
    start = true;
  }
  if (keyCode == 40&&start) {
    if (flag<nagasa-1) {
      flag++;
      Saisei = true;
    }
  }
  if (keyCode == 32&&start) {
    Saisei = true;
  }
  if (keyCode == 38&&start) {
    Saisei = true;
    if (flag>1) {
      flag--;
    } else {
      start = false;
    }
  }
}
void stop() {
  for (int i=0; i<nagasa; i++) {
    player[i].close();
  }
  minim.stop();
  super.stop();
}