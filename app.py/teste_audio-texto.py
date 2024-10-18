from flask import Flask, request, render_template, redirect
from vosk import Model, KaldiRecognizer
import wave
import json
import os

app = Flask(__name__)

# Carregar os modelos de idioma
model_en = Model("model-en/vosk-model-small-en-us-0.15")
model_pt = Model("model-pt/vosk-model-small-pt-0.3")

def transcrever_audio(caminho_audio):
    wf = wave.open(caminho_audio, "rb")

    # Verificar formato do áudio
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("O áudio precisa estar em formato mono, 16-bit, 16000 Hz.")

    # Identificar o idioma do arquivo de áudio
    idioma = identificar_idioma(caminho_audio)
    if idioma == 'en':
        rec = KaldiRecognizer(model_en, wf.getframerate())
    elif idioma == 'pt':
        rec = KaldiRecognizer(model_pt, wf.getframerate())
    else:
        raise ValueError("Idioma não suportado ou não reconhecido.")

    # Processar o áudio e transcrever
    texto_final = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto_final += result.get('text', '') + " "
        else:
            partial_result = json.loads(rec.PartialResult())
            texto_final += partial_result.get('partial', '') + " "
    
    final_result = json.loads(rec.FinalResult())
    texto_final += final_result.get('text', '')

    return texto_final.strip()

def identificar_idioma(caminho_audio):
    if "en" in os.path.basename(caminho_audio):
        return "en"
    elif "pt" in os.path.basename(caminho_audio):
        return "pt"
    else:
        return "unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audiofile' not in request.files:
        return redirect(request.url)
    file = request.files['audiofile']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        try:
            text = transcrever_audio(filepath)
            os.remove(filepath)  # Remover o arquivo após processar
            return render_template('index.html', transcript=text)
        except Exception as e:
            return str(e)

if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
