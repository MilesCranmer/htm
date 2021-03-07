# human_task_manager

How to use.

Set every task you need to do for work/chores,
that takes longer than 1 hour, and is not email, into
this program. Give an estimate for hours it will take,
and periodically update this estimate as you complete
the task by using the `he` macro to edit the task (`h` for
human task manager, `e` for edit).

Hard tasks are those with hard deadlines - e.g., a paper
will not be accepted past the date. 0.5 hardness
is used for a personal deadline made with another person,
but is not as hard. 0.0 hardness is a task that has no
hard cutoff at the date specified.

Use `hs` to sample a task based on score. Use `hsh` to sample a task
based on how many hours you need to work on it per day before it
is due. I usually do half-half between these, and tabulate
the samples for the day: e.g., spend 3 hours on X task, 2 hours on Y, etc.

Use `hp` to print a view of all your tasks.

Use `hst` to print statistics on your workload over the next 30 days,
giving how many hours you need to work per day in each time frame.

If the workload only shows a small number of hours to work per day,
consider giving yourself more soft deadlines - e.g., set a goal
with a supervisor to work towards.

## Scoring

Scoring is square with the number of hours/day required, as tasks
that are sooner should be have more time dedicated to them.

Tasks which are late, but hard=0.5, are assigned
a max of 3 hours/day. Tasks with hard=0.0 which are late
have a max of 30 minutes/day.

## TODO

- Underline task due tomorrow.
- State how many hours/day we have to work in next day, 7 days in order to finish all goals.
