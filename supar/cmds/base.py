# -*- coding: utf-8 -*-

import torch
from supar.utils import Config
from supar.utils.logging import init_logger
from supar.utils.parallel import init_device


def parse(parser):
    parser.add_argument('--path', '-p', default=None,
                        help='path to model file')
    parser.add_argument('--conf', '-c', default='config.ini',
                        help='path to config file')
    parser.add_argument('--device', '-d', default='-1',
                        help='ID of GPU to use')
    parser.add_argument('--seed', '-s', default=1, type=int,
                        help='seed for generating random numbers')
    parser.add_argument('--threads', '-t', default=16, type=int,
                        help='max num of threads')
    parser.add_argument('--batch-size', default=5000, type=int,
                        help='batch size')
    parser.add_argument('--buckets', default=32, type=int,
                        help='max num of buckets to use')
    args, unknown = parser.parse_known_args()
    args, _ = parser.parse_known_args(unknown, args)
    args = Config(args.conf).update(vars(args))
    Parser = args.pop('Parser')

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed)
    init_device(args.device)
    args.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger = init_logger(path=args.path)
    logger.info('\n' + str(args))

    if args.mode == 'train':
        parser = Parser.build(**args, logger=logger)
        parser.train(**args, logger=logger)
    elif args.mode == 'evaluate':
        parser = Parser.load(args.path)
        parser.evaluate(**args)
    elif args.mode == 'predict':
        parser = Parser.load(args.path)
        parser.predict(**args)
