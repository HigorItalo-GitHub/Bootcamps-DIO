📦 E-Commerce Microservices — Estoque, Vendas, Autenticação, API Gateway e RabbitMQ

Este repositório contém um projeto completo de microserviços construído com .NET, C#, Entity Framework Core, SQL Server, RabbitMQ, JWT e API Gateway (Ocelot).

O sistema simula o núcleo de uma plataforma de e-commerce, permitindo gerenciamento de estoque, registro de vendas e autenticação, com comunicação assíncrona entre microserviços.

🧱 Arquitetura Geral

O ecossistema é composto por quatro serviços:

Serviço	Descrição
auth-service	Responsável pela autenticação de usuários e emissão de JWT.
stock-service	Gerencia o cadastro de produtos e controla o estoque. Consome mensagens de vendas.
sales-service	Gerencia pedidos e publica eventos de venda no RabbitMQ.
api-gateway	Porta de entrada única utilizando Ocelot. Roteia requisições para os microserviços.

Além disso, são utilizados:

RabbitMQ — comunicação assíncrona entre serviços

SQL Server — armazenamento de produtos e pedidos

Docker Compose — orquestração completa do ambiente

🗂️ Estrutura do Repositório
ecommerce-microservices/
│
├── auth-service/
│   ├── Controllers/
│   ├── Models/
│   ├── Services/
│   ├── Dockerfile
│   ├── appsettings.json
│   └── Program.cs
│
├── stock-service/
│   ├── Controllers/
│   ├── Models/
│   ├── Services/
│   ├── Data/
│   ├── Dockerfile
│   └── Program.cs
│
├── sales-service/
│   ├── Controllers/
│   ├── Models/
│   ├── Services/
│   ├── Data/
│   ├── Dockerfile
│   └── Program.cs
│
├── api-gateway/
│   ├── ocelot.json
│   ├── Dockerfile
│   └── Program.cs
│
├── docker-compose.yml
├── README.md
├── LICENSE
└── .gitignore

🚀 Funcionalidades Implementadas
🔐 1. Autenticação via JWT

Serviço de login (auth-service)

Usuário de demonstração:

username: demo
password: demo


Token JWT inclui:

Username

Validade

Assinatura baseada no JWT_SECRET

📦 2. Gestão de Estoque

Cadastro de produtos

Consulta de produtos

Atualização automática via RabbitMQ quando ocorrer uma venda

Persistência via EF Core (SQL Server)

🛒 3. Gestão de Vendas

Criação de pedidos

Verificação básica de existência de produtos

Publicação de evento OrderCreated no RabbitMQ

Persistência via EF Core (SQL Server)

🔁 4. Comunicação Assíncrona (RabbitMQ)

Fluxo:

Pedido criado no sales-service

Evento enviado ao RabbitMQ

stock-service consome evento

Estoque é atualizado

🧩 5. API Gateway com Ocelot

Roteamentos configurados:

Rota	Microserviço	Exemplo
/api/products/*	stock-service	GET /api/products
/api/orders/*	sales-service	POST /api/orders
/api/auth/*	auth-service	POST /api/auth/login
🐳 Executando o Projeto com Docker
1️⃣ Requisitos

Docker

Docker Compose

2️⃣ Subir tudo

No diretório raiz:

docker compose up --build


Serviços gerados:

Serviço	Porta
auth-service	5100
stock-service	5200
sales-service	5300
api-gateway	8000
SQL Server	1433
RabbitMQ UI	15672
3️⃣ Acessos úteis

API Gateway → http://localhost:8000

RabbitMQ → http://localhost:15672
 (guest/guest)

SQL Server → localhost,1433

🛢️ Banco de Dados e Migrations

Este projeto usa SQL Server via Docker.

As migrations devem ser executadas localmente nos serviços:

StockService
cd stock-service
dotnet ef migrations add InitialCreate
dotnet ef database update

SalesService
cd sales-service
dotnet ef migrations add InitialCreate
dotnet ef database update

🔐 Autenticação e Uso de Token
1️⃣ Login
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "demo",
  "password": "demo"
}


Resposta:

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5c..."
}

2️⃣ Autorização nas demais APIs

Enviar header:

Authorization: Bearer <token>

🧪 Exemplos de Uso
✔ Cadastrar produto (estoque)
POST http://localhost:8000/api/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Teclado Gamer",
  "description": "Teclado RGB",
  "price": 150.0,
  "quantity": 20
}

✔ Criar pedido (vendas)
POST http://localhost:8000/api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "productId": 1,
  "quantity": 3
}

✔ Consultar pedidos
GET http://localhost:8000/api/orders
Authorization: Bearer <token>

🔎 Critérios de Aceitação (Atendidos)

✔ Cadastro de produtos

✔ Criação de pedidos

✔ Atualização de estoque via RabbitMQ

✔ API Gateway funcional

✔ Autenticação via JWT

✔ Arquitetura baseada em microserviços

✔ Persistência com EF Core e SQL Server

✔ Código organizado seguindo boas práticas

🔧 Melhorias Futuras (Opcional)

Adicionar testes unitários completos

Implementar autenticação com banco via Identity

Criar saga/compensation para rollback de falha de estoque

Incluir validações síncronas entre serviços

Monitoração via Grafana + Prometheus
  5. Use `docker compose up --build` para rodar o ambiente com SQL Server e RabbitMQ.
