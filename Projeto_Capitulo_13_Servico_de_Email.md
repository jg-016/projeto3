# Projeto – Capítulo 13: Serviços de E-mail

## Objetivo do trabalho

O objetivo é implementar no sistema Django um mecanismo de recuperação de senha por e-mail. Quando o usuário esquecer sua senha, deverá conseguir solicitar a redefinição, receber uma mensagem com um link individual, acessar esse link e cadastrar uma nova senha.

O fluxo geral será:

1. O usuário acessa a tela de login e seleciona **Esqueci minha senha**.
2. Informa o endereço de e-mail associado à conta.
3. O sistema valida os dados e identifica a conta correspondente.
4. O sistema gera um token seguro para a recuperação.
5. Uma mensagem é enviada ao usuário com um link que contém o token.
6. O usuário acessa o link.
7. O sistema verifica se o token é válido e ainda está dentro do prazo.
8. O usuário informa e confirma a nova senha.
9. O sistema salva a nova senha e invalida o token.
10. O usuário consegue entrar com a nova senha.

O trabalho envolve formulários, views, rotas, templates HTML, configuração de SMTP, geração e validação de tokens e testes.

---

# 1. Explicação do Capítulo 13

O Capítulo 13, intitulado **Serviços de E-mail**, apresenta a implementação de recuperação de senha utilizando o serviço de e-mail do próprio Django. O capítulo está organizado em duas partes:

- **13.1 – View de recuperação de senha:** criação do formulário, da view, da URL e da opção de recuperação na tela de login.
- **13.2 – Configurando o serviço de e-mail:** configuração do provedor de e-mail, implementação do envio da mensagem e criação do link de recuperação.

## 1.1. Formulário de recuperação de senha

No projeto do livro, o formulário é criado em `medicSearch/forms/AuthForm.py`, por meio da classe `RecoveryForm`.

Exemplo apresentado:

```python
class RecoveryForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
```

O formulário possui um campo obrigatório para o e-mail. O widget `EmailInput` cria um campo apropriado para endereços eletrônicos, enquanto `form-control` aplica a classe de estilização do Bootstrap.

A função desse formulário é receber e validar o endereço informado. Ele não altera a senha.

## 1.2. View de recuperação

No livro, a view `recovery_view` fica em `medicSearch/views/AuthView.py`.

A view é responsável por:

1. Criar o formulário.
2. Identificar se a requisição foi enviada pelo método POST.
3. Validar os dados.
4. Consultar o banco de dados para localizar o perfil associado ao e-mail.
5. Chamar a função de envio de e-mail quando o perfil existe.
6. Preparar uma mensagem de sucesso ou erro.
7. Renderizar o template de autenticação com o contexto necessário.

O exemplo do livro procura o perfil com uma consulta semelhante a:

```python
profile = Profile.objects.filter(user__email=email).first()
```

`Profile.objects` acessa os registros do modelo; `filter()` aplica o filtro; `user__email` consulta o e-mail do usuário relacionado; e `first()` retorna o primeiro resultado ou `None`.

O livro apresenta mensagens para envio bem-sucedido, falha no envio, e-mail inexistente e formulário inválido. Para um sistema em produção, é mais seguro não revelar se um e-mail está cadastrado. Pode-se apresentar uma mensagem genérica informando que, caso exista uma conta associada ao endereço, as instruções serão enviadas.

## 1.3. Rotas de recuperação

No arquivo `medicSearch/urls/AuthUrls.py`, o livro adiciona uma rota semelhante a:

```python
path("recovery", recovery_view, name="recovery")
```

- `recovery` é o caminho acessado pelo navegador.
- `recovery_view` é a função executada.
- `name="recovery"` é o nome usado para referenciar a rota nos templates.

## 1.4. Alteração do template de autenticação

O livro reutiliza `auth.html` para diferentes telas de autenticação. Quando o título da página é `Login`, o template apresenta o link **Esqueci minha senha**, apontando para a rota de recuperação.

