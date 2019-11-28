#!/usr/bin/env python3
import os
import os.path
import re
import sys
import argparse

import networkx


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output-filepath', default='out.dot')
    parser.add_argument('-F', '--delim', help='input delimiter', default=' +')
    parser.add_argument(
        '--agrpah-prog',
        default='dot',
        type=str,
        help='graph drawing prog (neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp, unflatten)')
    parser.add_argument('-v', '--verbose', action='store_true')

    args, extra_args = parser.parse_known_args()
    options = args

    G = networkx.DiGraph()
    input = sys.stdin
    while True:
        l = input.readline()
        if not l:
            break
        line = l.rstrip(os.linesep)
        nodes = list(
            filter(lambda x: x, re.split(options.delim, line)))
        if len(nodes) == 0:
            continue
        base_node = nodes[0]
        if options.verbose:
            print('base_node:', base_node)
        G.add_node(base_node)
        edges = [[base_node, x] for x in nodes[1:]]
        if len(edges) == 0:
            continue
        G.add_edges_from(edges)
        if options.verbose:
            print('edges:', edges)

    agrpah = networkx.nx_agraph.to_agraph(G)
    agrpah.graph_attr.update(ranksep='5.0')
    agrpah.draw(options.output_filepath, prog=options.agrpah_prog)


if __name__ == '__main__':
    main()
