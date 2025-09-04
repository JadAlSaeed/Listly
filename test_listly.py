import pytest
import json
import os
from listly import tasks, save, load, add, update, done, remove, date

@pytest.fixture(autouse = True)
def setup():
    global tasks
    tasks.clear()
    save()

def test_add():
    description = "buy groceries"
    add(description)
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1 
    assert tasks[0]["description"] == description
    assert tasks[0]["status"] == "in-progress"
    assert tasks[0]["due_date"] == "not-set"
    assert tasks[0]["priority"] == "low"
    load()
    assert tasks[0]["description"] == description


def test_update():
    add("buy dinner")
    new_desc = "buy a new laptop"
    update(2, new_desc)
    for task in tasks:
        if task["id"] == 2:
            assert task["description"] == new_desc
            load()
            assert task["description"] == new_desc

def test_done():
    add("buy a new desktop")
    done(3)
    for task in tasks:
        if task["id"] == 3:
            assert task["status"] == "done"
            load()
            assert task["status"] == "done"

def test_remove():
    add("water the plants")
    remove(4)
    assert len(tasks) == 0
    load()
    assert len(tasks) == 0

def test_date():
    date(1, "2025-12-15")
    for task in tasks:
        if task["id"] == 1:
            assert task["due_date"] == "2025-12-15"