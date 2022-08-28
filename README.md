# turing-webscrapingclima
Projeto para entrada na área de ciência de dados do Grupo Turing. Consiste na raspagem e no armazenamento de dados relacionados ao clima de diferentes regiões ao longo do tempo. 

## Como rodar o projeto
1. Crie uma virtualenv: `virtualenv env`
1. Instale as dependências: `pip install -r requirements.txt`
1. Rode o notebook e seja feliz

## Como raspar dados de locais diferentes?
Nós raspamos e armazenamos previsões do tempo do site ClimaTempo. O projeto foi construído de maneira a ser genérico e funcionar com qualquer cidade que possua as informações no site. Para adicionar um local à raspagem do projeto, faça o seguinte:

1. Vá até o site ClimaTempo e pesquise pela cidade que você quer adicionar
1. Acesse a página dela e clique no botão *15 DIAS*
1. Copie o link da página de *15 DIAS* da cidade
1. Na pasta do projeto, abra o arquivo _locais.csv_ localizado na pasta _data_
1. Acrescente uma nova linha no arquivo, onde a primeira coluna é o nome da cidade e a segunda coluna é o link que você copiou no passo 3.
1. Rode todas as células do arquivo _.ipynb_ *em sequência*.

_Obs: Só adicionar o local ao arquivo CSV não é o suficiente para fazer o notebook passar a buscar informações dele! O projeto na verdade pega as informações dos locais armazenados na tabela *local* do banco de dados. No notebook, há uma célula responsável por carregar no banco o que estiver no arquivo. Essa célula precisa ser executada para que seu local passe a ser raspado!_ 
