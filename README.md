# Faculends

Sistema web para controle de empréstimo de materiais, equipamentos e máquinas de uma instituição de ensino. Projeto desenvolvido para a disciplina de Análise e Projeto de Sistemas.

O usuário consulta o catálogo, solicita um material, e o responsável aprova ou rejeita o pedido e registra a retirada e a devolução. A disponibilidade de cada material é atualizada automaticamente.

## Funcionalidades

- **Catálogo:** lista de materiais com nome, descrição, categoria e quantidade disponível, com selo de disponibilidade.
- **Pesquisa e filtro:** busca por nome ou descrição e filtro por categoria, que podem ser combinados.
- **Solicitação de empréstimo:** formulário com nome do solicitante, com validação dos dados.
- **Lista de solicitações:** consulta dos pedidos e do status de cada um, com selos coloridos.
- **Área do responsável (`/admin`):** aprovar ou rejeitar pedidos pendentes e registrar retirada e devolução.
- **Controle de disponibilidade:** a quantidade disponível diminui na retirada e aumenta na devolução.
- **Persistência:** os dados ficam salvos em um banco SQLite e não se perdem ao reiniciar a aplicação.

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python 3 | Linguagem do servidor |
| Flask | Framework web (rotas, templates, mensagens) |
| SQLite | Banco de dados em arquivo, sem necessidade de instalar um servidor |
| HTML e CSS | Páginas e estilo da interface |
| Jinja2 | Templates HTML (já incluído no Flask) |
| Git e GitHub | Versionamento do código |

## Estrutura do projeto

```
Faculends/
├── app.py              # Rotas e regras de negócio
├── database.py         # Conexão com o banco, criação das tabelas e dados de exemplo
├── requirements.txt    # Dependências do projeto
├── templates/
│   ├── base.html           # Layout comum (cabeçalho, menu e rodapé)
│   ├── catalogo.html       # Catálogo com pesquisa e filtro
│   ├── solicitar.html      # Formulário de solicitação
│   ├── solicitacoes.html   # Lista de solicitações e status
│   └── admin.html          # Área do responsável
└── static/
    └── css/
        └── style.css       # Estilos
```

O arquivo `faculends.db` é criado automaticamente na primeira execução e não é versionado.

## Como instalar e executar

Pré-requisitos: [Python 3](https://www.python.org/downloads/) e [Git](https://git-scm.com/) instalados.

```bash
# 1. Baixar o projeto
git clone https://github.com/TRexExtreme/Faculends.git
cd Faculends

# 2. Criar o ambiente virtual
python -m venv venv

# 3. Ativar o ambiente virtual
#    Windows (PowerShell):
venv\Scripts\activate
#    Linux/Mac:
source venv/bin/activate

# 4. Instalar as dependências
pip install -r requirements.txt

# 5. Executar
python app.py
```

Acesse **http://127.0.0.1:5000** no navegador. Para parar o servidor, use `Ctrl + C`.

No Windows, se o PowerShell bloquear a ativação do ambiente virtual, execute uma vez:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Como usar

1. Abra o **Catálogo** e pesquise ou filtre os materiais.
2. Clique em **Solicitar** em um material disponível, informe seu nome e envie.
3. Acompanhe o pedido em **Solicitações** (status *pendente*).
4. No menu **Responsável** (`/admin`), o responsável aprova ou rejeita o pedido.
5. Para um pedido aprovado, o responsável registra a **retirada** (a disponibilidade diminui) e depois a **devolução** (a disponibilidade volta).

## Rotas

| Rota | Método | Função |
|---|---|---|
| `/` e `/catalogo` | GET | Catálogo com pesquisa (`?busca=`) e filtro (`?categoria=`) |
| `/solicitar/<id>` | GET, POST | Formulário e registro de solicitação |
| `/solicitacoes` | GET | Lista de solicitações e status |
| `/admin` | GET | Área do responsável |
| `/admin/solicitacao/<id>/aprovar` | POST | Aprova um pedido pendente |
| `/admin/solicitacao/<id>/rejeitar` | POST | Rejeita um pedido pendente |
| `/admin/solicitacao/<id>/retirar` | POST | Registra a retirada de um pedido aprovado |
| `/admin/solicitacao/<id>/devolver` | POST | Registra a devolução de um material retirado |

## Banco de dados

**materiais:** `id`, `nome`, `descricao`, `categoria`, `quantidade_total`, `quantidade_disponivel`

**solicitacoes:** `id`, `material_id` (chave estrangeira para materiais), `solicitante`, `data_solicitacao`, `status`

## Regras de negócio

- O nome do solicitante é obrigatório e deve ter entre 3 e 80 caracteres.
- Não é possível solicitar um material sem unidades disponíveis.
- Um pedido novo começa com o status **pendente**.
- Fluxo de status: `pendente` → `aprovada` ou `rejeitada`; `aprovada` → `retirada` → `devolvida`.
- Só pedidos pendentes podem ser aprovados ou rejeitados.
- Só pedidos aprovados podem ter a retirada registrada, e só pedidos retirados podem ser devolvidos.
- A quantidade disponível diminui na **retirada** (e não na solicitação nem na aprovação) e aumenta na **devolução**. Se não houver unidade disponível no momento da retirada, a operação é bloqueada.
- As consultas ao banco usam parâmetros, o que evita SQL injection.

## Limitações da versão atual

- **Não há autenticação:** a rota `/admin` é aberta e não deve ser usada em produção. O sistema não possui login nem contas de usuário; o solicitante apenas informa o nome.
- Não há cadastro, edição ou exclusão de materiais pela interface; os materiais vêm dos dados de exemplo.
- O histórico guarda a data da solicitação e o status atual, mas não registra data e hora da aprovação, da retirada e da devolução.
- Não há controle de prazo nem de atrasos, multas ou notificações.
- A chave secreta do Flask (usada nas mensagens da interface) está no código e o modo `debug` está ligado. Isso é adequado apenas para desenvolvimento.
- Cada solicitação trata de uma unidade do material.

## Integrantes e divisão do trabalho

| Integrante | Commits |
|---|---|
| [@TRexExtreme](https://github.com/TRexExtreme) | Estrutura do projeto, banco de dados, catálogo, pesquisa e filtro, README |
| [@matheusmendoncadefranca-eng](https://github.com/matheusmendoncadefranca-eng) | Solicitações, formulário com validação, lista de pedidos, área do responsável, retirada e devolução |