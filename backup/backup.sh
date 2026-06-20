BASE_DIR="$HOME/securechain"
DOC_DIR="$BASE_DIR/documentos"
BACKUP_DIR="$BASE_DIR/backup"
LOG_FILE="$BASE_DIR/logs/backup.log"
DATA=$(date +"%Y-%m-%d_%H-%M-%S")

ARQUIVO_TAR="$BACKUP_DIR/documentos_$DATA.tar.gz"
ARQUIVO_CRYPT="$BACKUP_DIR/documentos_$DATA.tar.gz.enc"

echo "Digite a senha para criptografar o backup:"
read -s SENHA

tar -czf "$ARQUIVO_TAR" "$DOC_DIR"

openssl enc -aes-256-cbc -salt -pbkdf2 -in "$ARQUIVO_TAR" -out "$ARQUIVO_CRYPT" -pass pass:"$SENHA"

if [ $? -eq 0 ]; then
    TAMANHO=$(du -h "$ARQUIVO_CRYPT" | cut -f1)
    echo "$DATA | Backup criado | $ARQUIVO_CRYPT | Tamanho: $TAMANHO | Status: OK" >> "$LOG_FILE"
    rm "$ARQUIVO_TAR"

    cd "$BASE_DIR"
    python3 -c "from blockchain.blockchain import adicionar_bloco; adicionar_bloco('Backup seguro executado com AES-256')"

    echo "[OK] Backup criptografado criado: $ARQUIVO_CRYPT"
else
    echo "$DATA | Falha ao criar backup | Status: ERRO" >> "$LOG_FILE"
    echo "[ERRO] Falha no backup."
