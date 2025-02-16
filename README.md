# Calendar Manager

## Descrição

O **Calendar Manager** é uma aplicação de gerenciamento de agenda para clínicas odontológicas. Ela permite que você registre clientes, consulte informações dos atendimentos e até exporte relatórios em PDF. O sistema é simples e intuitivo, feito com a biblioteca `Tkinter` para a interface gráfica, e utiliza SQLite como banco de dados para armazenamento local dos dados.

## Funcionalidades

- **Adicionar Cliente**: Adiciona um novo cliente à agenda, com informações como nome, CPF, telefone, data do procedimento, tipo de procedimento, local, valor e forma de pagamento.
- **Remover Cliente**: Remove um cliente da agenda a partir de seu nome completo.
- **Consultar Clientes**: Consulta todos os clientes cadastrados na agenda, com a possibilidade de filtrar os resultados por período (mês e ano).
- **Exportar Relatório**: Gera um relatório PDF com as informações dos clientes, podendo ser filtrado por período.

## Requisitos

Antes de executar o projeto, você precisa instalar as dependências:

pip install -r requirements.txt

Ou instalar as bibliotecas individualmente:

pip install sqlite3
pip install fpdf
pip install tk

Como Executar

Clone o repositório:
git clone leandroo65/Dental-Calendar-Manager

Navegue até a pasta do projeto:
cd CalendarManager

Execute o aplicativo:
python calendar_manager.py

Funcionalidades Adicionais
Gerenciamento Completo: Gerencie todos os dados de atendimento, com opções para adicionar, consultar, remover e exportar as informações de forma prática.
Exportação em PDF: Gere relatórios de atendimentos em PDF, com a opção de filtrar por mês/ano.

Tecnologias Usadas
Python: Linguagem de programação utilizada para o desenvolvimento do projeto.
Tkinter: Biblioteca utilizada para criar a interface gráfica.
SQLite3: Banco de dados utilizado para armazenar os dados da agenda.
FPDF: Biblioteca para geração de relatórios em formato PDF.

Contribuições
Contribuições são bem-vindas! Se você quiser melhorar ou adicionar novas funcionalidades ao projeto, basta seguir as etapas abaixo:
Faça um fork deste repositório.
Crie uma branch para a sua feature (git checkout -b minha-nova-feature).
Faça o commit das suas alterações (git commit -am 'Adiciona nova funcionalidade').
Envie para o repositório remoto (git push origin minha-nova-feature).
Crie um Pull Request.

Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
