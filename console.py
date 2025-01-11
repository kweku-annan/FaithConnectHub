#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd


class FaithConnectHubCommand(cmd.Cmd):
    """Class for the entry point of command interpreter"""

    prompt = "FaithConnectHub$ "

    def do_quit(self, args):
        """Exits program using Quit command"""
        return True

    def do_EOF(self, line):
        """Exits command"""
        print()
        return True

    def emptyline(self):
        """Does nothing"""
        pass

if __name__ == '__main__':
    FaithConnectHubCommand().cmdloop()