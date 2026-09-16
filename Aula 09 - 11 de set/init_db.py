from pathlib import Path
from db import get_connection

def criar_tabelas():
    sql = Path("schema.sql").read_text(encoding="utf-8")
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            
    print("Tabelas criadas com sucesso")
    
    
if __name__ == "__main__":
    criar_tabelas()