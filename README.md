# Laboratório Prático do Padrão de Projeto Proxy (Design Pattern)

**Disciplina:** Engenharia de Software II  
**Instituição:** Faculdade Católica da Paraíba (FAFIC) — Cajazeiras-PB, 2026  
**Tema:** Padrão Estrutural Proxy (GoF / Refactoring Guru)  
**Equipe Acadêmica:**
* João Pedro Cruz
* Pedro Henrique
* Pedro Arlyx
* Fabricio Nathan
* Lucas Gonçalves

---

## 1. Apresentação do Projeto e Objetivo Acadêmico

Este projeto é o complemento prático e executável do artigo acadêmico da disciplina de **Engenharia de Software II**. Ele foi desenvolvido para demonstrar visualmente e na prática como funciona o **Padrão de Projeto Estrutural Proxy**, permitindo que alunos e professores compreendam suas nuances através de um laboratório interativo desenvolvido em **Python 3.14 e Streamlit**.

O software demonstra como um objeto intermediário (*Proxy*) controla o acesso a um serviço real (*RealSubject*), expondo rigorosamente a **mesma interface** do serviço original, sem que o cliente (*Client*) precise sofrer qualquer alteração para se beneficiar de comportamentos como **inicialização preguiçosa**, **controle de permissões (segurança)**, **cache**, **auditoria/logs**, **acesso remoto transparente** e **gerenciamento de ciclo de vida (referência inteligente)**.

---

## 2. Fundamentação Teórica Baseada no Trabalho

O projeto espelha estritamente as seções do documento acadêmico:

1. **Introdução:** O Proxy intercepta todas as chamadas direcionadas ao serviço real através da mesma interface, executando pré ou pós-processamento de forma transparente.
2. **O Problema:** Como gerenciar objetos pesados ou caros (ex.: conexões com banco de dados) sem duplicar código de lazy loading nos clientes e sem poder modificar bibliotecas de terceiros.
3. **A Solução e Estrutura:** Quatro participantes canônicos:
   * **`Subject` (Interface):** Contrato comum seguido por Proxy e RealSubject.
   * **`RealSubject` (Serviço Real):** Contém a regra de negócio central.
   * **`Proxy`:** Guarda referência ao RealSubject, intercepta e gerencia seu ciclo de vida.
   * **`Client`:** Depende apenas da interface `Subject`.
   * *Analogia do Cartão de Crédito:* O cartão atua como proxy da conta bancária e do dinheiro físico, atendendo à mesma necessidade de pagamento sem expor o dinheiro vivo a riscos de manuseio e transporte.
4. **Exemplo Prático (YouTube):** Implementação fiel da Seção 4 do artigo, utilizando `ThirdPartyYouTubeLib`, `ThirdPartyYouTubeClass`, `CachedYouTubeClass` e `YouTubeManager`.
5. **Tipos de Proxy:** Implementação dos 6 tipos catalogados (Virtual, Proteção, Remoto, Log, Cache e Referência Inteligente).
6. **Vantagens & Desvantagens:** Demonstração visual do Princípio Aberto/Fechado (OCP), transparência ao cliente vs. complexidade de novas classes.
7. **Relação com Outros Padrões:** Diferenciação prática e executável contra **Adapter** (adapta interfaces incompatíveis), **Decorator** (composição dinâmica de responsabilidades pelo cliente) e **Facade** (interface simplificada para múltiplos subsistemas).

---

## 3. Arquitetura e Organização Modular do Projeto

