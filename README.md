## Inicialização da api:
- Clonar o projeto em um diretório local
  - `git clone `
  
- Criar ambiente virtual
  - `python -m venv nome_do_ambiente`
  
- Ativando o ambiente virtual (no Windows)
  - `nome_do_ambiente\Scripts\activate`
  
- Ativando o ambiente virtual (no Linux/Mac)
  - `source nome_do_ambiente/bin/activate`

- No ambiente virtual installar os requirements
  - `pip install -r requirements.txt` 
  - Atenção: os requirements ficam dentro do diretório `/api` do projeto

- Rodar o servidor
  - `py app.py` 
  - Atenção: o `app.py` fica dentro do diretório `/api` do projeto

- Se tudo der certo:
  - Terminal vai mostrar: `Running on http://127.0.0.1:5000`
  - Uma aba do navegador vai abrir na rota `http://127.0.0.1:5000`
  - E ser redirecionada para `http://127.0.0.1:5000/docs/`

## Tools:
- Para atualizar o pip:
  - `python -m pip install --upgrade pip`
  
- Parar o servidor:
  - `CTRL + C`




## Organização das rotas:
> Pode sofrer alterações dependendo de como forem desenhadas as outras entidades ou pensando em uma melhor arquitetura.
### auth_routes:
    /register (POST)
    /login (POST)
    /logout (POST)

### parent_routes:
    /create_child (POST)
    /create_task (POST)
    /assign_task_to_child (POST)

### child_routes:
    /get_child (GET)
    /get_all_childs (GET)
    /update_child (PUT)
    /delete_child (DELETE)

### task_routes:
    /get_task (GET)
    /get_all_tasks (GET)
    /update_task (PUT)
    /delete_task (DELETE)






