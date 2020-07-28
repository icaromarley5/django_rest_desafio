# django_rest_desafio


## Sobre

O projeto consiste de um CRUD de duas tabelas (Cliente e Endereco) pelo Django Admin e pela API criada com a biblioteca Django Rest Framework.

### Tabelas
#### Cliente

Atributos e restrições:
- foto (arquivo de imagem com limite máximo de 2 megas)
- nome (texto)
- sobrenome (texto)
- cpf (não pode ser repetido, formato aceito: "999.999.999-99")
- rg (não pode ser repetido, aceita qualquer texto com números, pontos e traços)
- telefone (formato aceito: "(99) 99999-9999")
- email (não pode ser repetido)

#### Endereço

Atributos e restrições:
- cliente (chave estrangeira)
- tipo (aceita os valores "Principal" ou "Secundário")
- logradouro (texto)
- bairro (texto)
- cidade (texto)
- estado (um dos estados do Brasil)
- número (inteiro positivo)

##### Restrições
- Um cliente pode ter vários endereços, mas somente um endereço é marcado como "Principal"
- Por causa da observação acima, o primeiro endereço de um cliente precisa ser marcado como "Principal"
- A combinação de (logradouro, bairro, cidade, estado e numero) em Endereço é única

#### Observações
- As remoções tanto no Django Admin quanto na API são feitas de forma lógica (soft-delete) através de um arquivamento dos dados. 
- Os registros deletados são armazenados nas tabelas equivalentes ClienteArquivo e EnderecoArquivo
- As tabelas ClienteArquivo e EnderecoArquivo podem ser acessadas a partir do Django Admin ao remover o caractere de comentário `#` nas linhas 18-20 de app.admin.py

## Instalação (terminal)

1) Clone o projeto `git clone https://github.com/icaromarley5/django_rest_desafio`
2) `cd django_rest_desafio`
3) <a href="https://www.treinaweb.com.br/blog/criando-ambientes-virtuais-para-projetos-python-com-o-virtualenv/">Crie um ambiente virtual Python<a>
4) Adicione a variável `SECRET_KEY` em variáveis de ambiente
5) Ative o ambiente virtual
6) Execute `pip install -r requirements.txt`
7) `cd challenge`
8) Execute as migrações `python manage.py migrate`
9) Crie um super usuário `python manage.py createsuperuser`
10) Para testar, inicie o servidor local `python manage.py runserver`

# URLs disponíveis para acesso:
- /admin
  - login no admin
- /api/cliente/
  - listagem e criação de clientes
- /api/cliente/id/
  - detalhes, alteração e remoção de um cliente
- /api/cliente/id/endereco/
  - listagem e criação de endereços de um cliente
- /api/cliente/id/endereco/id/
  - detalhes, alteração e remoção de um endereço de um cliente