O capítulo também orienta ocultar os links de autenticação por redes sociais nas páginas de recuperação e alteração de senha, pois esses recursos não são necessários nessas telas.

A ideia é reaproveitar o template e controlar título, texto do botão, links e formulário por meio do contexto enviado pela view.

## 1.5. O que é SMTP?

SMTP significa *Simple Mail Transfer Protocol*. É o protocolo utilizado para transmitir mensagens de e-mail.

O Django pode utilizar um servidor SMTP de um provedor, autenticar-se nele e enviar mensagens aos destinatários. O fluxo básico é:

**Sistema Django → servidor SMTP → caixa de entrada do usuário.**

O Django disponibiliza ferramentas de envio no módulo `django.core.mail`.

## 1.6. Configuração do serviço de e-mail

O livro utiliza o Gmail como exemplo e apresenta configurações semelhantes a estas no arquivo de configuração do Django:

```python
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "seuemail@gmail.com"
EMAIL_HOST_PASSWORD = "sua senha"
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = False
```

Significado das configurações:

| Configuração | Função |
|---|---|
| `EMAIL_USE_TLS` | Indica se a conexão utilizará TLS. |
| `EMAIL_HOST` | Endereço do servidor SMTP. |
| `EMAIL_HOST_USER` | Conta utilizada para autenticar o envio. |
| `EMAIL_HOST_PASSWORD` | Credencial utilizada na autenticação. |
| `EMAIL_PORT` | Porta de comunicação do servidor. |
| `DEFAULT_FROM_EMAIL` | Remetente padrão das mensagens. |
| `EMAIL_USE_SSL` | Indica se será utilizado SSL implícito. |

No exemplo tradicional do Gmail, utiliza-se `smtp.gmail.com`, porta `587`, TLS habilitado e SSL implícito desabilitado.

**Atenção à atualização do Gmail:** o capítulo mostra a opção antiga de “acesso a aplicativos menos seguros”. Essa orientação está desatualizada e não deve ser seguida. A autenticação deve utilizar um método atualmente aceito pelo provedor, como senha de aplicativo quando disponível ou OAuth 2.0. As credenciais devem ficar em variáveis de ambiente ou em arquivo local protegido, nunca diretamente no repositório.

## 1.7. Função de envio de e-mail

O capítulo utiliza as seguintes importações:

```python
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import hashlib
```

Função de cada recurso:

- `settings`: permite acessar as configurações do Django.
- `send_mail`: realiza o envio da mensagem.
- `render_to_string`: carrega um template e transforma seu conteúdo em uma string.
- `strip_tags`: remove as tags HTML, gerando uma versão em texto simples.
- `hashlib`: biblioteca utilizada no exemplo do livro para gerar um hash.

A função `send_email(profile)` do livro realiza estas operações:

1. Gera um valor para o token.
2. Armazena o token no perfil e salva o registro.
3. Renderiza o template HTML do e-mail com o token.
4. Cria uma versão em texto simples.
5. Envia a mensagem para o e-mail do usuário.

O envio utiliza parâmetros como:

| Parâmetro | Significado |
|---|---|
| `subject` | Assunto da mensagem. |
| `message` | Corpo em texto simples. |
| `html_message` | Corpo formatado em HTML. |
| `from_email` | Remetente. |
| `recipient_list` | Lista de destinatários. |
| `fail_silently` | Define se erros de envio serão ocultados. |

O livro utiliza `fail_silently=False`, permitindo que falhas no envio sejam identificadas.

**Melhoria técnica necessária:** o exemplo impresso usa `hashlib.sha256().hexdigest()` sem fornecer dados de entrada. Assim, o resultado não funciona como um token exclusivo por solicitação. Para uma implementação manual, deve-se gerar um valor aleatório e imprevisível, por exemplo com `secrets.token_urlsafe(32)`, e controlar sua expiração e uso único. Outra possibilidade é utilizar o mecanismo nativo de redefinição de senha do Django.

