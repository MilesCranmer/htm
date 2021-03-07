# Human Task Manager

I've never been happy with any project management software for personal
to-do items, so I wrote my own as a CLI script. Here's the advantages:
1. Not web-based, just from a script, so it doesn't feel bulky to view tasks/edit things. All command-line based.
2. Tracks deadlines, and calculates how many hours per day you need to work on each task to meet your deadline, based on your estimated # of hours required.
3. Allows you to define how "hard" a deadline is. Is it an actual deadline, or is it just a soft goal you'd like to meet?
4. Allows repeating tasks of arbitrary length.
5. Has a "sampler" which lets you randomly sample tasks based on hours/day or task score, so it makes a long to-do list less intimidating because you just get a few tasks per day to work on.

## Installation

Install `numpy`, `pandas`, and `fuzzywuzzy`.

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

## Commands

Control the task manager from the terminal. All tasks will be stored
in `tasks.csv`. You can use `<ctl-c>` to break out of a command,
or type `q`.

- Print all tasks, sorted by score, with `hp`.
- Add tasks with `ha`.
- Delete a task with `hd`.
- Edit parts tasks with `he`.
- Choose a random tasks, weighted by score, with `hs`.
- Choose a random tasks, weighted by hours/day, with `hsh`.
- Print the tasks due soon with `hsoon`.
- Print statistics about upcoming tasks with `hst`.

For commands requiring you to identify a task, you can use fuzzy search.
e.g., "finish paper" will match to "need to finish paper on X".

For commands requiring a date, you can use generic strings like `Monday`,
`2021-05-01`, `February 1`, etc., and the date parser will try to identify
the date.

## Columns

- `task`: Name of the task.
- `score`: How important it is that you work on the task today.
- `etc`: Estimated time to completion, in hours.
- `hours/day`: How many hours per day you need to work on it to finish by the deadline.
- `due`: When the task is due.
- `hard`: Whether the deadline is hard (1) - meaning a hard deadline, soft (0.5) - meaning you would like to finish by this date, but it's not the end of the world, or nonexistent (0) - meaning it is an arbitrary date you want to aim for.
- `repeat`: Whether to reset the due date after the deadline has passed to this number of days in the future. Useful for weekly/monthly deadly. `0` means no repeat.
