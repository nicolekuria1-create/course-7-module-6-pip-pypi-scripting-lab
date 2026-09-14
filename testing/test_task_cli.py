import json
import sys

from task_cli import TaskManager, main


def test_add_task_saves_to_storage_and_prints_feedback(tmp_path, capsys):
    storage_file = tmp_path / "tasks.json"
    manager = TaskManager(storage_file=str(storage_file))

    manager.add_task("alice", "Write report")

    assert storage_file.exists()
    data = json.loads(storage_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["user"] == "alice"
    assert data[0]["description"] == "Write report"
    assert data[0]["completed"] is False

    output = capsys.readouterr().out
    assert "Added task #1 for alice: Write report" in output


def test_complete_task_marks_task_complete_and_prints_feedback(tmp_path, capsys):
    storage_file = tmp_path / "tasks.json"
    manager = TaskManager(storage_file=str(storage_file))
    manager.add_task("alice", "Write report")
    capsys.readouterr()

    manager.complete_task(1)

    data = json.loads(storage_file.read_text(encoding="utf-8"))
    assert data[0]["completed"] is True

    output = capsys.readouterr().out
    assert "Completed task #1: Write report" in output


def test_complete_task_prints_not_found_when_id_missing(tmp_path, capsys):
    storage_file = tmp_path / "tasks.json"
    manager = TaskManager(storage_file=str(storage_file))

    manager.complete_task(99)

    output = capsys.readouterr().out
    assert "Task #99 was not found." in output


def test_main_add_task_command_creates_task_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "task_cli.py",
            "add-task",
            "--user",
            "bob",
            "--description",
            "Review submission",
        ],
    )

    main()

    storage_file = tmp_path / "tasks.json"
    assert storage_file.exists()
    data = json.loads(storage_file.read_text(encoding="utf-8"))
    assert data[0]["user"] == "bob"
    assert data[0]["description"] == "Review submission"
    assert data[0]["completed"] is False


def test_main_complete_task_command_marks_existing_task_complete(tmp_path, monkeypatch):
    storage_file = tmp_path / "tasks.json"
    storage_file.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "user": "bob",
                    "description": "Review submission",
                    "completed": False,
                }
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        ["task_cli.py", "complete-task", "--id", "1"],
    )

    main()

    data = json.loads(storage_file.read_text(encoding="utf-8"))
    assert data[0]["completed"] is True