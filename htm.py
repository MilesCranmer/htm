# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from dateutil import parser
import datetime
import numpy as np
import pandas as pd
from copy import deepcopy as copy

from fuzzywuzzy import fuzz

# To add a new column: make sure to add to actual_cols, edit_task, add_task, calc_scores.

# +
def calc_scores(df, a=10):
    def softplus(x, c=1):
        x = x
        if x*c > 10:
            return x
        return np.log(1+np.exp(x*c))/c

    def adjust_repeating(x):
        one_day_past_due = (x['due'] - datetime.datetime.today()).total_seconds() < -24*60*60
        repeating_event = (x['repeat'] > 0.0)

        if one_day_past_due and repeating_event:
            return x['due'] + datetime.timedelta(days=x['repeat'])
        else:
            return x['due']

    df['due'] = df.apply(
        adjust_repeating,
        axis=1
    )

    df['delta'] = df.apply(
        lambda x: (x['due'] - datetime.datetime.today()).total_seconds()/(24*60*60),
        axis=1)

    df['deltap'] = df.apply(
        lambda x: max([softplus(x['delta'], 5), 1e-7]),
        axis=1)

    df['r'] = df.apply(
        lambda x: softplus((a*x['deltap'] - x['etc'])/x['deltap']),
        axis=1
    )

    df['rp'] = df.apply(
        lambda x: softplus((a*x['deltap'] - x['etc'])/x['deltap']**0.5),
        axis=1
    )

    def hour_adjustment(x):
        raw = x['etc']/x['deltap']
        if x['hard'] == 1.0:
            return raw
        elif x['hard'] == 0.5:
            return min([raw, 2.0])
        elif x['hard'] == 0.0:
            return min([raw, 0.25])
        else:
            raise NotImplementedError()
    
    df['hours/day'] = df.apply(
        hour_adjustment,
        axis=1
    )

    df['score'] = df.apply(
        lambda x: (x['need']**2 - x['want']/3.0) * x['hours/day']**2 * (3.0/min([3.0, x['deltap']])*(x['hard'] == 1.0) + float(x['hard'] < 1.0))**0.5,
        axis=1
    )
    
    divisor = np.sum(df.query('hard==1.0 & delta < 7.0')['hours/day'])
    if divisor < 0.1: divisor = 0.1

    multiplier = a/divisor
    df['max_hours/day'] = df.apply(
        lambda x: x['hours/day']*multiplier,
        axis=1
    )

    return df

actual_cols = ['score', 'etc', 'task', 'hours/day', 'max_hours/day', 'due',
         'hard', 'want',
         'need', 'delta',
         'deltap', 'r', 'rp',
         'repeat']
print_cols = ['score', 'etc', 'task', 'hours/day', 'max_hours/day', 'due',
        'hard', 'want', 'delta', 'repeat']

def new_df():
    tasks = {
        'task': [],
        'etc': [],
        'due': [],
        'hard': [],
        'want': [],
        'need': [],
        'repeat': []
    }
    while True:
        task = input("What is the task? ")
        if task in ['', 'q']: break
        etc = input("Estimated hours to completion? ")
        if etc == 'q': break
        due = input("What date is it due? ")
        if due == 'q': break
        hard = input("Is this a hard deadline?\n[1.0 for cutoff/0.5 for soft deadline/0.0 for no deadline] ")
        if hard == 'q': break
        hard = float(hard)
        assert hard in [1.0, 0.5, 0.0]
        print("Importance?")
        print("[0-10; 3~organize computer, 7~finish paper, 8~exam, 9~job application]")
        need = input("")
        if need == 'q': break
        need = float(need)
        print("Repeating? (enter 0 for non-repeating, otherwise the days)")
        repeating = input("")
        repeating = float(repeating)
        assert repeating >= 0.0
        if repeating == 'q': break
        want = 0
        etc = float(etc)
        hard = float(hard)
        due = parser.parse(due)

        tasks['task'].append(task)
        tasks['etc'].append(etc)
        tasks['due'].append(due)
        tasks['hard'].append(hard)
        tasks['want'].append(want)
        tasks['need'].append(need)
        tasks['repeat'].append(repeating)

    df = pd.DataFrame(tasks)
    df = calc_scores(df)
    return df[actual_cols]

def add_tasks():
    old_df = calc_scores(load())
    df = new_df()
    df = pd.concat((old_df, df))
    dump(df)
    return sortload()
    
