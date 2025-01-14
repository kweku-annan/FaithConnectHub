#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd
import re
import shlex

from app.models import storage
from app.models.attendance import Attendance
from app.models.base_model import BaseModel
from app.models.event import Event
from app.models.finance import Expense, Income
from app.models.user import User
from app.models.membership import Membership


class FaithConnectHubCommand(cmd.Cmd):
    """Class for the entry point of command interpreter"""

    prompt = "FaithConnectHub$ "
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Membership': Membership,
        'Event': Event, 'Expense': Expense, 'Income': Income, 'Attendance': Attendance,

    }

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

    # def do_create(self, args):
    #     """Creates a new instance of the BaseModel"""
    #     if args:
    #         kwargs = dict()
    #         args_list = args.split(" ")
    #
    #         class_name = args_list[0]
    #
    #         if class_name in self.classes:
    #             if len(args_list) > 1:
    #                 params = args_list[1:]
    #                 for param in params:
    #                     key_value = param.split("=")
    #                     key = key_value[0]
    #                     value = key_value[1]
    #
    #                     if type(value) is str:
    #                         value = value.replace('"', '').replace("_", " ")
    #                     kwargs[key] = value
    #
    #                 instance = FaithConnectHubCommand.classes[class_name](**kwargs)
    #                 print(instance.id)
    #                 instance.save()
    #             else:
    #                 instance = FaithConnectHubCommand.classes[class_name]
    #                 instance.save()
    #                 print(instance.id)
    #         else:
    #             print("** class name doesn't exist **")
    #     else:
    #         print("** class name is missing **")

    def do_create(self, args):
        """ Create an object of any class"""
        pattern = """(^\w+)((?:\s+\w+=[^\s]+)+)?"""
        m = re.match(pattern, args)
        args = [s for s in m.groups() if s] if m else []

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in FaithConnectHubCommand.classes:
            print("** class doesn't exist **")
            return

        kwargs = dict()
        if len(args) > 1:
            params = args[1].split(" ")
            params = [param for param in params if param]
            for param in params:
                [name, value] = param.split("=")
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                kwargs[name] = value

        new_instance = FaithConnectHubCommand.classes[class_name]()

        for attr_name, attr_value in kwargs.items():
            setattr(new_instance, attr_name, attr_value)

        new_instance.save()
        print(new_instance.id)

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
        tokens = shlex.split(args)
        if len(tokens) == 0 or tokens == "":
            print("** class name is missing **")
        elif tokens[0] not in self.classes:
            print("** class name doesn't exist **")
        elif len(tokens) == 1 or tokens[1] == "":
            print("** instance id is missing **")
        else:
            key = f"{tokens[0]}.{tokens[1]}"
            a_dict = storage.all()
            if key in a_dict:
                del a_dict[key]
                storage.save()
            else:
                print("** no instance id found **")

    def do_all(self, args):
        """Prints all string representation of all instances
        based or not on the class name"""
        a_list = []
        if args == "" or len(args) == 0:
            for key, value in (storage.all()).items():
                a_list.append(str(value))
            print(a_list)
        elif args in self.classes:
            for key, value in (storage.all()).items():
                if key == f"{args}.{value.id}":
                    a_list.append(str(value))
            print(a_list)
        else:
            print("** class does not exist **")

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding
        or updating attribute
        """
        tokens = shlex.split(args)
        if len(tokens) == 0 or tokens == "":
            print("** class name missing **")
        elif tokens[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(tokens) == 1 or tokens[1] == "":
            print("** instance id missing **")
        elif len(tokens) == 2:
            a_dict = storage.all()
            key = f"{tokens[0]}.{tokens[1]}"
            if key not in a_dict:
                print("** no instance found **")
            else:
                print("** attribute name missing **")
        elif len(tokens) == 3:
            print("** value missing **")
        else:
            a_dict = storage.all()
            key = f"{tokens[0]}.{tokens[1]}"
            if key in a_dict:
                setattr(a_dict[key], tokens[2], args[3])
                storage.save()





if __name__ == '__main__':
    FaithConnectHubCommand().cmdloop()