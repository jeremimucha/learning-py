import sums


def test_sums(capsys):
    sums.main()
    output = capsys.readouterr().out
    assert output == "200.00\n"
