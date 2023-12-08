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

- Erro em algumas rotas
  - É esperado que erros ocorram caso esteja utilizando a versão mais
  recente deste repositório. Isto ocorre pois foram adicionados novos atributos
  à algumas rotas, e pode ser que seu banco não esteja atualizado.
  - Para corrigir:
  - Acesse a pasta `api/instance`
  - Apague o banco atual `api/instance/database.db`
  - O novo banco será criado ao executar o servidor novamente.
  - `py app.py` 
  - Atenção: o `app.py` fica dentro do diretório `/api` do projeto

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
    /get_parent (GET)
    /get_all_parents (GET)
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
    /update_all_tasks (PUT)
    /delete_task (DELETE)
    /delete_all_tasks (DELETE)
    /complete_task (PUT)

### child_task_routes:
    /get_child_task (GET)
    /get_all_child_tasks (GET)
    /update_child_tasks (PUT)
    /delete_child_task (DELETE)

### item_routes:
    /add_item (POST)
    /get_item (GET)
    /get_all_items(GET)
    /update_item(PUT)
    /delete_item(DELETE)

### style_tamagochi_routes:
    /add_style_tamagochi (POST)
    /get_style_tamagochi (GET)
    /get_all_style_tamagochis (GET)
    /update_style_tamagochi (PUT)
    /delete_style_tamagochi (DELETE)

### tamagochi_routes:
    /create_tamagochi (POST)
    /get_tamagochi (GET)
    /get_all_tamagochis (GET)
    /update_tamagochi (PUT)
    /delete_tamagochi (DELETE)

### inventory_routes:
    /add_to_inventory (POST)
    /get_inventory (GET)
    /get_all_inventories (GET)
    /update_inventory (PUT)
    /delete_inventory (DELETE)

### reward_routes:
    /create_reward (POST)
    /get_reward (GET)
    /get_all_rewards (GET)
    /update_reward (PUT)
    /delete_reward (DELETE)

### task_reward_routes:
    /add_task_reward (POST)
    /get_task_reward (GET)
    /get_all_task_rewards (GET)
    /update_task_reward (PUT)
    /delete_task_reward (DELETE)




