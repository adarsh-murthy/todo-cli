# TODO

A simple command-line tool to manage todos.

## Set up

Create a new virtual environment and work on it.

```
python3 -m venv venv
source venv/bin/activate
```

## Commands

### Add new todo

`python todo.py add -n <name> -d <description> -p <project>`

### Update a todo

`python todo.py update <id> -n <name> -d <description> -p <project> -c <comment>`

### Start a todo

`python todo.py workon <id>`

### Complete a todo

`python todo.py complete <id>`

### List todos

#### All todos

`python todo.py ls`

#### Filter on status

```
python todo.py ls -s todo
python todo.py ls -s inp
python todo.py ls -s done
```

#### Filter on project

`python todo.py ls -p <project>`

### Archive a todo

`python todo.py archive <id>`
