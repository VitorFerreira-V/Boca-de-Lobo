import sqlite3

conexao = sqlite3.connect('Boca_de_Lobo.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        cep TEXT NOT NULL
    )
''')
conexao.commit()

def SalvarUsuario(nome_usuario, email, senha_pura, cep):
    try:
        cursor.execute('''
            INSERT INTO usuarios (nome_usuario, email, senha, cep)
            VALUES (?, ?, ?, ?)
        ''', (nome_usuario, email.lower().strip(), senha_pura, cep))

        conexao.commit()
        print(f"\n Usuário '{nome_usuario}' cadastrado com sucesso!")
        return True
    except sqlite3.IntegrityError:
        print("\n Erro: Este e-mail já está cadastrado!")
        return False
    except Exception as e:
        print(f"\n Erro ao cadastrar: {e}")
        return False

def ListarUsuarios():
    cursor.execute("SELECT id, nome_usuario, email, cep FROM usuarios")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return False

    print("\n" + "="*65)
    print(f"{'ID':<5} | {'NOME':<20} | {'EMAIL':<25} | {'CEP':<10}")
    print("="*65)

    for usr in usuarios:
        id_usr, nome, email, cep = usr
        print(f"{id_usr:<5} | {nome:<20} | {email:<25} | {cep:<10}")
    print("="*65)
    return True

def ExcluirUsuario(user_id):
    try:
        cursor.execute("SELECT nome_usuario FROM usuarios WHERE id = ?", (user_id,))
        usuario = cursor.fetchone()

        if usuario:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conexao.commit()
            print(f"\n Usuário '{usuario[0]}' (ID: {user_id}) excluído com sucesso!")
        else:
            print(f"\n Erro: Nenhum usuário encontrado com o ID {user_id}.")
    except Exception as e:
        print(f"\n Erro ao excluir usuário: {e}")


while True:
    print("\n" + "="*25)
    print("   SISTEMA BOCA DE LOBO")
    print("="*25)
    print("1. Cadastrar")
    print("2. Ver Tabela de Usuários")
    print("3. Excluir Cadastro pelo ID")
    print("4. Sair")

    opcao = input("\nEscolha uma opção (1/2/3/4): ").strip()

    if opcao == '1':
        print("\n--- Novo Cadastro ---")

        while True: #nome
          nome = input("Digite o seu nome: ").strip()

          if nome.isdigit():
            print("Erro! Digite seu nome corretamente.")
          else:break


        while True: #senha
          senha = input("Digite a sua senha: ").strip()
          senha2 = input("Confirme sua senha: ").strip()

          if len(senha) <6:
            print("Senha muito curta! Digite uma maior(Mínimo 6 digitos)")
          elif senha!=senha2:
            print("As senhas não coincidem, digite novamente.")
          else:break

        while True: #cep
            cep_input = input("Digite o seu CEP: ").strip()
            cep_limpo = cep_input.replace("-", "")

            if cep_limpo.isdigit() and len(cep_limpo) == 8:
                cep = f"{cep_limpo[:5]}-{cep_limpo[5:]}"
                break
            print("CEP inválido! Digite 8 números.")

        while True: #email
          email = input("Digite o seu e-mail: ").strip()

          if not "@" in email or not "." in email:
            print("Email incorreto! Digite novemante.")
          else:break

        SalvarUsuario(nome, email, senha, cep)

    elif opcao == '2':
        ListarUsuarios()

    elif opcao == '3':
        tem_usuarios = ListarUsuarios()
        if tem_usuarios:
            user_id = input("\nDigite o ID do usuário que deseja excluir: ").strip()
            if user_id.isdigit():
                ExcluirUsuario(int(user_id))
            else:
                print("ID inválido! Digite apenas números.")

    elif opcao == '4':
        print("\nSaindo do sistema... Até mais!")
        break
    else:print("\nOpção inválida! Escolha de 1 a 4")

conexao.close()
