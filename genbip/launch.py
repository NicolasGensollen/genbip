import os
import click
import random
import logging
import argparse
import numpy as np

from genbip.utils import *
from genbip.bip import bip
from collections import Counter
from genbip.anomalyGenerator import *
from genbip.generators import GenBipConfiguration, GenBipPrunedConfiguration, GenBipRepeatedConfigurationWhole, GenBipRepeatedConfigurationAsap, GenBipCorrectedConfiguration, GenBipHavelHakimi



def anomaly_arguments(parser):
    """ add optional arguments to generate 'anomaly'"""
    parser.add_argument('-tan', '--top_anomaly', type=str,
            help='path to the "anomaly" top degree sequence')
    parser.add_argument('-ban', '--bot_anomaly', type=str,
            help='path to the "anomaly" bot degree sequence')
    parser.add_argument('--accept_multiedge', action='store_true', default=False,
            help='if enable, accept multi edge in output bipartite graph')

def normality_arguments(parser):
    """ add required arguments to generate 'normality'"""
    parser.add_argument('top_normality', type=str,
            help='path to the "normality" top degree sequence')
    parser.add_argument('bot_normality', type=str,
            help='path to the "normality" bot degree sequence')
    parser.add_argument('generator', type=str, default='havelhakimi',
            choices=['configuration','pruned','whole','asap','corrected','havelhakimi'],
            help='generator used to create the bipartite graph')
    parser.add_argument('--swaps', default=0, type=int,
            help='number of edge swaps to perform after generation')
    return parser

def cli():
    """Generate bi-partite graphs with the prescribed degree sequences."""
    """def cli(top_normality, bot_normality, top_anomaly, bot_anomaly, gen, seed, swaps, out):"""
    parser = argparse.ArgumentParser(description='link stream metrics')
    normality_arguments(parser)
    anomaly_arguments(parser)

    # general arguments
    parser.add_argument('--seed', type=int,
            help='random seed to use with generator')
    parser.add_argument('--out', default='./', type=str,
            help='path to folder output')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
            help='enable to be more verbose')
    # read parameters
    args = parser.parse_args()

    # instantiate logger
    if args.verbose:
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M'
                )
    else:
        logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M'
                )

    # instantiate logger
    logger = logging.getLogger()


    # Use random seed
    if args.seed is None:
        seed = random.randint(0,10**6)
        np.random.seed(seed)
        logger.info(f"Random seed fixed to {seed}")
    else:
        seed = args.seed


    # Instantiate a bip first
    logger.info('reading dataset')

    normal_bip = bip.from_files(args.top_normality, args.bot_normality, keep_idx=True)


    # Instantiate a generator
    generator_mapping = {"configuration": GenBipConfiguration,
                         "pruned": GenBipPrunedConfiguration,
                         "whole": GenBipRepeatedConfigurationWhole,
                         "asap": GenBipRepeatedConfigurationAsap,
                         "corrected": GenBipCorrectedConfiguration,
                         "havelhakimi": GenBipHavelHakimi,
                         }
    generator_instance = generator_mapping[args.generator](seed=args.seed)

    # Run the generator on the "normality" bip
    logger.info('generating normality')
    generator_instance.run(normal_bip)

    # Run the generator on the "anomaly" bip if input given
    if args.top_anomaly:
        logger.info('generating anomaly')

        #anomalyGenerator = AnomalyGenerator(n_anomaly, m_anomaly)
        #an_bip, edges = anomalyGenerator.generate_anomaly()

        anomaly_bip = bip.from_files(args.top_anomaly, args.bot_anomaly, keep_idx=True)
        generator_instance.run(anomaly_bip)
        mappers = map_bip_names(anomaly_bip, normal_bip)
        if not args.accept_multiedge:
            multiple_edges = check_multiple(normal_bip, anomaly_bip, mappers)
            if len(multiple_edges) > 0:
                logger.debug('number of multiple edges: {}'.format(len(multiple_edges)))
                swap_multiple(normal_bip, anomaly_bip, multiple_edges, mappers)


        output_anomaly = os.path.join(args.out, 'anomaly_bip.txt')
        logger.info('writing anomaly bip to {}'.format(output_anomaly))
        anomaly_bip.dump(output_anomaly)

        # to check multiple edges increment in each, some kind of DTW, it top bip is lower increment this one, else increment the other, and compare the edges
        #check_multiple_edges()
        #print('checking multiple edges')
        #multiple_edges = anomalyGenerator.check_multiple_edges(bip_instance, anomaly_edges)
        #print(' {} multiple edges'.format(len(multiple_edges)))
        #anomalyGenerator.target_multiple_edges(bip_instance, an_bip, anomaly_edges, multiple_edges)
        #multiple_edges = anomalyGenerator.check_multiple_edges(bip_instance, anomaly_edges)

    # mappers : top_an2norm, top_norm2an, bot_an2norm, bot_norm2an =  




    # Write output
    output_normal = os.path.join(args.out, 'normal_bip.txt')
    logger.info('writing normality bip to {}'.format(output_normal))
    normal_bip.dump(output_normal)

if __name__ == "__main__":
    cli()
