import click

from genbip.bip import bip
from genbip.generators import GenBipConfiguration, GenBipPrunedConfiguration, GenBipRepeatedConfigurationWhole, GenBipRepeatedConfigurationAsap, GenBipCorrectedConfiguration, GenBipHavelHakimi

@click.command()
@click.option('--top', required=True, type=click.Path(exists=True), help='Path to file for the top degree sequence.')
@click.option('--bot', required=True, type=click.Path(exists=True), help='Path to file for the bottom degree sequence.')
@click.option('--gen', required=True, type=click.Choice(['configuration','pruned','whole','asap','corrected','havelhakimi'], case_sensitive=False), help='Name of the generation method to use.')
@click.option('--seed', type=int, help='Random seed to use with generator.')
@click.option('--swaps', default=0, type=int, help='Number of link swaps to be performed.')
@click.option('--out', default="./out.txt", type=click.Path(), help='Path to file for writting output.')
def cli(top, bot, gen, seed, swaps, out):
    """Generate bi-partite graphs with the prescribed degree sequences."""

    # Instantiate a bip first
    bip_instance = bip.from_files(top, bot)

    if seed is None:
        seed = random.randint(0,10**6)
        print(f"Random seed fixed to {seed}")

    # Instantiate a generator
    generator_mapping = {"configuration": GenBipConfiguration,
                         "pruned": GenBipPrunedConfiguration,
                         "whole": GenBipRepeatedConfigurationWhole,
                         "asap": GenBipRepeatedConfigurationAsap,
                         "corrected": GenBipCorrectedConfiguration,
                         "havelhakimi": GenBipHavelHakimi,
                         }
    generator_instance = generator_mapping[gen](seed=seed)

    # Run the generator on the bip
    generator_instance.run(bip_instance)

    # Write output
    bip_instance.dump(out)

if __name__ == "__main__":
    cli()
