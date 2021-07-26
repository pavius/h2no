#!/usr/bin/env python3

import argparse

import h2no


def _register_arguments(parser):

    # main command subparser, to which we'll add subparsers below
    subparsers = parser.add_subparsers(dest='command', title='subcommands')

    parser.add_argument(
        '--host',
        type=str,
        help='OpenSprinkler host (e.g. http://10.0.0.1:8080)')

    parser.add_argument(
        '--password',
        type=str,
        help='MD5 hashed OpenSprinkler password')

    # report
    report_parser = subparsers.add_parser('report', help='Creates a PDF report')

    report_parser.add_argument(
        '--days',
        type=int,
        help='Number of days to report on')

    report_parser.add_argument(
        '--output-path',
        type=str,
        help='Path to outputted PDF report')


def _run():

    # create an argument parser
    parser = argparse.ArgumentParser()
    _register_arguments(parser)

    # parse command line arguments
    args = parser.parse_args()
    if not args.command:
        return parser.print_help()

    # get an h2no client
    client = h2no.Client(args.host, args.password)

    if args.command == 'report':
        client.create_report(args.days, args.output_path)


if __name__ == '__main__':
    _run()
