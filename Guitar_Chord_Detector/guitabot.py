from tensorflow.keras.models import load_model
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

class Servo:
    def _init_(self,p):
        self.set = GPIO.setup(p,GPIO.OUT)
        self.pin = GPIO.PWM(p,50)
        self.pin.start(0)
        #self.grados_duty(0)
        
    def grados_duty(self, grados):
        self.pin.ChangeDutyCycle(2+(grados/19))
        time.sleep(0.25)
        self.pin.ChangeDutyCycle(2+(grados/19))
        time.sleep(0.25)
        self.pin.ChangeDutyCycle(0)
            
    
    def apagar(self):
        self.pin.stop()
        GPIO.cleanup()



def trastes_a_mm(traste,servo):
    pct = traste/134
    grado = int(((servo[1]-servo[0])*pct)+servo[0])
    return grado


def mover(x):
    global p
    global grados
    global acorde
    global carga
    print("Moviendo a " + acorde)
    for i in range(6):
        p[i].grados_duty(grados[i])
    time.sleep(.1)
    
    
    
btn_pin = 19

trastes = {'0': 0,
           '1': 50,
           '2': 65,
           '3': 93,
           '4': 124}


servos = {'1':[5,185],
          '2':[0,185],
          '3':[180,0],
          '4':[190,2],
          '5':[180,15],
          '6':[0,180]}


chords ={
        'Am':{'1':trastes['0'],
              '2':trastes['4'],
              '3':trastes['3'],
              '4':trastes['2'],
              '5':trastes['0'],
              '6':trastes['0']},

        'B':{ '1':trastes['3'],
              '2':trastes['1'],
              '3':trastes['1'],
              '4':trastes['4'],
              '5':trastes['2'],
              '6':trastes['0']},

        'C':{ '1':trastes['0'],
              '2':trastes['4'],
              '3':trastes['0'],
              '4':trastes['2'],
              '5':trastes['3'],
              '6':trastes['0']},

        'D':{ '1':trastes['3'],
              '2':trastes['2'],
              '3':trastes['3'],
              '4':trastes['0'],
              '5':trastes['0'],
              '6':trastes['0']},

        'Em':{'1':trastes['2'],
              '2':trastes['0'],
              '3':trastes['1'],
              '4':trastes['2'],
              '5':trastes['2'],
              '6':trastes['0']},



        'F':{ '1':trastes['4'],
              '2':trastes['4'],
              '3':trastes['3'],
              '4':trastes['3'],
              '5':trastes['3'],
              '6':trastes['1']},

        'G':{ '1':trastes['2'],
              '2':trastes['2'],
              '3':trastes['0'],
              '4':trastes['0'],
              '5':trastes['2'],
              '6':trastes['3']},
        
        'No_Chord': {'1': trastes['0'],
              '2': trastes['0'],
              '3': trastes['0'],
              '4': trastes['0'],
              '5': trastes['0'],
              '6': trastes['0']},
       }




# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)


btn_pin = 19

GPIO.setup(btn_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(btn_pin,GPIO.RISING,callback=mover,bouncetime=5000)

pines = [11, 13, 15, 16, 18, 22]
p=[0, 0, 0, 0, 0, 0]





for i in range(6):
    p[i] = Servo(pines[i])



acorde = "No_Chord"
grados = []
for num in range(1,7):
    grado = trastes_a_mm(chords[acorde][str(num)],servos[str(num)])
    grados.append(grado)
print("Moviendo a " + acorde)
for i in range(6):
    p[i].grados_duty(grados[i])



model = load_model("Descargas/cnn_model.h5")

#dir_img = "Descargas/2.jpeg"


chord_list = ["No_Chord","Am","B","C","D","Em","F","G"]



 
cam = cv2.VideoCapture(0)

size=(64,64)
try:
    while True:

        ret, frame = cam.read()
        frame = frame[0:120,0:120]
        
        frame2 = cv2.resize(frame,size)
        frame = cv2.flip(frame,1)
        frame2 = np.expand_dims(frame2, axis=0)
        frame3 = cv2.resize(frame,(480,480))
        res = model.predict(frame2)
        acorde = str(chord_list[np.argmax(res)])
        cv2.putText(frame3,acorde,(20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 8, cv2.LINE_AA)
        grados = []
        for num in range(1,7):
            grado = trastes_a_mm(chords[acorde][str(num)],servos[str(num)])
            grados.append(grado)

        cv2.imshow("CAM",frame3)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


except KeyboardInterrupt:
    cam.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()