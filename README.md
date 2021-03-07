# Human Task Manager

## Installation

Clone the repo.

Add the following macros to your `.bashrc` file,
and replace the location of the repo to `DIR`

```bash
htm() {
    cPWD=$(pwd)
    cd DIR
    python -c "from htm import *; print($1)"
    cd $cPWD
}
# For piping
htmp() {
    cPWD=$(pwd)
    cd DIR
    python -c "from htm import *; print($1.to_markdown())"
    cd $cPWD
}
alias hs='htm "sample()"'
alias hsh='htm "samplehours()"'
alias he='htm "edit_task()"'
alias hp='htm "sortload()[print_cols]"'
alias hph='htm "sortloadhard()[print_cols]"'
alias ha='htm "add_tasks()"'
alias hd='htm "del_tasks()"'
alias hst='htm "printstats()"'
alias hsoon='htm "get_soon()"'
alias hpp='htmp "sortload()"'
```

## How to use.

Control the task manager from the terminal. All tasks will be stored
in `tasks.csv`.

- Add tasks with `ha`.
- Edit tasks with `hp`.
- Delete a task with `hd`.
- Print all tasks, sorted by score, with `hp`.
- Choose a random tasks, weighted by score, with `hs`.
- Choose a random tasks, weighted by hours/day, with `hsh`.
- Print the tasks due soon with `hsoon`.
- Print statistics about upcoming tasks with `hst`.
