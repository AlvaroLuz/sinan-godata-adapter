# Adaptador de Dados do SINAN para o GoData 

Projeto ainda não concluído.

## Descrição Geral

Este projeto fornece uma ferramenta de linha de comando para **processamento, mapeamento e upload de dados do SINAN** para uma instância local ou remota do **GoData**.
O fluxo completo inclui:

1. **Leitura de planilhas .xlsx** contendo notificações de casos.
2. **Normalização, padronização e enriquecimento dos dados** (ex.: resolução de localização, tradução de códigos, classificação de campos).
3. **Mapeamento para as entidades esperadas pelo GoData**.
4. **Envio autenticado para a API do GoData**, criando ou atualizando casos.

O código é especialmente projetado para uso em servidores Linux Ubuntu 22.04.

---

## Funcionalidades

### Processamento dos dados do SINAN

* Conversão de planilhas `.xlsx` em registros estruturados.
* Padronização de campos usando um **registry centralizado de traduções**.
* Aplicação de regras de negócio específicas por doença (ex.: sarampo, dengue).

### Mapeamento para Entidades GoData

* Conversão de um caso processado em uma estrutura compatível com o modelo GoData.
* Conectores reutilizáveis para campos de endereço, classificação, gênero, documentos etc.

### Enriquecimento de Dados

* Resolução automática de municípios, unidades federativas e coordenadas (quando aplicável).
* Normalização de valores inexistentes, inválidos ou divergentes.

### Upload via API

* Autenticação via token.
* Criação de casos GoData.
* Opção de processamento total ou parcial.

---

## 📁 Estrutura do Repositório

```
.
├── core/                       # Módulos centrais do sistema
│   ├── adapters/               # Comunicação com API (GoData)
│   ├── mappers/                # Classes de tradução 
│   ├── sinan_processor.py      # Pipeline de processamento SINAN
│   ├── sinan_case_mapper.py    # Mapeador de dados para classe
│   ├── location_solver.py      # Resolve ids de municípios para id de localização
│   ├── utils.py
│   └── entities.py             # Estruturas de dados centrais
│
├── diseases/              # Módulos de tratamento específicos por doença
│   ├── sarampo/
│   │   ├── mapping.py
│   │   └── processor.py
│   └── dengue/            # (estruturado para expansão futura)
│
├── data/
│   ├── input/             # Arquivos de entrada (.xlsx)
│   └── output/            # Dados processados e debug
│
├── main.py                # Entry point principal
├── README.md
├── poetry.lock
└── pyproject.toml
```

---

## Requisitos

* Python 3.9+
* Poetry (para instalação e isolamento de ambiente)
* Dependências listadas no `pyproject.toml`

---

## Instalação e Execução

Instale as dependências usando **Poetry**:

```bash
poetry install
```

Execute o pipeline principal (TBW CLI ainda não implementada):

```bash
poetry run python main.py 
```

---

## Configuração

Algumas configurações devem ser feitas via variáveis de ambiente:

| Variável          | Descrição                 |
| ----------------- | ------------------------- |
| `API_URL`         | URL do servidor GoData    |
| `API_TOKEN`       | Token da API              |
| `API_USERNAME`    | Username de um usuário    |
| `API_PASSWORD`    | Senha do usuário          |

Configuração alternativa via arquivo `.env` também é suportada (opcional).

---

## Uso

### Executar processamento sem enviar ao GoData:

```bash
poetry run python main.py 
```

### Gerar arquivo de depuração:

```bash
--debug data/output/cases_debug.json
```

### Filtrar por intervalo de linhas:

```bash
--start 0 --end 200
```

---

## Componentes Principais do Código (Visão Geral)

### **1. core/sinan_processor.py**

Controla o fluxo geral:

* aplica as traduções de a colunas da planilha,
* realiza o tratamento geral dos dados,
* retorna a planilha uma planilha processada

### **2. core/mappers/**

Contém mapeadores para os valores fixos do godata, ex.:"LNG_REFERENCE_DATA_CATEGORY_ADDRESS_TYPE_USUAL_PLACE_OF_RESIDENCE":

* `gender_map.py`
* `classification_map.py`
* `document_map.py`
* `address_type_map.py`
* etc.

Todos são registrados centralmente via `translation_registry.py` e são usados no processo de tradução.

### **3. diseases/<doença>/**

Tratamentos de dados para os dados específicos do agravo que será rastreado no godata. Idealmente trata e normaliza todas as colunas que serão convertidas em dados dos questionários. 

Exemplos de ações realizadas no módulo da doença:
* tratamento da coluna de de classificação final,
* tratamento da coluna de evolução,
* tratamento de datas.

### **4. core/adapters/api_client.py**

Cliente HTTP que envia casos para o GoData.

---

## Contato

Em caso de dúvidas, solicitações de suporte ou sugestões:

* Abra uma *issue* no repositório.
* Ou contate o responsável do projeto na SDS.

