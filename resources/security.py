import bcrypt

# Função para criar um hash de senha
def create_password_hash(password):
    # Gere um salt aleatório
    salt = bcrypt.gensalt()
    # Gere o hash da senha com o salt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash

# Função para verificar a senha
def verify_password(stored_password_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash)

