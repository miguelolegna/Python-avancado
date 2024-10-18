from flask import Flask, render_template, request, jsonify, send_file
from flask_assets import Environment, Bundle
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import aifc
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Configurar Flask-Assets
assets = Environment(app)

# Definir um bundle para o SCSS
scss = Bundle('scss/styles.scss', filters='libsass', output='scss/styles.css')
assets.register('scss_all', scss)

# Carregar o modelo e o tokenizer
model_name = "pierreguillou/gpt2-small-portuguese"  # Modelo em português
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Rotas
@app.route('/') 
def index():
    return render_template('index.html')  # Corrigido de render_templates para render_template


@app.route('/Documentação')  # Adicionada a barra no início
def Documentação():
    return render_template('/Documentação.html')

@app.route('/API')  
def API():
    return render_template('API.html')

@app.route('/AI')  
def AI():
    return render_template('AI.html')

@app.route('/tecnologia')  
def tecnologia():
    return render_template('tecnologia.html')


@app.route('/detalhes')  
def detalhes():
    return render_template('detalhes.html')
    

@app.route('/java')  
def java():
    return render_template('java.html')

@app.route('/python') 
def python():
    return render_template('python.html')

@app.route('/cpp')    
def cpp():
    return render_template('cpp.html')

@app.route('/db')    
def database():
    return render_template('db.html')

@app.route('/reds')  
def networks():
    return render_template('reds.html')

@app.route('/pross-comp')  
def computing():
    return render_template('pross-comp.html')


@app.route('/JAI')
def JAI():
    return render_template('JAI.html')




@app.route('/perguntar', methods=['POST'])
def perguntar():
    pergunta = request.json['pergunta']
    
    try:
        # Preparar a entrada para o modelo
        input_ids = tokenizer.encode(pergunta, return_tensors='pt')
        
        # Gerar a resposta
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
        
        # Decodificar a resposta
        resposta = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Remover a pergunta da resposta, se estiver presente
        resposta = resposta.replace(pergunta, "").strip()
    except Exception as e:
        resposta = f"Desculpe, ocorreu um erro ao gerar a resposta: {str(e)}"

    return jsonify({'resposta': resposta})

@app.route('/audio_to_text', methods=['POST'])
def audio_to_text():
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='pt-BR')
            return jsonify({'texto': text})
        except sr.UnknownValueError:
            return jsonify({'erro': 'Não consegui entender o áudio.'}), 400
        except sr.RequestError:
            return jsonify({'erro': 'Erro ao conectar ao serviço de reconhecimento de fala.'}), 500

@app.route('/text_to_audio', methods=['POST'])
def text_to_audio():
    texto = request.json['texto']
    tts = gTTS(text=texto, lang='pt-br')
    
    # Salvar o áudio em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        tts.save(f"{tmp_file.name}.mp3")
        return jsonify({'audio_url': f"{tmp_file.name}.mp3"})

@app.route('/test_audio', methods=['GET'])
def test_audio():
    # Texto de teste
    test_text = "Olá, este é um teste de áudio."
    
    # Gerar áudio a partir do texto
    tts = gTTS(text=test_text, lang='pt-br')
    
    # Salvar o áudio em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        temp_filename = tmp_file.name
        tts.save(temp_filename)
    
    # Enviar o arquivo de áudio como resposta
    return send_file(temp_filename, mimetype='audio/mp3')

# Iniciar o app
if __name__ == '__main__':
    app.run(debug=True)