```text
proxy/
├── app.py                          # Aplicação Gráfica Completa em Streamlit (Laboratório Visual)
├── requirements.txt                # Dependências mínimas (streamlit, pytest)
├── pyproject.toml                  # Configuração do pytest e caminhos de importação
├── README.md                       # Documentação acadêmica completa
│
├── interfaces/                     # Contratos abstratos (ABC) do sistema
│   ├── __init__.py
│   ├── subject.py                  # Interface Subject (Estrutura Básica)
│   ├── database_interface.py       # Interface DatabaseInterface (Proxy Virtual)
│   ├── admin_interface.py          # Interface AdminServiceInterface (Proxy de Proteção)
│   ├── remote_interface.py         # Interface RemoteServiceInterface (Proxy Remoto)
│   ├── document_interface.py       # Interface DocumentServiceInterface (Proxy de Log)
│   ├── youtube_interface.py        # Interface ThirdPartyYouTubeLib (Proxy de Cache)
│   └── resource_interface.py       # Interface SharedResourceInterface (Referência Inteligente)
│
├── services/                       # Serviços reais de negócio (RealSubjects)
│   ├── __init__.py
│   ├── real_subject.py             # RealSubject básico
│   ├── database_service.py         # HeavyDatabaseService (simula conexão pesada e latência de rede)
│   ├── admin_service.py            # RealAdminService (operações críticas de sistema)
│   ├── remote_service.py           # RealRemoteServer (simula nó remoto e recepção de pacotes)
│   ├── document_service.py         # RealDocumentService (emissão e assinatura digital)
│   ├── youtube_service.py          # ThirdPartyYouTubeClass (API do YouTube de terceiros)
│   └── resource_service.py         # SharedResourceService (alocação de buffer compartilhado)
│
├── proxies/                        # Implementações dos Proxies intermediários
│   ├── __init__.py
│   ├── basic_proxy.py              # BasicProxy (delegação e hooks de pré/pós processamento)
│   ├── virtual_proxy.py            # VirtualDatabaseProxy (Lazy Loading e reuso de conexão)
│   ├── protection_proxy.py         # ProtectionAdminProxy (Controle RBAC: ADMIN, OPERADOR, CONVIDADO)
│   ├── remote_proxy.py             # RemoteServiceProxy (RPC, Marshalling e Unmarshalling)
│   ├── logging_proxy.py            # LoggingDocumentProxy (Auditoria, timestamps, parâmetros e erros)
│   ├── cache_proxy.py              # CachedYouTubeClass (Cache em memória e economia de tráfego)
│   └── smart_reference_proxy.py    # SmartReferenceProxy (Contador de referências e auto-desalocação)
│
├── clients/                        # Clientes consumidores da aplicação
│   ├── __init__.py
│   ├── client.py                   # ClientApp (consome qualquer Subject indiferentemente)
│   └── youtube_manager.py          # YouTubeManager (renderiza telas consumindo ThirdPartyYouTubeLib)
│
├── patterns_comparison/            # Modelos comparativos com Adapter, Decorator e Facade
│   ├── __init__.py
│   └── comparison_models.py        # Exemplos didáticos das diferenças estruturais
│
├── examples/                       # Scripts executáveis standalone via console
│   ├── basic_proxy.py              # Execução direta da estrutura básica no terminal
│   └── youtube_example.py          # Demonstração do Cache do YouTube no terminal
│
└── tests/                          # Suíte de testes automatizados unitários e de integração
    ├── __init__.py
    └── test_proxies.py             # 12 testes automatizados com 100% de aprovação no pytest
```

---

## 4. Requisitos de Ambiente e Instalação

* **Python:** 3.11 ou superior (desenvolvido e testado em Python 3.14).
* **Sistema Operacional:** Linux, macOS ou Windows.
* **Dependências Externas:** Zero (sem necessidade de banco de dados ou APIs externas instaladas).

### Instalação passo a passo:

1. Clone ou acesse o repositório no terminal:
   ```bash
   cd /caminho/do/projeto/proxy
   ```

2. Instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Como Executar a Aplicação Interativa (Streamlit)

Inicie o servidor do Streamlit executando:

```bash
streamlit run app.py
```

A interface abrirá automaticamente no seu navegador no endereço:
👉 `http://localhost:8501`

