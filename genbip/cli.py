import random
import click
from collections import Counter
import numpy as np
import ipdb

from genbip.bip import bip
from genbip.generators import GenBipConfiguration, GenBipPrunedConfiguration, GenBipRepeatedConfigurationWhole, GenBipRepeatedConfigurationAsap, GenBipCorrectedConfiguration, GenBipHavelHakimi
from genbip.anomalyGenerator import *

@click.command()
@click.option('--top', required=True, type=click.Path(exists=True), help='Path to file for the top degree sequence.')
@click.option('--bot', required=True, type=click.Path(exists=True), help='Path to file for the bottom degree sequence.')
@click.option('--gen', required=True, type=click.Choice(['configuration','pruned','whole','asap','corrected','havelhakimi'], case_sensitive=False), help='Name of the generation method to use.')
@click.option('--seed', type=int, help='Random seed to use with generator.')
@click.option('--n_anomaly', type=int, help='number of nodes in anomaly')
@click.option('--m_anomaly', type=int, help='number of edges in anomaly')
@click.option('--swaps', default=0, type=int, help='Number of link swaps to be performed.')
@click.option('--out', default="./out.txt", type=click.Path(), help='Path to file for writting output.')
def cli(top, bot, gen, seed, n_anomaly, m_anomaly, swaps, out):
    """Generate bi-partite graphs with the prescribed degree sequences."""
    if seed is None:
        seed = random.randint(0,10**6)
        np.random.seed(seed)
        print(f"Random seed fixed to {seed}")

    print('generating anomaly')
    an_bip, edges = generate_anomaly(n_anomaly, m_anomaly)

    # Instantiate a bip first
    print('reading real data')
    bip_instance = bip.from_files(top, bot)
    print('adding anomaly to stream')
    anomaly_edges = select_nodes_anomaly(an_bip, bip_instance, edges)
    #ipdb.set_trace()




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
    print('generating normality')
    generator_instance.run(bip_instance)
    print('checking multiple edges')
    multiple_edges = check_multiple_edges(bip_instance, anomaly_edges)
    print(' {} multiple edges'.format(len(multiple_edges)))
    target_multiple_edges(bip_instance, an_bip, anomaly_edges, multiple_edges)
    multiple_edges = check_multiple_edges(bip_instance, anomaly_edges)


    # Write output
    bip_instance.dump(out)

@click.command()
@click.option("--edgelist",   required=True,           type=click.Path(exists=True),  help="Path to file with the list of links.")
@click.option("--top_output", default="./top_out.txt", type=click.Path(),             help="Path to export top degree sequence.")
@click.option("--bot_output", default="./bot_out.txt", type=click.Path(),             help="Path to export bot degree sequence.")
@click.option("--sep",        default=" ",             type=str,                      help="Seperator string to use.")
@click.option("--sort",       default="unsorted",      type=click.Choice(["unsorted","degree","degree-reverse","label", "label-numeric"], case_sensitive=False), help="Sort method for sequences.")
def genseq(edgelist, top_output, bot_output, sep, sort):
    """Generate the top and bottom degree sequences from a edge list file."""
    top,bot = Counter(),Counter()
    with open(edgelist,"r") as fp:
        for line in fp:
            u,v = line.strip().split(sep)
            top.update([u])
            bot.update([v])
    for out,holder in zip([top_output,bot_output], [top,bot]):
        with open(out,"w") as fp:
            if sort == "degree-reverse":
                for u,d in holder.most_common():
                    fp.write(f"{u}{sep}{d}\n")
            elif sort == "degree":
                for u,d in holder.most_common()[::-1]:
                    fp.write(f"{u}{sep}{d}\n")
            elif sort == "label":
                for u,d in sorted(holder.items(), key=lambda x:x[0]):
                    fp.write(f"{u}{sep}{d}\n")
            elif sort == "label-numeric":
                for u,d in sorted(holder.items(), key=lambda x:int(x[0])):
                    fp.write(f"{u}{sep}{d}\n")
            else:
                for u,d in holder.items():
                    fp.write(f"{u}{sep}{d}\n")
if __name__ == "__main__":
    cli()
