import paramiko
import configparser
import concurrent.futures

class SSHExecutor:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)
        except FileNotFoundError as e:
            print(f"Errore: file di configurazione non trovato: {e}")

    def execute_commands(self):
        try:
            thread_enabled = self.config['configuration'].getboolean('thread', fallback=False)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for section in self.config.sections():
                    if section == 'configuration':
                        continue

                    try:
                        user = self.config[section].get('user')
                        password = self.config[section].get('pass')
                        port = self.config[section].getint('port', fallback=22)
                        ip = self.config[section].get('ip')
                        commands = [cmd.strip() for cmd in self.config[section].get('commands', '').split(',')]
                        if None in (user, password, ip):
                            print(f"Errore: informazioni incomplete per la sezione '{section}'")
                            continue
                        print(f"Connessione SSH a {user}@{ip}:{port}")

                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        try:
                            ssh.connect(ip, port=port, username=user, password=password)
                        except paramiko.AuthenticationException:
                            print(f"Errore di autenticazione per {user}@{ip}:{port}: verifica le credenziali.")
                            continue
                        except paramiko.SSHException as ssh_ex:
                            print(f"Errore di connessione SSH a {ip}:{port}: {ssh_ex}")
                            continue

                        if thread_enabled:
                            futures.append(executor.submit(self.execute_single_command, ssh, commands, user, ip))
                        else:
                            self.execute_single_command(ssh, commands, user, ip)

                    except configparser.Error as config_e:
                        print(f"Errore nel leggere il file di configurazione: {config_e}")

                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Errore durante l'esecuzione del comando: {e}")

        except KeyboardInterrupt:
            print("\nOperazione interrotta dall'utente.")
        except AttributeError as attr_e:
            print(f"Errore: file di configurazione non valido o mancante: {attr_e}")

    def execute_single_command(self, ssh, commands, user, ip):
        try:
            if ssh is not None:
                for command in commands:
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()
                    output = stdout.read().decode()
                    error = stderr.read().decode()

                    print(f"Esecuzione del comando '{command}' su {user}@{ip}")
                    if output:
                        print(f"Output di '{command}':")
                        print(output)
                    if error:
                        print(f"Errore durante l'esecuzione di '{command}':")
                        print(error)
                    if exit_status != 0:
                        print(f"Comando '{command}' ha restituito un codice di uscita non zero: {exit_status}")
            else:
                print("Connessione SSH non stabilita correttamente.")
        except paramiko.SSHException as ssh_e:
            print(f"Errore SSH durante l'esecuzione di '{command}': {ssh_e}")

if __name__ == "__main__":
    executor = SSHExecutor()
    executor.execute_commands()
