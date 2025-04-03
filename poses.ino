#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#define ledGreenPin 6
#define ledRedPin 9
#define ledY1Pin 8
#define ledY2Pin 7

LiquidCrystal_I2C lcd(0x27, 16, 2); 
int series = 0;
int repeticoes = 0;
void setup() {
  Serial.begin(9600);
  pinMode(ledGreenPin, OUTPUT);
  pinMode(ledRedPin, OUTPUT);
  lcd.init(); // Inicia o LCD
  lcd.backlight(); // Liga a luz de fundo
  lcd.setCursor(0, 0);
  lcd.print("Hello, Arduino!");
  lcd.setCursor(0, 1);
  lcd.print("LCD I2C Teste");
  delay(3000);
  lcd.clear();
}

void loop() {
  
  if(Serial.available() > 0){
    char command = Serial.read();
      lcd.setCursor(0, 1); // Linha 2
      lcd.print("Qtd series: ");
      lcd.print(series);

    

    if (command == 'R'){
      series = 1;
      repeticoes = 0;
      digitalWrite(ledRedPin, HIGH);
      digitalWrite(ledGreenPin, LOW);
      digitalWrite(ledY1Pin, LOW);
      digitalWrite(ledY2Pin, LOW);
      lcd.setCursor(0, 1); // Linha 2
      lcd.print("Qtd series: ");
      lcd.print(series);

    
    } else if(command == 'Y'){
      series = 2;
      repeticoes = 0;
      digitalWrite(ledGreenPin, LOW);
      digitalWrite(ledRedPin, LOW);
      digitalWrite(ledY1Pin, HIGH);
      digitalWrite(ledY2Pin, LOW);
      lcd.setCursor(0, 1); // Linha 2
      lcd.print("Qtd series: ");
      lcd.print(series);
    } else if (command == 'S'){
      series = 3;
      repeticoes = 0;
      digitalWrite(ledGreenPin, LOW);
      digitalWrite(ledRedPin, LOW);
      digitalWrite(ledY1Pin, LOW);
      digitalWrite(ledY2Pin, HIGH);
      lcd.setCursor(0, 1); // Linha 2
      lcd.print("Qtd series: ");
      lcd.print(series);
    } else if(command == 'G'){
      series = 4;
      repeticoes = 0;
      digitalWrite(ledGreenPin, HIGH);
      digitalWrite(ledRedPin, LOW);
      digitalWrite(ledY1Pin, LOW);
      digitalWrite(ledY2Pin, LOW);
      lcd.setCursor(0, 1); // Linha 2
      lcd.print("Qtd series: ");
      lcd.print(series);
    }


    if (command == 'U'){
      repeticoes += 1;
      lcd.setCursor(0, 0); // Linha 1
      lcd.print("Repeticoes: ");
      lcd.print(repeticoes);
    }
  }

}
