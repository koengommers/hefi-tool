from .commands import commands

class Application:
    def __init__(self):
        self.command_mappings = {command_handler.name: command_handler for command_handler in commands}

    def process_input(self, command):
        if len(command) > 0:
            self.execute_command(command)
        else:
            while True:
                while not len(command) > 0:
                    command = input('>> ')
                if command in ['exit', 'quit']:
                    exit()
                self.execute_command(command)
                command = str()

    def execute_command(self, command):
        if type(command) == str:
            command = command.split()

        command_handler = self.command_mappings[command[0]]
        command_handler(command[1:])