## 1.8. Template do e-mail

O livro cria `medicSearch/templates/auth/recovery.html`. Esse template contém a mensagem de recuperação e um link que inclui a variável `{{ token }}`.

Quando o template é renderizado, o Django substitui a variável pelo token real do usuário. O link enviado permite que o usuário abra a página de redefinição.

O livro utiliza um endereço `localhost:8000` como exemplo. Esse endereço serve apenas para testes locais. Em produção, o link deve utilizar o domínio real da aplicação e HTTPS.

E-mails HTML devem ser simples e compatíveis com diferentes clientes de e-mail. Por isso, estilos inline costumam ser mais confiáveis do que depender de folhas CSS externas.

## 1.9. Formulário de alteração de senha

O livro cria a classe `ChangePasswordForm`, com um campo de senha que utiliza `PasswordInput`.

A função desse formulário é receber a nova senha sem exibir os caracteres digitados.

Para uma implementação mais completa, o formulário deve possuir também um campo de confirmação e validar se os dois valores são iguais. A senha deve passar pelos validadores configurados no Django.

## 1.10. View de alteração de senha

A view `change_password(request, token)` recebe a requisição e o token que veio na URL.

O funcionamento esperado é:

1. Procurar o token no armazenamento.
2. Verificar se ele existe e ainda é válido.
3. Identificar o usuário associado.
4. Exibir o formulário de nova senha.
5. Validar os dados enviados.
6. Salvar a nova senha utilizando `set_password()`.
7. Invalidar o token para impedir reutilização.
8. Informar o resultado da operação.

O método `set_password()` é importante porque aplica o mecanismo de hash de senhas do Django. Não se deve salvar a senha diretamente em texto puro.

## 1.11. URL de alteração de senha

O livro apresenta uma rota com parâmetro dinâmico para receber o token, semelhante a:

```python
path(
    "change-password/<str:token>",
    change_password,
    name="change-password"
)
```

O trecho `<str:token>` indica que parte do caminho será recebida como parâmetro pela view.

Exemplo ilustrativo:

```text
/change-password/abc123
```

O valor `abc123` seria recebido como token pela função responsável pela redefinição.

---

# 2. Adaptação ao projeto 2026-CAP

O livro utiliza uma estrutura chamada `medicSearch`, com um modelo `Profile` relacionado ao usuário. O projeto 2026-CAP já possui uma aplicação de usuários e um modelo próprio chamado `Usuario`.

Portanto, não se deve copiar os arquivos e nomes do livro sem adaptação. A recuperação deve utilizar o modelo de usuário já existente e respeitar a organização atual do projeto.

## 2.1. Diferenças entre o livro e o projeto

| Livro | Projeto 2026-CAP |
|---|---|
| `medicSearch` | `apps.usuarios` |
| `AuthForm.py` | Estrutura de formulários existente em usuários |
| `AuthView.py` | Views de autenticação existentes |
| `AuthUrls.py` | Arquivo de URLs da aplicação |
| `Profile` | Modelo `Usuario` |
| `profile.user.email` | Campo de e-mail do usuário |
| `profile.token` | Campo que ainda precisa ser definido ou substituído por mecanismo próprio |
| `auth/auth.html` | Templates de autenticação do projeto |

A implementação não deve criar outro modelo de usuário nem uma tabela `Profile` apenas para reproduzir o tutorial.

## 2.2. Arquivos que provavelmente precisarão ser criados ou modificados

Os caminhos exatos devem ser confirmados na árvore atual do repositório antes de começar.

