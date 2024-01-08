# Readme

[Readme: Italiano](./README_IT.md)

[Readme: English](./README.md)

# SSH Executor

Questo è un semplice modulo Python che consente di eseguire comandi SSH su diversi server in parallelo o sequenzialmente. Le credenziali e i comandi da eseguire vengono letti da un file di configurazione.

## Installazione

Il modulo utilizza le librerie `paramiko`, `configparser` e `threading`. Puoi installarle con pip:

```
pip install paramiko configparser
```

## File di configurazione

Il modulo legge un file di configurazione `config.ini` che deve essere strutturato come segue (si possono aggiungere più server usando questa sintassi):

```ini
[configuration]
thread = True

[server1]
user = username
pass = password
port = 22
ip = 192.168.1.1
commands = comando1, comando2, comando3

[server2]
user = username
pass = password
port = 22
ip = 192.168.1.2
commands = comando1, comando2, comando3
```

La sezione `[configuration]` contiene l'opzione `thread`.
Se `thread` è impostato su `True`, i comandi verranno eseguiti in parallelo su ogni server.
Se `thread` è impostato su `False` o non specificato, i comandi verranno eseguiti sequenzialmente.

Le altre sezioni rappresentano i diversi server sui quali eseguire i comandi. Ogni sezione deve contenere le seguenti opzioni:

- `user`: il nome utente per la connessione SSH.
- `pass`: la password per la connessione SSH.
- `port`: la porta per la connessione SSH (opzionale, default è 22).
- `ip`: l'indirizzo IP del server.
- `commands`: una lista di comandi separati da virgole da eseguire sul server.

## Uso

Assicurati di aver impostato i parametri del `config.ini` in maniera corretta ed esegui il comando:

```
python ssh_executor.py
```

## Errori

Se vengono rilevati errori durante la connessione SSH o l'esecuzione dei comandi, verranno stampati sulla console. Questi includono errori di autenticazione, errori di connessione SSH e errori durante l'esecuzione dei comandi.