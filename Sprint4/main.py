# Importação das bibliotecas json (exportação dos registros criados para um arquivo json), oracledb (conexão com o banco de dados Oracle) e datetime (para capturar o horário exato de criação do registro)
import json
import oracledb
import datetime
import pandas as pd
def criar_registro():
    """"Criar um registro no banco de dados Oracle utilizando o timestamp gerado automaticamente,
    fazendo com que o usuário apenas precise fornecer a posição X e Y."""

    # Tratamento de erro para a inserção dos valores de id, timestamp, posição X e posição Y.
    try:
        id = input("Digite o ID do registro: ")

        hora = datetime.datetime.now()
        timestamp = hora.strftime('%Y-%m-%dT%H:%M:%S.%f')[:23] + 'Z'

        xp: int = int(input("Digite a posição X do registro: "))
        yp: int = int(input("Digite a posição Y do registro: "))

        # Criação da variável "cadastro", que armazena um comando SQL para inserção dos valores anteriores no banco de dados.
        cadastro = f"""INSERT INTO CLICKS (ID, TIMESTAMP, X_POSITION, Y_POSITION) 
                                VALUES ({id}, '{timestamp}', {xp}, {yp})"""

        # Utilização do cursor para executar o comando armazenado na variável "cadastro" e logo em seguida realiza um commit
        cursor.execute(cadastro)
        conn.commit()
        print("Registro criado!")

    # Caso o usuário forneça um valor que não seja um int
    except ValueError:
        print("ERRO! Valor inválido para a posição X ou Y.")

    # Caso ocorra um erro na criação do registro.
    except Exception as e:
        print(f"ERRO! Erro ao criar registro.{e}")
def ler_registro():
    """"Ler os registros existentes no banco de dados Oracle."""

    # Tratamento de erro para a leitura dos registros do banco de dados
    try:
        # Criação da variável "ler", que armazena um comando SQL para leitura dos registros do banco de dados.
        ler = f"""SELECT * FROM CLICKS"""

        # Utilização do cursor para executar o comando armazenado na variável 'ler', e logo em seguida faz uso do método fetchall para recuperar os resultados da consulta e armazenar na variável 'lista_clicks'
        cursor.execute(ler)
        lista_clicks = cursor.fetchall()

        # Caso a quantidade de registros for igual a 0 (nenhum), o código entra no primeiro print. Caso contrário, o código print cada linha, ou seja, cada registro do banco de dados.
        if len(lista_clicks) == 0:
            print("Nenhum registro")
        else:
            for linha in lista_clicks:
                print(linha)

    # Caso ocorra um erro na leitura dos registros.
    except Exception as e:
        print(f"ERRO! Erro ao ler registros.{e}")
def atualizar_registro():
    """"Atualizar um registro (alterar valores de X e Y) específico do banco de dados Oracle através do ID do mesmo."""

    # Tratamento de erro para atualização de um registro através da inserção do ID por parte do usuário.
    try:
        id: int = input("Digite o ID do registro: ")

         # Criação da variável 'consulta', que armazena um comando SQL para leitura dos registros do banco de dados, onde o ID seja igual ao que o usuário forneceu.
        consulta = f"""SELECT * FROM CLICKS WHERE ID = {id}"""

        # Utilização do cursor para executar o comando armazenado na variável 'consulta', e logo em seguida faz uso do método fetchall para recuperar os resultados da consulta e armazenar na variável 'lista_clicks'
        cursor.execute(consulta)
        lista_clicks = cursor.fetchall()

        # Caso a quantidade de registros for igual a 0 (nenhum), o código entra no primeiro print.
        if len(lista_clicks) == 0:
            print(f"Nenhum registro cadastrado com o ID {id}")

        # Caso contrário, criação das variáveis 'timestamp', 'xp' e 'yp'. A 'timestamp' gera o horário automaticamente, porém a xp e yp pedem respectivamente o fornecimento das posições X e Y pro usuário inserir.
        else:
            hora = datetime.datetime.now()
            timestamp = hora.strftime('%Y-%m-%dT%H:%M:%S.%f')[:23] + 'Z'

            xp: int = int(input("Digite a posição X do registro: "))
            yp: int = int(input("Digite a posição Y do registro: "))

            # Criação da variável 'atualizar', que armazena um comando SQL para atualização dos valores anteriores no banco de dados de acordo com o registro que coincide com o ID fornecido.
            atualizar = f"""UPDATE CLICKS SET
                            TIMESTAMP = '{timestamp}',
                            X_POSITION = {xp},
                            Y_POSITION = {yp}
                            WHERE ID = {id}"""

            # Utilização do cursor para executar o comando armazenado na variável "cadastro" e logo em seguida realiza um commit
            cursor.execute(atualizar)
            conn.commit()
            print("Registro atualizado com sucesso!")

    # Caso o usuário forneça um valor que não seja um int.
    except ValueError:
        print("ERRO! Valor inválido para a posição X ou Y.")

    # Caso ocorra um erro na atualização dos registros.
    except Exception as e:
        print(f"ERRO! Erro ao atualizar registro.{e}")