| Arquivo ou área | Ação | Responsabilidade |
|---|---|---|
| Formulários de `apps/usuarios` | Modificar/criar | Formulário de solicitação e formulário de nova senha. |
| Views de autenticação | Modificar | Solicitação, envio e redefinição. |
| URLs de usuários | Modificar | Rotas de recuperação e redefinição. |
| Templates de usuários | Criar | Telas de recuperação e nova senha. |
| Template de login | Modificar | Link “Esqueci minha senha”. |
| Configurações Django | Modificar | Backend SMTP e remetente. |
| Arquivo `.env` | Criar/modificar | Credenciais de e-mail protegidas. |
| Modelo ou mecanismo de token | Definir | Associação do token ao usuário, validade e uso único. |

## 2.3. Estratégia de armazenamento do token

Existem duas opções principais. A equipe deve escolher uma delas antes de implementar para evitar soluções duplicadas.

### Opção A – Modelo próprio de recuperação

Criar um modelo específico, por exemplo `TokenRecuperacaoSenha`, com campos como:

| Campo | Tipo sugerido | Finalidade |
|---|---|---|
| `usuario` | ForeignKey | Identifica o usuário. |
| `token_hash` | CharField | Armazena o hash do token. |
| `criado_em` | DateTimeField | Registra a criação. |
| `expira_em` | DateTimeField | Define a expiração. |
| `utilizado_em` | DateTimeField, opcional | Registra o uso. |

Essa opção permite controlar tokens, prazos e solicitações individualmente.

### Opção B – Mecanismos nativos do Django

O Django oferece ferramentas próprias, como `PasswordResetTokenGenerator`, `PasswordResetView` e `PasswordResetConfirmView`. Elas permitem implementar a redefinição sem reproduzir manualmente toda a lógica do livro.

A equipe deve verificar se o professor exige a implementação manual do token. Se não exigir, os mecanismos nativos são uma alternativa adequada. Não é necessário manter as duas soluções simultaneamente.

## 2.4. Requisitos de segurança

- Cada solicitação deve gerar um token imprevisível.
- O token deve possuir prazo de validade.
- O token deve ser invalidado após o uso.
- A senha deve ser salva por meio dos mecanismos seguros do Django.
- A nova senha deve ser confirmada.
- As credenciais SMTP não podem ser versionadas no Git.
- O sistema não deve revelar se determinado e-mail está cadastrado.
- Deve haver proteção contra solicitações excessivas.
- Em produção, os links devem utilizar HTTPS.

---

# 3. Divisão do trabalho entre quatro pessoas

A divisão abaixo separa o desenvolvimento em quatro frentes: solicitação da recuperação, serviço de e-mail, redefinição da senha e interface/integração/testes.

## Pessoa 1 – Recuperação de senha

**Responsabilidade:** desenvolver a funcionalidade que permite ao usuário solicitar a recuperação da senha.

### Atividades

1. Criar o formulário `RecoveryForm`, com o campo de e-mail.
2. Validar se o e-mail foi preenchido corretamente.
3. Criar a view de solicitação de recuperação.
4. Consultar o banco de dados para localizar o usuário pelo e-mail.
5. Preparar mensagens de retorno.
6. Criar a URL de recuperação.
7. Adicionar o link “Esqueci minha senha” na tela de login.
8. Integrar a view com a função de envio de e-mail definida pela Pessoa 2.

### Arquivos envolvidos

- Formulários de autenticação.
- Views de autenticação.
- Arquivo de URLs.
- Template de login.

### Resultado esperado

O usuário consegue acessar a tela de recuperação, informar seu e-mail e solicitar a redefinição da senha.

**Referência no capítulo:** páginas 264–267.

## Pessoa 2 – Configuração e envio de e-mails

**Responsabilidade:** configurar o serviço de e-mail e implementar o envio da mensagem de recuperação.

### Atividades

