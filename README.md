Introdução
    
     ->Descrição
     Este projeto é um sistema de gerenciamento de inventário desenvolvido com Python e framework Django. 
     Ele permite aos usuários gerenciar produtos, controlar o estoque e gerar relatórios. A aplicação 
     é projetada para ser facilmente extensível e configurável, utilizando tecnologias como Docker
     para facilitar o desenvolvimento e a implantação.

     -> Objetivos do projeto
     O objetivo deste projeto é finalizar e aprimorar o sistema de gerenciamento
     de inventário iniciado no período inicial da faculdade, incorporando novos conhecimentos e tecnologias
     adquiridos posteriormente. Isso inclui a implementação de funcionalidades adicionais, a otimização do desempenho e a 
     adoção de melhores práticas de desenvolvimento para garantir que o sistema seja eficiente, confiável e fácil de usar.

Próximas Etapas

     -> Documentação do código
     -> Otimização de código
     -> Implementação de testes TDD (Test Driven Development)

Tecnologias Utilizadas

     -> Python - Linguagem de programação principal.
     -> Django - Framework web.
     -> PostgreSQL - Banco de dados.
     -> Docker e Docker Compose - Contêineres para ambiente de desenvolvimento.

Pré-requisitos

     -> Linux versão 22.04 (versão utilizada no desenvolvimento)
     -> Python versão 3.10.12 (versão utilizada no desenvolvimento)
     -> Pip (gerenciador de pacotes do Python)
     -> Docker e Docker Compose

Instalação (Linux)
     
  -> Clonando o Repositório
    
    git clone git@github.com:DennerRobert/Estoque_API_Python_Django.git
    cd Estoque_API_Python_Django

  -> Configurando o Ambiente Virtual
    
    python -m venv venv
    source venv/bin/activate

  -> Instalando Dependências
   
    pip install -r requirements.txt

Configuração
    -> Variáveis de Ambiente
    Crie um arquivo .env na raiz do projeto com as seguintes configurações:
    
    POSTGRES_DB=seu_banco
    POSTGRES_USER=seu_usuario
    POSTGRES_PASSWORD=sua_senha

    POSTGRES_HOST=localhost

    DEBUG=False
    DATABASE_URL=postgres://seu_usuario:sua_senha@localhost:5432/seu_banco

Scripts (Inserção e Exclusão de dados)
  
  -> Adicionar dados
      
    python3 add_product.py
  
  -> Remover dados
    
    python3 clear_data.py
  
Executando o Projeto (Linux)

  -> Configurando o Banco de Dados

    python manage.py makemigrations
    python manage.py migrate

  -> Criando Superusuário
    
    python manage.py createsuperuser

  -> Coletando Arquivos Estáticos
    
    python manage.py collectstatic

  -> Servidor de Desenvolvimento

    python manage.py runserver

  -> Acessando o Projeto

    O projeto estará acessível em http://localhost:8000/ .Abra seu navegador e acesse essa URL para ver a aplicação em funcionamento.


Instalação (Docker)
     
  -> Clonando o Repositório
    
    git clone git@github.com:DennerRobert/Estoque_API_Python_Django.git
    cd Estoque_API_Python_Django

Configuração (Docker)
    -> Variáveis de Ambiente
    Crie um arquivo .env na raiz do projeto com as seguintes configurações:
    
    POSTGRES_DB=seu_banco
    POSTGRES_USER=seu_usuario
    POSTGRES_PASSWORD=sua_senha

    POSTGRES_HOST=db

    DEBUG=False
    DATABASE_URL=postgres://seu_usuario:sua_senha@db:5432/seu_banco
  
Executando o Projeto (Docker)

  -> Construindo e Inicializando os Contêineres

    docker-compose up --build

  -> Acessando o Projeto (Docker)

    O projeto estará acessível em http://localhost:8000/ .Abra seu navegador e acesse essa URL para ver a aplicação em funcionamento.
    Usuário é criado automaticamente!
    User: Admin
    Pass: Adminpass

Licença

    -> Este projeto está licenciado sob a Licença GNU GENERAL PUBLIC LICENSE - veja o arquivo LICENSE para mais detalhes.

