import subprocess
import pytest


def compare_requirements(left, right):
    return len(set(left.splitlines()) - set(right.splitlines())) == 0


@pytest.mark.parametrize(
    "command,golden_file",
    [
        ("pipfile2req -p tests", "tests/requirements.txt"),
        ("cd tests && pipfile2req", "tests/requirements.txt"),
        ("pipfile2req -p tests -d", "tests/dev-requirements.txt"),
        ("pipfile2req -p tests --hashes", "tests/requirements-hashes.txt"),
        ("pipfile2req -p tests Pipfile", "tests/requirements-pipfile.txt"),
        ("pipfile2req -d tests/Pipfile", "tests/dev-requirements-pipfile.txt"),
        ("pipfile2req -d tests/Pipfile.lock", "tests/dev-requirements.txt"),
    ],
)
def test_convert_pipfile(command, golden_file):
    proc = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, err = proc.communicate()
    with open(golden_file) as f:
        assert compare_requirements(output.decode("utf-8").strip().replace(
            "\r\n", "\n"
        ), f.read().strip().replace("\r\n", "\n"))
