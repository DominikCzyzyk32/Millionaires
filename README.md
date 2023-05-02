# Millionaires

Gra stworzona na podstawie popularnego teleturnieju o nazwie "Milionerzy"

## Requirements

1. PostgreSQL DBMS
2. Disable the master password for pgAdmin by setting the configuration parameter MASTER_PASSWORD_REQUIRED=False. Change it in file config.py. Probable location on Windows: C:\Program Files\PostgreSQL\pgAdmin 4\v5\web
3. Change authentication method for PostgreSQL from md5 to trust in pg_hba.conf. It will assure that there won't be need to provide password for any user.
4. Python packages

```
pip install -r requirements.txt
```

Run main.py to launch application.