def deletar_registro():
    """Deletar um registro no banco de dados Oracle através do ID do mesmo."""

    # Tratamento de erro para deleção de um registro através da inserção do ID por parte do usuário.
    try:
        id: int = input("Digite o ID do registro: ")

        # Criação da variável 'consulta', que armazena um comando SQL para leitura dos registros do banco de dados, onde o ID seja igual ao que o usuário forneceu.
        consulta = f"""SELECT * FROM CLICKS WHERE ID = {id}"""

        # Utilização do cursor para executar o comando armazenado na variável 'consulta', e logo em seguida faz uso do método fetchall para recuperar os resultados da consulta e armazenar na variável 'lista_clicks'
        cursor.execute(consulta)
        lista_clicks = cursor.fetchall()

        # Caso a quantidade de registros for igual a 0 (nenhum), o código entra no primeiro print.
        if len(lista_clicks) == 0:
            print(f"Nenhum registro cadastrado com o ID {id}")

        # Caso contrário, criação da variável 'excluir', que armazena um comando SQL para deletar um registro onde o ID é igual ao fornecido.
        else:
            excluir = f"""DELETE FROM CLICKS WHERE ID = {id}"""

            # Utilização do cursor para executar o comando armazenado na variável "cadastro" e logo em seguida realiza um commit
            cursor.execute(excluir)
            conn.commit()
            print("Registro excluído com sucesso!")

    # Caso o usuário forneça um valor que não seja um int
    except ValueError:
        print("Digite um número inteiro para o ID do registro.")

    # Caso ocorra um erro na criação do registro.
    except Exception as e:
        print(f"ERRO! Erro ao deletar registros.{e}")
def exportar_para_json():
    """Exportar os registros do banco de dados para um arquivo JSON."""
    try:
        # Consulta ao banco de dados para obter todos os registros
        cursor.execute("SELECT * FROM CLICKS")
        registros = cursor.fetchall()

        # Lista para armazenar os registros no formato json
        registros_formatados = []
        for registro in registros:
            registros_formatados.append({
                "ID": registro[0],
                "TIMESTAMP": str(registro[1]),
                "X_POSITION": registro[2],
                "Y_POSITION": registro[3]
            })

        # Abre o arquivo JSON para escrita e escreve os registros nele
        with open('registros.json', 'w') as arquivo_json:
            json.dump(registros_formatados, arquivo_json, indent=4)

        print("Registros exportados com sucesso!")

    except Exception as e:
        print(f"ERRO! Falha ao exportar registros para JSON: {e}")
def carregar_csv_para_banco():
    """Carrega os registros de um arquivo CSV para o banco de dados Oracle."""
    try:
        # Caminho para o arquivo CSV
        caminho_arquivo_csv = input("Digite o caminho do arquivo CSV: ")

        print("IDs adicionados com sucesso!")

        # Carrega o CSV usando o pandas
        dados_csv = pd.read_csv(caminho_arquivo_csv)

        # Nome da tabela Oracle onde você deseja inserir os dados
        tabela_oracle = 'CLICKS'

        # Convertendo o DataFrame pandas para uma lista de tuplas
        registros = [tuple(x) for x in dados_csv.to_numpy()]

        # Construindo o comando SQL para inserção
        sql_insert = f"INSERT INTO {tabela_oracle} (ID, TIMESTAMP, X_POSITION, Y_POSITION) VALUES (:1, :2, :3, :4)"

        # Utilizando o cursor para executar o comando SQL
        cursor.executemany(sql_insert, registros)
        conn.commit()

        print("Registros do CSV carregados com sucesso para o banco de dados Oracle.")

    except Exception as e:
        print(f"Erro ao carregar registros do CSV para o banco de dados: {e}")
