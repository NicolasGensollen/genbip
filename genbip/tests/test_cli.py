import os

from click.testing import CliRunner
from genbip.cli import cli, genseq

current_directory = os.path.realpath(os.path.dirname(__file__))

def test_cli():
	runner = CliRunner()
	result = runner.invoke(cli, [f"--top={os.path.join(current_directory, 'data/toy_1/toy_top.gz')}",
				     f"--bot={os.path.join(current_directory, 'data/toy_1/toy_bot.gz')}",
				     "--gen=asap", "--seed=123", "--swaps=0",
				     f"--out={os.path.join(current_directory, 'out.txt')}"])
	assert result.exit_code == 0
	expected_output = ["c beta\n","c alpha\n","c gamma\n","d alpha\n","d delta\n","a gamma\n","a beta\n","b delta\n"]
	with open(os.path.join(current_directory, "out.txt"),"r") as fp:
		output = fp.readlines()
	assert output == expected_output
	# Cleaning...
	os.remove(os.path.join(current_directory, "out.txt"))

def test_cli_genseq():
    runner = CliRunner()
    result = runner.invoke(genseq, [f"--edgelist={os.path.join(current_directory, 'data/toy_1/toy.edgelist')}",
                                    f"--top_output={os.path.join(current_directory, 'top_out.txt')}",
                                    f"--bot_output={os.path.join(current_directory, 'bot_out.txt')}",
                                     "--sort=degree-reverse"])
    assert result.exit_code == 0
    expected_output_top = ["c 3\n","a 2\n","d 2\n","b 1\n"]
    expected_output_bot = ["alpha 2\n","gamma 2\n","beta 2\n","delta 2\n"]
    with open(os.path.join(current_directory, "top_out.txt"), "r") as fp:
        output_top = fp.readlines()
    assert output_top == expected_output_top
    with open(os.path.join(current_directory, "bot_out.txt"), "r") as fp:
        output_bot = fp.readlines()
    assert output_bot == expected_output_bot
    # Cleaning...
    os.remove(os.path.join(current_directory, 'top_out.txt'))
    os.remove(os.path.join(current_directory, 'bot_out.txt'))

