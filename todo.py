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
import json

import click


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

TODO_FILE_PATH = ".gtd.json"

try:
    with open(TODO_FILE_PATH, "r") as f:
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
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)
    return todo


def update_name(_id, name):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["name"] = name
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_description(_id, description):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["description"] = description
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_project(_id, project):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["project"] = project
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def add_comment(_id, comment):
    todo = todos[_id]
    if todo["archive"]:
        raise Exception("Invalid id.")
    todo["comments"].append(f"[{NOW}] {comment}")
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print_todo(todo)


def update_todo_status(todo, status):
    todo["status"] = status
    if todo["archive"]:
        raise Exception("Invalid id.")
    with open(TODO_FILE_PATH, "w") as outfile:
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
    with open(TODO_FILE_PATH, "w") as outfile:
        json.dump(todos, outfile, indent=4)
    print(f"Archived todo {_id}")


def print_todo(todo, print_done=False):
    if todo["archive"]:
        return
    if todo["status"] == STATUS[DONE] and not print_done:
        return
    print(json.dumps(todo, indent=4))
    print("--------------------------------")


def todo_by_id(_id):
    print_todo(todos[_id])


def print_all(print_done=False):
    for todo in todos:
        print_todo(todo)


def current_todo():
    global todos
    current_present = False
    for t in todos:
        if t["current"]:
            current_present = True
            print_todo(t)
    if not current_present:
        print("There is no todo being worked on.")


def todos_by_status(status):
    global todos
    print_done = False
    if status == "todo":
        req = STATUS[TODO]
    elif status == "inp":
        req = STATUS[IN_PROGRESS]
    else:
        req = STATUS[DONE]
        print_done = True
    todos = list(filter(lambda x: x["status"] == req, todos))
    for t in todos:
        print_todo(t, print_done)


def todos_by_project(project):
    global todos
    todos = list(filter(lambda x: x["project"] == project, todos))
    for t in todos:
        print_todo(t)


@click.group()
def todo():
    """
    A Simple CLI tool to manage your todos.
    """
    pass


@click.command()
@click.option(
    "-n", "--name",
    required=True,
    type=str,
    help="Short description of todo",
)
@click.option(
    "-d", "--description",
    required=False,
    type=str,
    help="Detailed description of todo",
)
@click.option(
    "-p", "--project",
    required=False,
    default=DEFAULT,
    type=str,
    help="Name of project the todo belongs to",
)
def add(name, description, project):
    """Add a new todo.

    Eg. python todo.py add -n "buy milk" -p "chores"
    """
    create_todo(project, name, description)


@click.command()
@click.argument('id', type=int, nargs=1)
def workon(id):
    """Start or continue working on a specific todo.

    Eg. python todo.py workon 23
    """
    workon_todo(id)


@click.command()
@click.argument('id', type=int, nargs=1)
def archive(id):
    """
    Archive a todo.

    Eg. python todo.py archive 23
    """
    archive_todo


@click.command()
@click.argument('id', type=int, nargs=1)
def complete(id):
    """Complete a todo.

    Eg. python todo.py complete 23
    """
    complete_todo(id)


@click.command()
@click.argument('id', type=int, nargs=1)
@click.option(
    "-n", "--name",
    required=False,
    default=None,
    type=str,
    help="Short description of todo",
)
@click.option(
    "-d", "--description",
    required=False,
    default=None,
    type=str,
    help="Detailed description of todo",
)
@click.option(
    "-p", "--project",
    required=False,
    default=None,
    type=str,
    help="Name of project the todo belongs to",
)
def update(id, name, description, project):
    """Update the details of a given todo.

    Eg. python todo.py update 23 -d "New description."
    """
    if name is not None:
        update_name(id, name)
    if description is not None:
        update_description(id, description)
    if project is not None:
        update_project(id, project)


@click.command()
@click.argument("id", type=int, nargs=1)
@click.argument("comment", type=str, nargs=1)
def comment(id, comment):
    """Comment on a todo.

    Eg. python todo.py comment 23 "My comment."
    """
    add_comment(id, comment)


@click.command()
def current():
    """Show current todo.

    Eg. python todo.py current
    """
    current_todo()


@click.command()
@click.option(
    "-id",
    required=False,
    default=None,
    type=int,
    help="Filter by ID of the todo.",
)
@click.option(
    "-s", "--status",
    required=False,
    default=None,
    type=click.Choice(["todo", "inp", "done"], case_sensitive=True),
    help="Filter by status of todo."
)
@click.option(
    "-p", "--project",
    required=False,
    default=None,
    type=str,
    help="Filter by name of project the todo belongs to",
)
def show(id, status, project):
    """List todos.

    List all
        python todo.py list

    List by id
        python todo.py list -id 23

    List by status
        python todo.py list -s todo

    List by project
        python todo.py list -p "project"
    """
    if id is not None:
        todo_by_id(id)
    elif status is not None:
        todos_by_status(status)
    elif project is not None:
        todos_by_project(project)
    else:
        print_all()


todo.add_command(add)
todo.add_command(workon)
todo.add_command(complete)
todo.add_command(update)
todo.add_command(comment)
todo.add_command(current)
todo.add_command(show)
todo.add_command(archive)


if __name__ == '__main__':
    todo()
