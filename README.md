#### Como executar a infra do projeto?

- Primeiramente instale o Docker https://www.docker.com/products/docker-desktop/
- Acesse a pasta infra
- Execute o código ```docker-compose up -d ```
- Para acompanhar o passo-a-passo da maquina subindo rode ```docker logs -t -f api```

### Plataforma Web - Como utilizar

- Rodar o site em: http://127.0.0.1:8081
- Acessar a página de login em http://127.0.0.1:8081/login.html
- Logar com os dados:
    - CNPJ: ***KEBE17609492220843***
    - Senha: ***123***
    - OBS: Qualquer cliente na base pode ser acessado com a senha "123".
- Após logado, abrir o menu lateral e clicar em "financeiro".
- Na tela das últimas solicitações, clicar em "Solicitar".
- Preencher o valor desejado, adicionar uma mensagem (opicional) e finalmente clicar em "Enviar Solicitação" para enviar a solicitação e obter o retorno da API.