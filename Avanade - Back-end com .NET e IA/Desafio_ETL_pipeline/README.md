
# ETL com IA Generativa (OpenAI GPT)

Este projeto demonstra um pipeline ETL simples que:
- Extrai IDs de usuários de um arquivo CSV
- Transforma os dados gerando mensagens de marketing personalizadas usando a API OpenAI
- Carrega os dados transformados em um novo CSV

## Estrutura do Projeto
```
etl_pipeline/
├── data/
│     └── users.csv
├── output/
├── etl.py
├── gpt_service.py
└── README.md
```

## Como Executar

1. Instale dependências:
```
pip install openai pandas
```

2. Exporte sua chave de API:
- Windows:
```
setx OPENAI_API_KEY "SUA_CHAVE"
```
- Linux/Mac:
```
export OPENAI_API_KEY="SUA_CHAVE"
```

3. Execute:
```
python etl.py
```

O arquivo com mensagens será gerado em: `output/messages.csv`