1. Definir o provedor de e-mail que será utilizado.
2. Configurar o serviço SMTP.
3. Adicionar as configurações necessárias ao Django.
4. Armazenar as credenciais de maneira segura.
5. Implementar a função de envio de e-mail.
6. Definir a estratégia de geração e armazenamento do token em conjunto com a Pessoa 3.
7. Criar o template HTML do e-mail.
8. Inserir no e-mail o link com o token.
9. Testar se a mensagem chega ao destinatário.

### Arquivos envolvidos

- Configurações do Django.
- Serviço/função de envio de e-mail.
- Template HTML do e-mail.
- Arquivo de variáveis de ambiente.

### Resultado esperado

Ao solicitar a recuperação, o usuário recebe um e-mail contendo o link para redefinir sua senha.

**Referência no capítulo:** páginas 268–276.

## Pessoa 3 – Alteração da senha

**Responsabilidade:** desenvolver a funcionalidade que permite cadastrar uma nova senha utilizando o token recebido por e-mail.

### Atividades

1. Criar o formulário de alteração de senha.
2. Adicionar os campos de nova senha e confirmação.
3. Criar a view de redefinição.
4. Receber o token pela URL.
5. Verificar se o token existe, é válido e não expirou.
6. Permitir a alteração da senha.
7. Salvar a senha utilizando o mecanismo seguro do Django.
8. Invalidar o token após a utilização.
9. Criar a URL de redefinição.
10. Apresentar mensagens de sucesso e erro.

### Arquivos envolvidos

- Formulários de autenticação.
- Views de autenticação.
- Arquivo de URLs.
- Template de alteração de senha.
- Modelo ou mecanismo de token, caso seja adotado.

### Resultado esperado

O usuário consegue acessar o link recebido, cadastrar uma nova senha e utilizar essa senha para entrar no sistema.

**Referência no capítulo:** parte de redefinição de senha do capítulo.

## Pessoa 4 – Interface, integração e testes

**Responsabilidade:** adaptar as interfaces ao projeto, integrar as funcionalidades desenvolvidas pelos demais integrantes e verificar o funcionamento completo.

### Atividades

1. Analisar a estrutura atual do projeto.
2. Adaptar os templates de recuperação de senha.
3. Desenvolver a interface de redefinição de senha.
4. Manter o padrão visual das páginas existentes.
5. Integrar as views e URLs desenvolvidas pelas outras pessoas.
6. Verificar a comunicação entre formulários e views.
7. Testar a solicitação e o recebimento do e-mail.
8. Testar tokens inválidos, expirados e reutilizados.
9. Testar a alteração efetiva da senha e o novo login.
10. Corrigir problemas de integração e documentar a implementação.

### Arquivos envolvidos

- Templates HTML.
- Arquivos CSS.
- Arquivos de URLs e integração, quando necessário.
- Configurações de testes e documentação.

### Resultado esperado

Todas as partes funcionam juntas, com interfaces adequadas e o fluxo de recuperação de senha completo.

**Referência:** integração das funcionalidades do capítulo e requisitos complementares de segurança.

---

# 4. Como as quatro partes se conectam

O fluxo de trabalho entre os integrantes será:

1. **Pessoa 1 – Solicitação:** recebe o e-mail informado pelo usuário, valida os dados e inicia a recuperação.
2. **Pessoa 2 – Envio:** gera ou utiliza o token definido em conjunto, prepara a mensagem e envia o link.
3. **Pessoa 3 – Redefinição:** recebe o token pelo link, valida sua autenticidade e permite cadastrar a nova senha.
4. **Pessoa 4 – Integração:** conecta as telas e funcionalidades, testa o processo completo e corrige problemas.

## 4.1. Cuidados para evitar conflitos

- Pessoa 1 e Pessoa 3 trabalharão em áreas que podem envolver os mesmos arquivos de formulários, views e URLs. Devem combinar previamente quais funções e rotas cada uma adicionará.
- Pessoa 2 ficará responsável pela função de envio. A Pessoa 1 deverá utilizar a interface definida para essa função.
- Pessoa 2 e Pessoa 3 devem combinar o formato do token, onde ele será armazenado e como será validado.
- Pessoa 4 deverá manter contato com todos para garantir que os templates utilizem os nomes e as variáveis esperados pelas views.
- Cada integrante deve trabalhar em uma branch própria e integrar suas alterações por Pull Request.
- Antes da integração, todos devem informar quais arquivos foram modificados e quais dependências sua parte possui.

