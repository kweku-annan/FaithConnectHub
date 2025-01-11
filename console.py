#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd
import shlex

from app.models import storage
from app.models.base_model import BaseModel


class FaithConnectHubCommand(cmd.Cmd):
    """Class for the entry point of command interpreter"""

    prompt = "FaithConnectHub$ "
    classes = {'BaseModel': BaseModel}

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

    def do_create(self, args):
        """Creates a new instance of the BaseModel"""
        if args:
            if args in self.classes:
                instance = eval(args)
                print(instance.id)
                instance.save()
            else:
                print("** class name doesn't exist **")
        else:
            print("** class name is missing **")

    def do_show(self, args):
        """Prints the string representation of an instance based on
        the class name and id."""
        tokens = shlex.split(args)
        if len(tokens) == 0 or tokens == "":
            print("** class name is missing **")
        elif tokens[0] not in self.classes:
            print("** class name doesn't exist **")
        elif len(tokens) == 1 or tokens[1] == "":
            print("** instance id missing **")
        else:
            key = f"{tokens[0]}.{tokens[1]}"
            a_dict = storage.all()
            if key in a_dict:
                print(a_dict[key])
            else:
                print("** no instance id found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and """


if __name__ == '__main__':
    FaithConnectHubCommand().cmdloop()