### O que você encontrará na interface gráfica:
* **Navegação Lateral:** Seletor intuitivo entre todos os 8 módulos acadêmicos.
* **Demonstrações Interativas:** Botões dedicados para disparar chamadas com feedback visual instantâneo.
* **Métricas em Tempo Real:** Indicadores de cache hits, milissegundos economizados, contagem de clientes e status de alocação de memória.
* **Históricos e Tabelas:** Livros de auditoria, registros de rede RPC e dados de telemetria.
* **Caixas Conceituais:** Explicações claras em português para apresentação direta em sala de aula.

---

## 6. Como Executar os Testes Automatizados (Pytest)

Para rodar a suíte completa de 12 testes automatizados:

```bash
pytest
```

Ou com visualização detalhada e verbose:

```bash
pytest -v
```

### O que os testes cobrem:
* `test_basic_proxy_transparency_to_client`: Prova que o cliente funciona indiferentemente com o serviço real ou proxy.
* `test_virtual_proxy_lazy_initialization`: Garante que o banco pesado NÃO é instanciado na criação do proxy, apenas na primeira query.
* `test_virtual_proxy_instance_reuse`: Valida o reuso da mesma conexão sem recriar objetos.
* `test_protection_proxy_authorized_admin`: Valida que usuários `ADMIN` possuem acesso irrestrito.
* `test_protection_proxy_blocked_access_raises_permission_error`: Valida o bloqueio de usuários `CONVIDADO` ou `OPERADOR` com `PermissionError` e log de segurança.
* `test_remote_proxy_call_forwarding`: Valida empacotamento RPC, serialização JSON e desempacotamento de telemetria remota.
* `test_remote_proxy_unsupported_operation`: Valida tratamento de erro em chamadas remotas inválidas.
* `test_logging_proxy_audit_trail_and_error_capture`: Valida histórico com data, hora, parâmetros e captura de exceções.
* `test_cached_youtube_hit_miss_and_call_economy`: Valida cache misses na 1ª chamada e cache hits nas consultas seguintes, poupando a API real.
* `test_youtube_manager_client_integration`: Valida que o cliente `YouTubeManager` consome o proxy de cache transparentemente.
* `test_smart_reference_counting_and_auto_deallocate`: Valida contagem de clientes e desalocação automática quando referências chegam a zero.
* `test_patterns_comparison_behavior`: Valida as diferenças entre Proxy, Adapter, Decorator e Facade.

---

## 7. Exemplos de Utilização via Console (Terminal)

Você também pode demonstrar os exemplos diretamente no terminal, sem abrir a interface web:

### Demonstração da Estrutura Básica:
```bash
python3 examples/basic_proxy.py
```

### Demonstração do Cache do YouTube:
```bash
python3 examples/youtube_example.py
```

---

## 8. Comparativo Entre Padrões Vizinhos

| Padrão | Interface com o Cliente | Controle de Ciclo de Vida? | Propósito Central |
| :--- | :---: | :---: | :--- |
| **🛡️ Proxy** | **Idêntica** à do serviço real | **Sim**, gerenciado pelo Proxy | Controlar acesso, aplicar cache, segurança e adiar criação (lazy init). |
| **🔌 Adapter** | **Diferente** / Convertida | Não | Traduzir uma interface incompatível para que dois sistemas conversem. |
| **🎀 Decorator** | **Mesma base**, mas estendida | Pelo **Cliente** (Composição) | Agregar novas responsabilidades dinâmicas ao objeto em camadas. |
| **🏛️ Facade** | **Nova interface simplificada** | Parcial | Esconder a complexidade de múltiplos subsistemas em uma porta de entrada única. |

---

## 9. Referências Bibliográficas

* GAMMA, Erich; HELM, Richard; JOHNSON, Ralph; VLISSIDES, John. *Padrões de Projeto: Soluções Reutilizáveis de Software Orientado a Objetos*. Porto Alegre: Bookman, 2000.
* REFACTORING GURU. *Proxy*. Disponível em: <https://refactoring.guru/pt-br/design-patterns/proxy>. Acesso em: 9 nov. 2026.
# proxy
