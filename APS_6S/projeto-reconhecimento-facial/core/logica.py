# core/logica.py

"""
Lógica principal de reconhecimento facial do sistema.
Inclui funções para cadastro, treinamento, reconhecimento e controle de vídeo.
"""

import cv2
import os
import numpy as np
import time
import threading
from PIL import Image
from database.setup import SessionLocal
from database.models import Usuario


class FacialRecognitionLogic:
    """
    Classe principal para lógica de reconhecimento facial.
    """
    PASTA_ASSETS = 'assets'
    ARQUIVO_CASCADE = 'haarcascade_frontalface_default.xml'
    PASTA_DATASET = 'dataset'
    PASTA_TRAINER = 'trainer'
    ARQUIVO_TRAINER = 'trainer.yml'
    LIMIAR_CONFIANCA = 30


    def __init__(self, modo_simulacao=True, video_path="assets/video-teste2.mp4"):
        """
        Inicializa variáveis, caminhos e componentes do OpenCV.
        """
        self.modo_simulacao = modo_simulacao
        self.caminho_video_simulacao = video_path
        self.caminho_cascade = os.path.join(self.PASTA_ASSETS, self.ARQUIVO_CASCADE)
        self.caminho_dataset = os.path.join(self.PASTA_ASSETS, self.PASTA_DATASET)
        self.caminho_trainer = os.path.join(self.PASTA_ASSETS, self.PASTA_TRAINER)
        self.caminho_arquivo_trainer = os.path.join(self.caminho_trainer, self.ARQUIVO_TRAINER)
        self._criar_pastas()
        if not os.path.exists(self.caminho_cascade):
            raise FileNotFoundError(f"Erro: Classificador não encontrado em '{self.caminho_cascade}'")
        self.detector_face = cv2.CascadeClassifier(self.caminho_cascade)
        self.reconhecedor = cv2.face.LBPHFaceRecognizer_create()
        self.current_frame = None
        self.thread_video = None
        self.parar_thread = False


    def _criar_pastas(self):
        """
        Cria as pastas de assets necessárias se não existirem.
        """
        for path in [self.caminho_dataset, self.caminho_trainer]:
            if not os.path.exists(path):
                os.makedirs(path)


    def salvar_e_obter_usuario(self, nome: str, cpf: str, nivel_acesso: str) -> Usuario | None:
        """
        Salva um novo usuário no banco de dados se o CPF não existir.
        """
        db = SessionLocal()
        try:
            if db.query(Usuario).filter(Usuario.cpf == cpf).first():
                print(f"Erro: CPF {cpf} já cadastrado.")
                return None
            novo_usuario = Usuario(nome=nome, cpf=cpf, nivel_acesso=nivel_acesso)
            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)
            print(f"Usuário '{nome}' salvo no banco com ID: {novo_usuario.id}")
            return novo_usuario
        finally:
            db.close()


    def salvar_fotos_capturadas(self, usuario_id: int, lista_de_fotos: list):
        """
        Salva as imagens de rosto capturadas em memória para o dataset no disco.
        """
        print(f"Salvando {len(lista_de_fotos)} fotos para o usuário ID: {usuario_id}...")
        for i, foto in enumerate(lista_de_fotos, 1):
            caminho_foto = os.path.join(self.caminho_dataset, f"user.{usuario_id}.{i}.jpg")
            cv2.imwrite(caminho_foto, foto)
        print("Fotos salvas com sucesso.")


    def processar_rosto_para_captura(self) -> np.ndarray | None:
        """
        Se houver um único rosto no frame atual, retorna a imagem recortada em escala de cinza.
        """
        if self.current_frame is None:
            return None
        frame_cinza = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector_face.detectMultiScale(frame_cinza, 1.3, 5, minSize=(30, 30))
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            return frame_cinza[y:y+h, x:x+w]
        return None


    def treinar_modelo(self) -> bool:
        """
        Treina o modelo de reconhecimento facial com as imagens do dataset.
        """
        print("Iniciando treinamento...")
        caminhos = [os.path.join(self.caminho_dataset, f) for f in os.listdir(self.caminho_dataset)]
        faces, ids = [], []
        for caminho_img in caminhos:
            img = Image.open(caminho_img).convert('L')
            img_np = np.array(img, 'uint8')
            id_usuario = int(os.path.split(caminho_img)[-1].split(".")[1])
            faces.append(img_np)
            ids.append(id_usuario)
        if not faces:
            print("Nenhuma face encontrada para treinar.")
            return False
        self.reconhecedor.train(faces, np.array(ids))
        self.reconhecedor.write(self.caminho_arquivo_trainer)
        print("Treinamento concluído!")
        return True

    def verificar_rosto_existente(self, rosto_cinza: np.ndarray) -> str | None:
        """
        Verifica se um rosto já está cadastrado no modelo treinado.
        Retorna o nome do usuário se reconhecido com confiança, senão None.
        """
        try:
            id_predito, confianca = self.reconhecedor.predict(rosto_cinza)

            if confianca < self.LIMIAR_CONFIANCA:
                db = SessionLocal()
                try:
                    usuario = db.query(Usuario).filter(Usuario.id == id_predito).first()
                    if usuario:
                        return usuario.nome
                finally:
                    db.close()
        except cv2.error:
            return None
        return None

    def preparar_acesso(self) -> bool:
        """
        Verifica se o modelo treinado existe e o carrega na memória.
        """
        if not os.path.exists(self.caminho_arquivo_trainer):
            return False
        self.reconhecedor.read(self.caminho_arquivo_trainer)
        return True


    def reconhecer_rosto(self) -> tuple:
        """
        Tenta reconhecer um rosto no frame atual e retorna o frame com anotações e o objeto do usuário.
        """
        if self.current_frame is None:
            return self.current_frame, None
        frame_anotado = self.current_frame.copy()
        frame_cinza = cv2.cvtColor(frame_anotado, cv2.COLOR_BGR2GRAY)
        faces = self.detector_face.detectMultiScale(frame_cinza, 1.3, 5, minSize=(30, 30))
        usuario_reconhecido = None
        for (x, y, w, h) in faces:
            id_predito, confianca = self.reconhecedor.predict(frame_cinza[y:y+h, x:x+w])
            nome, cor = "Desconhecido", (0, 0, 255)
            if confianca < self.LIMIAR_CONFIANCA:
                db = SessionLocal()
                try:
                    usuario = db.query(Usuario).filter(Usuario.id == id_predito).first()
                    if usuario:
                        nome, cor = usuario.nome, (0, 255, 0)
                        usuario_reconhecido = usuario
                finally:
                    db.close()
            cv2.rectangle(frame_anotado, (x, y), (x+w, y+h), cor, 2)
            cv2.putText(frame_anotado, nome, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, cor, 2)
        return frame_anotado, usuario_reconhecido


    def iniciar_camera(self):
        """
        Inicia a thread de captura de vídeo para não travar a interface.
        """
        if self.thread_video is None or not self.thread_video.is_alive():
            self.parar_thread = False
            self.thread_video = threading.Thread(target=self._loop_captura_video, daemon=True)
            self.thread_video.start()


    def parar_camera(self):
        """
        Para a thread de captura de vídeo de forma segura.
        """
        if self.thread_video and self.thread_video.is_alive():
            self.parar_thread = True
            self.thread_video.join()
        self.thread_video = None
        self.current_frame = None


    def _loop_captura_video(self):
        """
        Loop executado em uma thread separada para capturar os frames.
        """
        if self.modo_simulacao:
            cap = cv2.VideoCapture(self.caminho_video_simulacao)
        else:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            #camera_adress = "http://"
            #cap = cv2.VideoCapture(camera_adress)
        if not cap.isOpened():
            print("THREAD: Erro ao abrir a fonte de vídeo.")
            return
        while not self.parar_thread:
            ret, frame = cap.read()
            if ret:
                self.current_frame = frame
            elif self.modo_simulacao:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            else:
                break
            time.sleep(1/30)
        cap.release()
        print("THREAD: Fonte de vídeo liberada.")