---

# 5. Checklist de implementação e testes

## Funcionalidades

- [ ] O link “Esqueci minha senha” aparece na tela de login.
- [ ] A tela de recuperação recebe o e-mail.
- [ ] O formulário valida o endereço informado.
- [ ] A solicitação de recuperação é processada.
- [ ] O sistema gera um token seguro.
- [ ] O token fica associado ao usuário correto.
- [ ] O e-mail é enviado.
- [ ] A mensagem contém o link correto.
- [ ] O link abre a página de redefinição.
- [ ] O sistema valida o token.
- [ ] Tokens inexistentes são rejeitados.
- [ ] Tokens expirados são rejeitados.
- [ ] A confirmação da senha é validada.
- [ ] A nova senha passa pelos validadores do Django.
- [ ] A nova senha é salva corretamente.
- [ ] O token é invalidado após o uso.
- [ ] O link não pode ser reutilizado.
- [ ] O usuário consegue entrar com a nova senha.
- [ ] A senha antiga deixa de funcionar.

## Ordem recomendada de desenvolvimento

| Ordem | Atividade | Responsável principal |
|---|---|---|
| 1 | Analisar a estrutura atual e combinar contratos entre partes | Todos |
| 2 | Definir a estratégia de tokens | Pessoas 2 e 3 |
| 3 | Criar o formulário e a view de solicitação | Pessoa 1 |
| 4 | Configurar SMTP e implementar envio | Pessoa 2 |
| 5 | Criar formulário e view de redefinição | Pessoa 3 |
| 6 | Criar/adaptar templates e interfaces | Pessoa 4 |
| 7 | Integrar rotas e funcionalidades | Todos, com coordenação da Pessoa 4 |
| 8 | Executar testes completos | Todos, com coordenação da Pessoa 4 |

---

# 6. Resultado final esperado

Ao concluir o trabalho, o sistema deverá permitir que um usuário que esqueceu sua senha recupere o acesso de maneira independente e segura.

O processo começa na tela de login, passa pela solicitação de recuperação e pelo envio de um e-mail com um link individual, continua com a validação do token e termina com o cadastro de uma nova senha. Após a redefinição, o token deve deixar de funcionar e o usuário deve conseguir entrar utilizando a nova senha.

A divisão proposta distribui o desenvolvimento entre quatro pessoas:

| Integrante | Área principal | Entrega |
|---|---|---|
| Pessoa 1 | Recuperação | Solicitação de recuperação |
| Pessoa 2 | Serviço de e-mail | Envio da mensagem com token |
| Pessoa 3 | Redefinição | Alteração segura da senha |
| Pessoa 4 | Interface e integração | Sistema completo integrado e testado |

**Importante:** o PDF enviado apresenta o Capítulo 13 do tutorial, não um enunciado independente com todos os critérios de avaliação do professor. A divisão e os requisitos complementares de segurança deste documento são uma organização proposta para executar o projeto no Django 2026-CAP.

## Referências

- PDF fornecido: *Capítulo 13 – Configurando o Serviço de E-mail*, especialmente a seção 13.1 (páginas 264–267) e a seção 13.2 (a partir da página 268).
- [Documentação oficial do Django – Envio de e-mails](https://docs.djangoproject.com/en/6.0/topics/email/).
- [Documentação oficial do Django – Redefinição de senha](https://docs.djangoproject.com/en/6.0/topics/auth/default/#all-authentication-views).
- [Google – Fazer login com senhas de app](https://support.google.com/accounts/answer/185833).
