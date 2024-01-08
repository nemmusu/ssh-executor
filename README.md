# Readme

[Readme: Italiano](./README_IT.md)

[Readme: English](./README.md)

# SSH Executor

This is a simple Python module that allows you to execute SSH commands on different servers either in parallel or sequentially. Credentials and commands to be executed are read from a configuration file.

## Installation

The module uses the `paramiko`, `configparser` and `threading` libraries. You can install them with pip:

```
pip install paramiko configparser
```

## Configuration file

The module reads a `config.ini` configuration file which must be structured as follows (you can add more servers using this syntax):

```ini
[configuration]
thread = True

[server1]
user = username
pass = password
port = 22
ip = 192.168.1.1
commands = command1, command2, command3

[server2]
user = username
pass = password
port = 22
ip = 192.168.1.2
commands = command1, command2, command3
```

The `[configuration]` section contains the `thread` option.
If `thread` is set to `True`, the commands will be executed in parallel on each server.
If `thread` is set to `False` or not specified, the commands will be executed sequentially.

The other sections represent the different servers on which to execute the commands. Each section must contain the following options:

- `user`: the username for the SSH connection.
- `pass`: the password for the SSH connection.
- `port`: the port for the SSH connection (optional, default is 22).
- `ip`: the IP address of the server.
- `commands`: a list of comma-separated commands to be executed on the server.

## Usage

Make sure you have set the parameters of `config.ini` correctly and run the command:

```
python ssh_executor.py
```

## Errors

If errors are detected during the SSH connection or command execution, they will be printed on the console. These include authentication errors, SSH connection errors, and errors during command execution.