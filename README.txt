CINEMAX_2010

Terceiro trabalho de Sistemas Operacionais 2010/2
DCC/UFRJ, professor Antonio Carlos Gay Thomé

Autores:
  Denilson Figueiredo de Sá
  Pedro Henrique Conilh de Beyssac
  Renato Signoretti


Conteúdo deste arquivo README.txt:

.. Objetivo
.. Como rodar o trabalho
.. Abordagem
.. dbserver
.... Arquitetura do dbserver
.... Protocolo de comunicação com o dbserver
.. webserver
.... Arquitetura do webserver


== Objetivo ==

O objetivo deste trabalho é implementar um sistema web de venda de ingressos
de cinema, e com isso mostrar o conhecimento de threads, semáforos,
sincronização e exclusão mútua.


== Como rodar o trabalho ==

Para rodar o trabalho, basta executar o script "run.py". Esse script irá
automaticamente inicar o "dbserver" e o "webserver".

Para conseguir rodar o trabalho, é necessário ter o seguinte software na
máquina:

* Java Runtime Environment
   Testado na versão 1.6
* Python 2.x
   Testado na versão 2.6, deve funcionar na 2.7, mas não vai funcionar na 3.x


== Abordagem ==

Quando se cria um sistema web moderno, o programador não precisa implementar
threads nem semáforos, pois tanto o servidor web (por exemplo, o Apache)
quanto o servidor de banco dados (por exemplo, MySQL ou Postgres) já possuem
uma estrutura de threads e/ou processos implementada e altamente confiável. O
programador web precisa apenas escrever o código que será executado em uma
thread do servidor web e que fará acesso ao banco dados.

Portanto, usando tecnologias modernas de desenvolvimento para web, não seria
possível utilizar threads explicitamente. Desta forma, resolvemos implementar
um banco de dados próprio para aplicar os conhecimentos desejados.


== dbserver ==

O nosso servidor de banco de dados é bastante simplificado e também limitado.
Não é nosso objetivo criar algo do nível de qualidade de um servidor
profissional, como MySQL ou Postgres.

O "dbserver", como foi chamado o nosso servidor de banco de dados, não segue o
modelo relacional, e portanto poderia ser enquadrado numa classe de banco de
dados chamada NoSQL. Na verdade, o "dbserver" está mais próximo de um banco de
dados orientado a documentos.

O "dbserver" foi escrito em Java, e está disponível dentro do diretório
"dbserver/". É possível compilar o código digitando "make" dentro desse
diretório. É possível apagar os arquivos compilados digitando "make clean". É
possível rodar o "dbserver" digitando "make run".


=== Arquitetura do dbserver ===

Ao ser executado, é iniciada uma thread principal (ListenerThread) que fica
esperando por conexões TCP na porta 1234. É iniciada uma nova thread
(WorkerThread) para tratar cada conexão recebida.

Cada "WorkerThread" recebe comandos do cliente e retorna respostas, acessando
acessando arquivos *.data dentro do diretório "data/".

Bancos de dados profissionais fazem exclusão mútua travando apenas uma tabela,
ou então apenas uma linha de uma tabela, durante a execução de certos comandos
(leituras ou escritas). Implementar um banco dados com tamanha flexibilidade
de performance requer um esforço muito grande, e está fora do escopo deste
trabalho de faculdade.

Portanto, no "dbserver" a exclusão mútua é feita através de um único semáforo
global, o qual pode ser adquirido ou liberado pelo cliente. Cabe ao cliente
conectado ao "dbserver" requerer o semáforo antes de alguma operação crítica,
como, por exemplo, uma escrita.


=== Protocolo de comunicação com o dbserver ===

Uma vez estabelecida uma conexão, o "dbserver" aceita 4 comandos: GET, PUT,
ACQUIRE, RELEASE.

"GET nome" faz o "dbserver" ler um arquivo "nome.data" dentro do diretório
"data/" e enviar o conteúdo desse arquivo para o cliente. O término do arquivo
é sinalizado por uma linha contendo apenas "###".

"PUT nome" faz o contrário: o "dbserver" salva no arquivo "nome.data" o
conteúdo enviado pelo cliente. Novamente, o final dos dados é sinalizado por
uma linha contendo apenas "###".

"ACQUIRE" e "RELEASE" servem para requisitar e liberar o semáforo global do
"dbserver". Esse semáforo deve ser usado pelo cliente para realizar operações
críticas, ou seja, quando for atualizar ou guardar dados no "dbserver" e
houver risco de condições de corrida.

O "dbserver" é inteligente o suficiente para liberar automaticamente o
semáforo caso a conexão seja fechada sem receber o comando "RELEASE".


== webserver ==

A interface web e toda a lógica de negócio ficam dentro do "webserver", o qual
foi escrito em Python 2.6 usando o framework "web.py" versão 0.34. Para
executar o servidor web, basta ter um interpretador de Python 2.x instalado e
executar o arquivo "webserver.py". Uma vez rodando, basta acessar o endereço
http://127.0.0.1:8080/ a partir de um browser.


=== Arquitetura do webserver ===

A implementação do "webserver" segue o modelo MVC (Model-View-Controller).

O arquivo "models.py" contém os modelos de negócio (ou seja, a camada
"Model").

O diretório "templates/" contém as interfaces com o usuário (ou seja, a camada
"View").

O arquivo "webserver.py" contém toda a lógica do negócio (ou seja, a camada
"Controller"). Ele contém o código para tratamento de cada requisição do
usuário, assim como o mapeamento de URLs para esse código.

Além disso, o arquivo "persistence.py" contém o código para acesso ao
"dbserver", que é a camada de persistência de dados.

Por fim, arquivos estáticos (imagens, estilos CSS, códigos JavaScript) ficam
no diretório "static/".

O código do framework "web.py" está dentro do diretório "web/".
