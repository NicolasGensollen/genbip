import os

from click.testing import CliRunner
from genbip.cli import cli

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
