#!/public/agis/znjy_group/xianglilingzi/software/miniconda/bin/python

import argparse
import sys
import re

def main():
    parser = argparse.ArgumentParser( description='The screen operation of set A and set B.' )

    parser.add_argument('-ia', '--set_A_file', type=str, required=True, help='Path to an input Set A file' )
    parser.add_argument('-ib', '--set_B_file', type=str, required=True, help='Path to an input Set B file' )
    parser.add_argument('-mode', '--set_mode', type=str, required=True, help='screen mode [union|difference|intersection]' )
    parser.add_argument('-ouv', '--output_union_VCF', type=str, required=False, help='Path to an output union VCF file' )
    parser.add_argument('-oup', '--output_union_position', type=str, required=False, help='Path to an output union position file' )
    parser.add_argument('-odv', '--output_difference_VCF', type=str, required=False, help='Path to an output difference set VCF file' )
    parser.add_argument('-odp', '--output_difference_position', type=str, required=False, help='Path to an output difference set position file' )
    parser.add_argument('-oiv', '--output_intersection_VCF', type=str, required=False, help='Path to an output intersection VCF file' )
    parser.add_argument('-oip', '--output_intersection_position', type=str, required=False, help='Path to an output intersection position file' )
    args = parser.parse_args()

    ia = open(args.set_A_file, 'r')
    ib = open(args.set_B_file, 'r')

    if args.output_union_VCF:
        ouv = open(args.output_union_VCF, 'w')
    else:
        ouv = sys.stdout

    if args.output_union_position:
        oup = open(args.output_union_position, 'w')
    else:
        oup = sys.stdout

    if args.output_difference_VCF:
        odv = open(args.output_difference_VCF, 'w')
    else:
        odv = sys.stdout

    if args.output_difference_position:
        odp = open(args.output_difference_position, 'w')
    else:
        odp = sys.stdout

    if args.output_intersection_VCF:
        oiv = open(args.output_intersection_VCF, 'w')
    else:
        oiv = sys.stdout

    if args.output_intersection_position:
        oip = open(args.output_intersection_position, 'w')
    else:
        oip = sys.stdout

    da={}
    db={}
    pa={}
    pb={}
    dd={}
    du={}
    di={}
    pu={}
    pd={}
    pi={}

    for i in ia:
        if not re.match('#',i):
            a1,a2,a3,a4,a5,a6=i.split('\t',5)
            a7,a8 = re.findall(r'\d\/\d',i)
            da[a1,a2,a4,a5,a7,a8]=i
            pa[a1,a2]=0

    for i in ib:
        if not re.match('#',i):
            a1,a2,a3,a4,a5,a6=i.split('\t',5)
            a7,a8 = re.findall(r'\d\/\d',i)
            db[a1,a2,a4,a5,a7,a8]=i
            pb[a1,a2]=0

    du,dd,di=screen(da,db,args.set_mode)
    pu,pd,pi=screen(pa,pb,args.set_mode)

    if re.search('union',args.set_mode):
        for key in du:
            print(du[key],end='',file=ouv)
        for key in pu:
            print(key[0],key[1],sep='\t',end='\n',file=oup)
    if re.search('difference',args.set_mode):
        for key in dd:
            print(dd[key],end='',file=odv)
        for key in pd:
            print(key[0],key[1],sep='\t',end='\n',file=odp)
    if re.search('intersection',args.set_mode):
        for key in di:
            print(di[key],end='',file=oiv)
        for key in pi:
            print(key[0],key[1],sep='\t',end='\n',file=oip)

def screen(dica,dicb,mode):
    dicu={}
    dicd={}
    dici={}
    for key in dica:
        if re.search('union', mode):
            dicu[key]=dica[key]
        elif re.search('difference', mode) and key not in dicb:
            dicd[key]=dica[key]
        elif re.search('intersection', mode) and key in dicb:
            dici[key]=dica[key]
    for key in dicb:
        if re.search('union', mode):
            dicu[key]=dicb[key]
        elif re.search('difference', mode) and key not in dica:
            dicd[key]=dicb[key]
    return dicu,dicd,dici

if __name__ == '__main__':
    main()
