import argparse
import json
import os
from dataclasses import dataclass, asdict


DATA_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    user: str
    description: str
    completed: bool = False


class TaskManager:
    def __init__(self, storage_file=DATA_FILE):
        self.storage_file = storage_file
        self.tasks = self._load()

    def _load(self):
        if not os.path.exists(self.storage_file):
            return []
        with open(self.storage_file, "r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
        return [Task(**item) for item in raw_tasks]

    def _save(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=2)

    def add_task(self, user, description):
        next_id = 1 if not self.tasks else max(task.id for task in self.tasks) + 1
        task = Task(id=next_id, user=user, description=description)
        self.tasks.append(task)
        self._save()
        print(f"Added task #{task.id} for {user}: {description}")

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save()
                print(f"Completed task #{task.id}: {task.description}")
                return
        print(f"Task #{task_id} was not found.")


def build_parser():
    parser = argparse.ArgumentParser(description="Task manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("--user", required=True, help="Account name")
    add_parser.add_argument("--description", required=True, help="Task description")

    complete_parser = subparsers.add_parser(
        "complete-task", help="Mark a task as complete"
    )
    complete_parser.add_argument("--id", type=int, required=True, help="Task id")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add-task":
        manager.add_task(args.user, args.description)
    elif args.command == "complete-task":
        manager.complete_task(args.id)


if __name__ == "__main__":
    main()
