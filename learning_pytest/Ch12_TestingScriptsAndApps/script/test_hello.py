import subprocess

def test_hello():
    result = subprocess.run(["python", "hello.py"], capture_output=True, text=True)
    output = result.stdout
    assert output == "Hello, World!\n"
