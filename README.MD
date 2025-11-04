### Criar o ambiente virtual dentro da pasta do projeto

    python3 -m venv venv

### Ativar o ambiente virtual
    
    source venv/bin/activate
 
### Instalar os pacotes dentro do ambiente

    pip install fastapi uvicorn opencv-python requests

### Rodar sua API

    uvicorn main:app --reload
