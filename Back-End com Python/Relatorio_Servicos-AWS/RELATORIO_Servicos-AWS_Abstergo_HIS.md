# RELATÓRIO DE IMPLEMENTAÇÃO DE SERVIÇOS AWS

**Data:** 08/01/2026  
**Empresa:** Abstergo Industries  
**Responsável:** Higor I. Santos  

---

## Introdução

Este relatório apresenta o processo de implementação de serviços em nuvem na empresa **Abstergo Industries**, realizado por **Higor I Santos**, a pedido da gestão financeira da organização.

A PharmaHub atua como um **hub de distribuição farmacêutica**, integrando operações logísticas e de dados para empresas parceiras do setor. Até o momento, a empresa não fazia uso de serviços de computação em nuvem, mantendo sua infraestrutura baseada exclusivamente em recursos locais (on-premises).

O objetivo principal deste projeto foi **elencar e propor a adoção de três serviços AWS**, priorizando **redução imediata de custos operacionais**, maior previsibilidade financeira e diminuição de gastos com infraestrutura física, sem comprometer a segurança e a confiabilidade exigidas pelo setor farmacêutico.

---

## Descrição do Projeto

O projeto de implementação foi dividido em **três etapas**, cada uma associada a um serviço AWS específico, selecionado com foco em **simplicidade, baixo custo inicial e impacto financeiro direto**.

### Etapa 1:
- **Nome da ferramenta:** Amazon S3 (Simple Storage Service)  
- **Foco da ferramenta:** Armazenamento escalável e de baixo custo  
- **Descrição de caso de uso:**  
  O Amazon S3 foi proposto para substituir servidores locais e dispositivos físicos utilizados para armazenar documentos operacionais, relatórios logísticos, notas fiscais, arquivos de integração com parceiros e backups internos.

  Com o S3, a empresa passa a pagar apenas pelo volume de dados efetivamente armazenado, eliminando custos recorrentes com:
  - Manutenção de servidores físicos
  - Aquisição de novos equipamentos de armazenamento
  - Riscos de perda de dados por falhas de hardware  

  Além disso, políticas de ciclo de vida permitem mover dados pouco acessados para camadas ainda mais baratas, gerando **economia contínua**.

---

### Etapa 2:
- **Nome da ferramenta:** Amazon EC2 (Elastic Compute Cloud)  
- **Foco da ferramenta:** Computação sob demanda e eliminação de infraestrutura ociosa  
- **Descrição de caso de uso:**  
  O Amazon EC2 foi indicado para hospedar sistemas internos da empresa, como aplicações de controle logístico, integrações com parceiros e serviços administrativos, substituindo servidores locais subutilizados.

  A principal vantagem financeira está no modelo **pay-as-you-go**, que permite:
  - Desligar instâncias fora do horário comercial
  - Ajustar capacidade conforme a demanda real
  - Evitar gastos com servidores superdimensionados  

  Dessa forma, a empresa reduz custos fixos elevados e passa a ter **controle direto sobre o consumo computacional**, alinhando despesas à operação real.

---

### Etapa 3:
- **Nome da ferramenta:** AWS Cost Explorer e AWS Budgets  
- **Foco da ferramenta:** Controle financeiro, visibilidade de custos e governança  
- **Descrição de caso de uso:**  
  Para garantir que a adoção da nuvem resulte em economia contínua, foi proposta a utilização combinada do AWS Cost Explorer e do AWS Budgets.

  Essas ferramentas permitem:
  - Visualizar detalhadamente os custos por serviço e período
  - Identificar rapidamente desperdícios ou recursos ociosos
  - Criar alertas automáticos quando os gastos ultrapassarem limites definidos pelo financeiro  

  Essa etapa é essencial para uma empresa sem experiência prévia em cloud, pois garante **transparência, previsibilidade orçamentária e controle rigoroso dos gastos**, atendendo diretamente às preocupações da gestão financeira.

---

## Conclusão

A implementação dos serviços AWS na empresa **Abstergo Industries** tem como resultado esperado a **redução imediata de custos operacionais**, a eliminação de investimentos em infraestrutura física e o aumento da previsibilidade financeira.

Os serviços propostos — Amazon S3, Amazon EC2 e AWS Cost Explorer/Budgets — formam uma base sólida, segura e financeiramente controlável para a entrada da empresa no modelo de computação em nuvem.

Recomenda-se a continuidade da utilização das ferramentas implementadas e, após a maturação inicial, a avaliação de novos serviços AWS que possam ampliar ainda mais a eficiência operacional e a competitividade da empresa.

---

## Anexos (a incluir)

- Documentação oficial dos serviços AWS utilizados  
- Planilha de estimativa de custos mensais  
- Política inicial de controle e monitoramento de gastos  

---

**Assinatura do Responsável pelo Projeto:**

Higor I. Santos
