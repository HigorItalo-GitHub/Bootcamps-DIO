# Meu Projeto API TDD

# 🛒 Product API - TDD com FastAPI

Esta API foi desenvolvida para gerenciar produtos (por exemplo, aparelhos celulares), aplicando **Test-Driven Development (TDD)** em todas as etapas.  
O projeto utiliza **FastAPI** como framework principal e foi implementado em um ambiente com **Python 3.13.4** rodando em **Windows 10**.

---

## 🚀 Tecnologias Utilizadas
- **Python 3.13.4**
- **FastAPI**
- **Uvicorn**
- **Pytest** (para testes automatizados)
- **Pydantic** (validação de dados)
- **MongoDB (mockado com FakeCollection nos testes)**

---

## ⚙️ Como Rodar o Projeto

### 1. Clonar o repositório
git clone https://github.com/HigorItalo-GitHub/BootcampDio.git
cd API_TDD


### 2. Criar e ativar um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


### 3. Instalar as dependências
pip install -r requirements.txt


### 4. Executar a aplicação
uvicorn main:app --reload


A API estará disponível em: http://127.0.0.1:8000


# 🧪 Como Rodar os Testes
pytest -v


Durante os testes, foi utilizada uma FakeCollection para simular o banco de dados MongoDB, evitando dependências externas e garantindo a execução consistente dos testes.


# 📖 Detalhes do Desenvolvimento

O projeto foi desenvolvido em um computador com Windows 10.

Foi adotado o Python 3.13.4, que trouxe alguns desafios de compatibilidade inicial com bibliotecas.

Para a abordagem TDD (Test-Driven Development), foi necessário implementar uma classe chamada FakeCollection, que simula operações do MongoDB (insert_one, find_one, delete_one, etc.), garantindo testes unitários e funcionais sem a necessidade de um banco real.

Essa estratégia possibilitou a escrita de testes confiáveis, eliminando problemas relacionados a event loops e dependências externas.


# 📌 Endpoints Principais

POST /products → Cria um novo produto

GET /products → Lista todos os produtos

GET /products/{id} → Obtém detalhes de um produto

PATCH /products/{id} → Atualiza informações de um produto

DELETE /products/{id} → Remove um produto