def buscar_ID():
    """Buscar o registro pelo ID."""

    try:
        id = input("Digite o ID do registro: ")

        consulta  = f"""SELECT * FROM CLICKS WHERE ID = {id}"""

        cursor.execute(consulta)
        lista_clicks = cursor.fetchall()

        if len(lista_clicks) == 0:
            print(f"Nenhum registro cadastrado com o ID {id}")

        else:
            for linha in lista_clicks:
                print(linha)

    # Caso o usuário forneça um valor que não seja um int
    except ValueError:
        print("Digite um número inteiro para o ID do registro.")

    # Caso ocorra um erro na criação do registro.
    except Exception as e:
        print(f"ERRO! Erro ao buscar registro por ID.{e}")
def heatmap():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import cv2

    df = pd.read_json("registros.json")
    df.sample(3)

    sns.scatterplot(
        data=df,
        x="X_POSITION",
        y="Y_POSITION"
    )

    # Carregando a imagem
    layout = cv2.imread('layout.png')

    # Convertendo de Bgr para RGB
    layout = cv2.cvtColor(layout, cv2.COLOR_BGR2RGB)

    df_filtrado = df[df["Y_POSITION"] < layout.shape[0]]

    sns.scatterplot(
        data=df,
        x="X_POSITION",
        y="Y_POSITION"
    )

    fundo = cv2.imread('../layout.png')
    fundo = cv2.cvtColor(layout, cv2.COLOR_BGR2RGB)
    plt.imshow(layout)

    df_filtrado = df[df["Y_POSITION"] < layout.shape[0]]
    df_filtrado

    sns.kdeplot(
        data=df_filtrado,
        x="X_POSITION",
        y="Y_POSITION"
    )

    sns.scatterplot(
        data=df_filtrado,
        x="X_POSITION",
        y="Y_POSITION"
    )

    layout = cv2.imread('../layout.png')
    layout = cv2.cvtColor(fundo, cv2.COLOR_BGR2RGB)

    df_filtrado = df[df["Y_POSITION"] < layout.shape[0]]

    sns.kdeplot(
        data=df_filtrado,
        x="X_POSITION",
        y="Y_POSITION",
        fill=True, cmap="rocket", alpha=0.5, levels=15, lw=0, thresh=0.1
    )

    sns.scatterplot(
        data=df_filtrado,
        x="X_POSITION",
        y="Y_POSITION",
        s=20, c="k"
    )

    plt.xlim(0, layout.shape[1])
    plt.ylim(layout.shape[0], 0)

    plt.savefig("heatmap.png", dpi=600)


# Credenciais de Acesso (login e senha)
login: str = input("Digite o login do Oracle SQL Developer: ")
senha: str = input("Agora digite a senha: ")

try:
    # Conexão com o banco de dados
    conn = oracledb.connect(user=login,
                            password=senha,
                            host="oracle.fiap.com.br",
                            port=1521,
                            service_name="orcl")

    # Cria o cursor para realizar as operações no banco de dados
    cursor = conn.cursor()

# Caso ocorra algum erro durante a conexão.
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True
exportar_para_json()
# Caso a conexão aconteça corretamente, este looping acontecerá.
while conexao:
    # Printa as opções do menu.
    print("Bem-vindo ao menu!\n")
    print("C - Criar registro.")
    print("R - Ler registro.")
    print("U - Atualizar registro.")
    print("D - Deletar registro.\n")
    print("======== MANIPULAÇÃO DOS REGISTROS =======")
    print("1 - Exportar para json.")
    print("2 - Carregar registros de um arquivo CSV para o banco de dados.")
    print("3 - Gerar um mapa de calor dos clicks (para essa opção você precisa exportar os registros para um json primeiro")
    print("4 - Buscar registro pelo ID.\n")
    print("S - Sair do programa.")

    # Criação da variável 'decisao', que é um input para a escolha da opção do menu.
    decisao = input("Escolha uma das opções acima: ").upper()
    if decisao == "C":
        criar_registro()
    elif decisao == "R":
        ler_registro()
    elif decisao == "U":
        atualizar_registro()
    elif decisao == "D":
        deletar_registro()
    elif decisao == "1":
        exportar_para_json()
    elif decisao == "2":
        carregar_csv_para_banco()
    elif decisao == "3":
        heatmap()
    elif decisao == "4":
        buscar_ID()
    elif decisao == "S":
        break
    else:
        # Print caso nenhuma das opções acima for selecionada.
        print("Opção inválida.")

