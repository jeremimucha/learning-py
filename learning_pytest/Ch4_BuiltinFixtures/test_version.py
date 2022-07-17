import subprocess
from typer.testing import CliRunner
import cards


# Without using the `capsys` fixture, we're pretty much left with no other option
# than to run the cli in a subprocess and capture the stdout that way.
def test_version_v1():
    process = subprocess.run(
        ["cards", "version"], capture_output=True, text=True
    )
    output = process.stdout.rstrip()
    assert output == cards.__version__

# On the other hand using capsys we can just test the cli function directly
def test_version_v2(capsys):
    cards.cli.version()
    # capsys.readouterr() -> (out, err) -- tuple of stdout and stderr output
    output = capsys.readouterr().out.rstrip()
    assert output == cards.__version__


# Yet another, better, way of testing the CLI when using `typer` is to rely on
# CliRunning prividing output hooks:
def test_version_v3():
    runner = CliRunner()
    result = runner.invoke(cards.app, ["version"])
    output = result.output.rstrip()
    assert output == cards.__version__

