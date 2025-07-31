# Getting started

Task-cli is a command line python app built under UV and using [Click](https://click.palletsprojects.com/en/stable/) for keeping track of tasks. Tasks are stored in Json. Just a simple test project

Clone the repository

`git clone https://github.com/DeusWyvern/task-cli.git`

CD into the folder

`cd task-cli`

Setup dependencies and Run the cli with

`uv run task-cli`

Alternatively to run without uv run for the session

`source .venv/bin/activate`

## Usage
`task-cli [OPTIONS] <PATH> COMMAND [ARGS]`

Example

`task-cli --file 'tasks' ~/Documents add "Make a task list"`

`task-cli --file 'tasks' ~/Documents list todo`

To get more help type

`task-cli --help`