def update_tasks():
    df = load()
    df = calc_scores(df)
    dump(df)
    return df

def load():
    df = pd.read_csv('~/human_task_manager/tasks.csv', sep='|')
    for i in range(len(df)):
        df.loc[i, 'due'] = parser.parse(df.loc[i, 'due'])
    return df[actual_cols]

def sortload():
    update_tasks()
    df = load()
    return sortdf(df)[actual_cols]

def sortloadhard():
    update_tasks()
    df = load()
    return (sortdf(df)[actual_cols]).query('hard == 1.0')

def get_soon():
    df = sortload()
    df = df.query('(delta < 3.0) & (hard > 0.0)')
    return df

def dump(df):
    df[actual_cols].to_csv('~/human_task_manager/tasks.csv', sep='|')
    
def sortdf(df):
    return df.sort_values('score', ascending=False)

def printstats():
    update_tasks()
    df = load()
    df = calc_scores(df)
    hours = [1, 2, 7, 14, 30]
    days_ahead = {key: [0.0, 0.0, 0.0] for key in hours}
    for i in range(len(df)):
        cur = lambda key: df.loc[i, key]
        hard = {1.0: 0, 0.5: 1, 0.0: 2}[cur('hard')]
        dt = cur('delta')
        etc = cur('etc')

        for hour in hours:
            if dt <= hour:
                days_ahead[hour][hard] += etc

    print("Hard deadlines:")
    for dt in hours:
        print(f"{dt} days in advance, must work {days_ahead[dt][0]/(dt)} hours per day.")
    print("+Soft deadlines")
    for dt in hours:
        print(f"{dt} days in advance, must work {np.sum(days_ahead[dt][:2])/(dt)} hours per day.")
    print("+No deadlines")
    for dt in hours:
        print(f"{dt} days in advance, must work {np.sum(days_ahead[dt])/(dt)} hours per day.")



def print_all():
    df = sortdf(load())
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        print(df[actual_cols])

def print_tasks():
    df = sortdf(load())
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 100):
        print(df['task'])

def print_top():
    print(sortdf(load()).head()[actual_cols])

def edit_task():
    print_tasks()
    fuzzy_exp = input("Enter search string: ")
    df = load()
    all_tasks = list(df['task'])
    best = (0, 0)
    for i in range(len(all_tasks)):
        match = fuzz.ratio(df.loc[i, 'task'], fuzzy_exp)
        if match > best[0]:
            best = (match, i)
    
    print(f"Task: {df.loc[best[1], 'task']}")
    key = input(f"Enter key to edit (task, due, etc, hard, need, repeat): ")
    if key == 'q': return
    val = df.loc[best[1], key]
    print(f"Current {key}={val}")
    new_val = input(f"Enter new {key} (or q to quit) ")
    if new_val == 'q': return
    if key in ['due']:
        new_val = parser.parse(new_val)
    elif key in ['etc', 'hard', 'need', 'repeat']:
        new_val = float(new_val)
    elif key in ['task']:
        ...
    else:
        raise NotImplementedError(f"Can't change {key}") 
    
    df.loc[best[1], key] = new_val
    df = calc_scores(df)
    dump(df)
    return df

def del_tasks():
    print_tasks()
    fuzzy_exp = input("Enter search string: ")
    df = load()
    all_tasks = list(df['task'])
    best = (0, 0)
    for i in range(len(all_tasks)):
        match = fuzz.ratio(df.loc[i, 'task'], fuzzy_exp)
        if match > best[0]:
            best = (match, i)
    
    print(f"Task: {df.loc[best[1], 'task']}")
    etc = input("Remove? (y/n) ")
    if etc == 'y':
        df = df.drop(best[1])
    df = calc_scores(df)
    dump(df)
    return df

def sampler(df, weights):
    weights /= np.sum(weights)
    idxes = np.arange(len(df))
    choice = np.random.choice(idxes, p=weights)
    task = df.loc[choice, 'task']
    hours = df.loc[choice, 'etc']
    print(f"For task \"{task}\", working for 1 hour should finish {100.*1/hours:.2f}%")
    return ""

def samplehours():
    df = load()
    weights = np.array(df['hours/day'])
    return sampler(df, weights)

def sample():
    df = load()
    weights = np.array(df['score'])
    return sampler(df, weights)
# -
