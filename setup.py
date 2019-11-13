import os 
import sys
import time
import numpy as np
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-n", "--number", help="Number of nodes.", required=False, type=int, default=4)

    args = parser.parse_args()
    
    if args.number > 4:
        print('The number of nodes should not be more than 4.')
        sys.exit()
    elif args.number < 4:
        print('The number of nodes should not be less than 4(3f+1).')
        sys.exit()

    # ports setting
    # [12, 13, 14, 1x, 23, 24, 2x, 34, 3x, 4x]
    # output_ports = np.random.choice(total_ports, total_number, replace=False)
    total_ports = range(10000,10010)
    
    client_port = 10010

    t = [ str(port) for port in total_ports]
    op_ports = []
    op_ports.append([ [t[0], t[1], t[2]], [t[3]] ])
    op_ports.append([ [t[4], t[5]], [t[0], t[6]] ])
    op_ports.append([ [t[7]], [t[1], t[4], t[8]] ])
    op_ports.append([ [], [t[2], t[5], t[7], t[9]] ])

    CP_op_ports = [t[3], t[6], t[8], t[9]]

    # output command
    print('\nserver : command')
    print('='*17)
    print('cd control_panel/')
    print('\t python3 main.py -n {} -lsp {}'.format(args.number, ' '.join(CP_op_ports)))

    print('\ncd real_estate_agents/')
    for id in range(args.number):
        if id == 0:
            print('\t python3 main.py -p True -n {} -crp {} -conp {} -clip {}'\
                        .format(args.number, ' '.join(op_ports[id][0]), ' '.join(op_ports[id][1]), client_port))
        elif id == args.number - 1:
            print('\t python3 main.py -p False -n {} -conp {}'\
                        .format(args.number,' '.join(op_ports[id][1])))
        else:
            print('\t python3 main.py -p False -n {} -crp {} -conp {}'\
                        .format(args.number, ' '.join(op_ports[id][0]), ' '.join(op_ports[id][1])))
        
    print('='*17+'\n')