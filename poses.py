import cv2                          # Biblioteca para vídeo e imagens
import mediapipe as mp              # Biblioteca do Google para reconhecimento corporal
import numpy as np                  # Para cálculos matemáticos (vetores e ângulos
import serial                      # Comunicação com Arduino via porta serial
import time                        # Usado para dar tempo de inicializar o Arduino
# Inicia conexão com o Arduino (ajuste a porta conforme necessário)
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # Aguarda o Arduino iniciar

# Inicializa o modelo de detecção de pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils  # Para desenhar na tela os pontos e traços

# Contador de repetições na rosca direta
contador = 0
fase = None  # 'descendo' ou 'subindo' baseado no ângulo do braço

# Abre a webcam
cap = cv2.VideoCapture("exercicio.mp4")

while True:
    ret, frame = cap.read()          # Captura o vídeo frame a frame
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Volta ao início do vídeo, loop infinito
        continue
        #break
    frame = cv2.resize(frame, (500, 500)) # imagem redimensionada para 500 x 500 (linha coluna)
    frame = cv2.flip(frame, 1)       # Espelha o vídeo (efeito espelho)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB (MediaPipe espera RGB)
    resultado = pose.process(rgb)    # Processa a pose no frame atual

    if resultado.pose_landmarks:     # Se algum corpo for detectado
        mp_draw.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Pegando os pontos do braço direito
        pontos = resultado.pose_landmarks.landmark
        ombro = [pontos[12].x * frame.shape[1], pontos[12].y * frame.shape[0]]     # Ponto do ombro direito frame.shape retorna a dimensão da imagem
        cotovelo = [pontos[14].x * frame.shape[1], pontos[14].y * frame.shape[0]]  # Cotovelo direito frame.shape[1] qtd colunas, eixo x
        punho = [pontos[16].x * frame.shape[1], pontos[16].y * frame.shape[0]]     # Pulso direito frame.shape[0] qtd linhas, eixo y

        # Cálculo direto do ângulo entre ombro, cotovelo e punho
        a = np.array(ombro)
        b = np.array(cotovelo)
        c = np.array(punho)

        angulo = np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) -
                            np.arctan2(a[1]-b[1], a[0]-b[0]))
        angulo = np.abs(angulo)
        if angulo > 180:
            angulo = 360 - angulo

        # Exibe o ângulo na tela
        cv2.putText(frame, f"Angulo: {int(angulo)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Lógica da repetição
        if angulo > 160:
            fase = 'descendo'
        if angulo < 40 and fase == 'descendo':
            fase = 'subindo'
            contador += 1
            arduino.write(b'U')
        
        if (contador/6 == 1):
            arduino.write(b'R')
        elif (contador/6 == 2):
            arduino.write(b'Y')
        elif (contador/6 == 3):
            arduino.write(b'S')
        elif (contador/6 == 4):
            arduino.write(b'G')


        # Exibe o número de repetições
        cv2.putText(frame, f"Repeticoes: {contador}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostra o vídeo com as informações
    cv2.imshow("Rosca Biceps - Pose Detection", frame)

    # Encerra se apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza a aplicação
cap.release()
cv2.destroyAllWindows()