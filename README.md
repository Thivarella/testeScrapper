## Rodando com e sem Docker

#### Rodando sem docker
Caso queira executar o projeto sem o docker, basta apenas realizar os passos abaixo:
> É aconselhavel realizar essas operações em um ambiente virtual, para que os acotes sejam instalados apenas para executar o projeto e não globalmente em sua máquina

    - pip/pip3 install -r requirements.txt
    e em seguida executar o comando para iniciar a aplicação
    - python/python3 run.py
    
#### Rodando com docker
Para rodar a aplicação dentro de um container, você precisará ter uma versão do docker previamente instalada em sua máquina.
Caso não possua uma instalação basta se guir o link abaixo:

[https://docs.docker.com/v17.12/install/]
     
Primeiro você deve buildar a imagem e em seguida iniciar o container
####
    docker build -t <app_name>:latest .
    Após o término da criação da imagem, basta iniciar a aplicação.
    
    docker run -p 5000:5000 --network=host <app_name>:latest
    
    O uso do --network, serve para que a aplicação enxergue o serviço do banco que está rodando localmente na máquina.
    Caso queira rodar a aplicação em background, basta executar o comando acima incluindo a opção -d
    
    docker run -p 5000:5000 -d --network=host <app_name>:latest
    
Após isso sua aplicação estará disponível.

