"""
Sample todo
{
    "id": "",
    "name": "",
    "description": "",
    "status": "TODO",
    "comments": [],
    "project": "",
    "current": false,
    "archive": false,
}
"""
from datetime import datetime
import getopt
import json
import sys


DEFAULT = "default"
NOW = datetime.now().strftime("%m/%d/%Y, %H:%M")

TODO = 0
IN_PROGRESS = 1
DONE = 2
STATUS = {
    TODO: "TODO",
    IN_PROGRESS: "IN PROGRESS",
    DONE: "DONE"
}

try:
    with open("todos.json", "r") as f:
        todos = json.load(f)
except Exception:
    todos = []


def create_todo(project, name, description=""):
    _id = len(todos)
    todo = {
        "id": _id,
        "name": name,
        "description": description,
        "status": STATUS[TODO],
        "comments": [],
        "project": project,
        "current": False,
        "archive": False,
        "created": NOW,
        "completed": None,
        "archived": None,
    }
    todos.append(todo)
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)
    return todo


def update_name(_id, name):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["name"] = name
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_description(_id, description):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["description"] = description
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_project(_id, project):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["project"] = project
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def add_comment(_id, comment):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["comments"].append(f"[{NOW}] {comment}")
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_todo_status(todo, status):
    todo["status"] = status
    if todo["archive"]:
        raise Exception("Invalid id.")
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo, print_done=True)


def workon_todo(_id):
    for t in todos:
        t["current"] = False
    todo = todos[_id]
    todo["current"] = True
    update_todo_status(todo, STATUS[IN_PROGRESS])


def complete_todo(_id):
    todo = todos[_id]
    todo["current"] = False
    todo["completed"] = NOW
    update_todo_status(todo, STATUS[DONE])


def archive_todo(_id):
    todo = todos[_id]
    todo["archive"] = True
    todo["archived"] = NOW
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print(f"Archived todo {_id}")


def print_todo(todo, print_done=False):
    if todo["archive"]:
        return
    if todo["status"] == STATUS[DONE] and not print_done:
        return
    print(json.dumps(todo, indent=4))
    print("--------------------------------")


def print_all(print_done=False):
    for todo in todos:
        print_todo(todo)


if __name__ == "__main__":
    command = sys.argv[1]
    argumentList = sys.argv[2:]

    options = "p:n:d:i:c:"
    long_options = ["project=", "name=", "description=", "id=", "comment="]

    if command == "add":
        project = DEFAULT
        description = ""
        try:
            arguments, values = getopt.getopt(
                argumentList, options, long_options
            )
            # checking each argument
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-p", "--project"):
                    project = currentValue
                if currentArgument in ("-n", "--name"):
                    name = currentValue
                if currentArgument in ("-d", "--description"):
                    description = currentValue
        except getopt.error as err:
            # output error, and return with an error code
            print(str(err))
        create_todo(project, name, description)

    if command == "workon":
        _id = int(sys.argv[2])
        workon_todo(_id)

    if command == "complete":
        _id = int(sys.argv[2])
        complete_todo(_id)

    if command == "update":
        _id = int(sys.argv[2])
        project = None
        name = None
        description = None
        comment = None
        argumentList = sys.argv[3:]
        try:
            arguments, values = getopt.getopt(
                argumentList, options, long_options
            )
            # checking each argument
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-p", "--project"):
                    project = currentValue
                if currentArgument in ("-i", "--id"):
                    _id = int(currentValue)
                if currentArgument in ("-n", "--name"):
                    name = currentValue
                if currentArgument in ("-d", "--description"):
                    description = currentValue
                if currentArgument in ("-c", "--comment"):
                    comment = currentValue
        except getopt.error as err:
            # output error, and return with an error code
            print(str(err))
        if name is not None:
            update_name(_id, name)
        if description is not None:
            update_description(_id, description)
        if comment is not None:
            add_comment(_id, comment)
        if project is not None:
            update_project(_id, project)

    if command == "ls":
        options = "p:i:s:"
        long_options = ["project=", "id=", "status=", "show-done", "current"]

        project = None
        _id = None
        status = None
        current = False
        print_done = False
        try:
            arguments, values = getopt.getopt(
                argumentList, options, long_options
            )
            # checking each argument
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-p", "--project"):
                    project = currentValue
                if currentArgument in ("-i", "--id"):
                    _id = int(currentValue)
                if currentArgument in ("-s", "--status"):
                    status = currentValue
                if currentArgument in ("--show-done"):
                    print_done = True
                if currentArgument in ("--current"):
                    current = True
        except getopt.error as err:
            # output error, and return with an error code
            print(str(err))
        if current:
            current_present = False
            for t in todos:
                if t["current"]:
                    current_present = True
                    todos = [t]
            if not current_present:
                todos = []
        elif _id is not None:
            todos = [todos[_id]]
        else:
            if status is not None:
                if status == "todo":
                    req = STATUS[TODO]
                elif status == "inp":
                    req = STATUS[IN_PROGRESS]
                else:
                    req = STATUS[DONE]
                    print_done = True
                todos = list(filter(lambda x: x["status"] == req, todos))
            if project is not None:
                todos = list(filter(lambda x: x["project"] == project, todos))
        for t in todos:
            print_todo(t, print_done=print_done)

    if command == "archive":
        _id = int(sys.argv[2])
        archive_todo(_id)
