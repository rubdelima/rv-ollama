## Como executar

Para executar, você primeiramente deve ter o [Ollama](https://ollama.com/) e alguns modelos de visão.

### Passos iniciais

1. **Instale o Ollama**  
   Você pode instalar o Ollama a partir deste [link](https://ollama.com/).

2. **Baixe os modelos necessários**  
   Após a instalação, você pode baixar alguns modelos executando os comandos abaixo no terminal:  
   ```sh
   ollama pull gemma3
   ollama pull llama3.2-vision
   ollama pull minicpm-v
   ```

### Preparando o ambiente

1. **Crie um ambiente virtual**  
   Para criar o ambiente virtual e organizar suas dependências, execute:
   ```sh
   python3 -m venv .rv
   ```

2. **Ative o ambiente virtual**  
   No Linux/MacOS:
   ```sh
   source .rv/bin/activate
   ```
   No Windows:
   ```sh
   .rv\Scripts\activate
   ```

3. **Instale as dependências**  
   Com o ambiente virtual ativado, instale as dependências necessárias com:
   ```sh
   pip install -r requirements.txt
   ```

### Executando o projeto

1. Certifique-se de que o Ollama esteja configurado corretamente.
2. Verifique se os modelos de visão foram baixados e estão acessíveis.
3. Execute o programa principal com:
   ```sh
   streamlit run app.py
   ```


---