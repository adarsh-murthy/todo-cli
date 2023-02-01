# TODO

A simple command-line tool to manage todos.

## Set up

### Python virtualenv

Create a new virtual environment and work on it.

```
python3 -m venv venv
source venv/bin/activate
```

## Commands

### Add new todo

`python todo.py add -n <name> -d <description> -p <project>`

### Update a todo

`python todo.py update <id> -n <name> -d <description> -p <project>

### Start a todo

`python todo.py workon <id>`

### Complete a todo

`python todo.py complete <id>`

### Comment on a todo

`python todo.py comment <id> <comment>`

### List todos

#### All todos

`python todo.py show`

#### Filter on status

```
python todo.py show -s todo
python todo.py show -s inp
python todo.py show -s done
```

#### Filter on project

`python todo.py show -p <project>`

### Archive a todo

`python todo.py archive <id>`

## Docker

You can also dockerize this CLI app.

### Build

`docker image build -t gtd:latest .`

### Create local .gtd.json file

`touch /path/to/.gtd.json`

### bashrc updates

Add the following to your `.bashrc` and source it or open a new terminal.

NOTE: This is a one time action.

```
function gtd() {
  docker run -v /path/to/.gtd.json:/.gtd.json gtd:latest "@"
}
```

### Usage

`gtd --help`
