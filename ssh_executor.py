import paramiko
import configparser
import threading

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
                    ssh.connect(ip, port=port, username=user, password=password)
                    if thread_enabled:
                        self.execute_with_threading(ssh, commands, user, ip)
                    else:
                        self.execute_without_threading(ssh, commands, user, ip)
                    ssh.close()
                except paramiko.AuthenticationException:
                    print(f"Errore di autenticazione per {user}@{ip}:{port}: verifica le credenziali.")
                except paramiko.SSHException as ssh_ex:
                    print(f"Errore di connessione SSH a {ip}:{port}: {ssh_ex}")
                except configparser.Error as config_e:
                    print(f"Errore nel leggere il file di configurazione: {config_e}")
        except KeyboardInterrupt:
            print("\nOperazione interrotta dall'utente.")
        except AttributeError as attr_e:
            print(f"Errore: file di configurazione non valido o mancante: {attr_e}")

    def execute_with_threading(self, ssh, commands, user, ip):
        threads = []
        for command in commands:
            thread = threading.Thread(target=self.execute_single_command, args=(ssh, command, user, ip))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

    def execute_without_threading(self, ssh, commands, user, ip):
        for command in commands:
            self.execute_single_command(ssh, command, user, ip)

    def execute_single_command(self, ssh, command, user, ip):
        try:
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
        except paramiko.SSHException as ssh_e:
            print(f"Errore SSH durante l'esecuzione di '{command}': {ssh_e}")

if __name__ == "__main__":
    executor = SSHExecutor()
    executor.execute_commands()
