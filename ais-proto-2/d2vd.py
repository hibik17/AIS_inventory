# -*- coding:utf-8 -*-
"""
d2vdのメイン処理。引数を解析してBottleサーバーを立ち上げる。
$ python d2vd.py --model モデル名  --port ポート
"""
from bottle_server import BottleServer
from ipsj_model import IpsjModel
from argparse import ArgumentParser

def main_proc(args):
    '''
    メイン処理。
    '''
    # Loading Model
    print("Loading model: " + args.model_name)
    model = IpsjModel(args.model_name)

    # Start Bottle server
    bottle_server = BottleServer(model=model, host='0.0.0.0', port=args.port)
    bottle_server.start()

def parse_args():
    '''
    引数の解析
    '''
    desc = u'{0} [Args] [Options]\nDetailed options -h or --help'.format(__file__)
    parser = ArgumentParser(description=desc)
    parser.add_argument("--port", dest="port",
                    default=57007, type=int,
                    help="port number of server")
    parser.add_argument("--model", dest="model_name",
                    default="d2v_ipsj_desc", type=str,
                    help="prefix of model files to be stored")

    return parser.parse_args()

# Call main procedure
if __name__ == '__main__':
    args = parse_args()
    main_proc(args)
