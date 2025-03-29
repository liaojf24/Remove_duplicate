"""
This script aims to remove duplicates from raw fasta
@date: 2025.03.29
@author: Jiafeng Liao
@affliation: Xiong lab, ZJU
"""

import pandas as pd
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser(description="This is a parameters.")
parser.add_argument("--raw", type = str, default = '../data/raw.fasta',
                    help="the path of raw fasta") 
parser.add_argument("--blast", type= str, default = '../data/blast_results.txt',
                    help="path of blast results")  
parser.add_argument("--output", type = str, default = '../results/filtered.txt',
                   help="path of output file")
args = parser.parse_args()

def main():
  blast_results = pd.read_csv(args.blast, header=None, sep='\t')
  blast_id = blast_results[[0,1]]
  
  unique_sequences = []
  with open(args.raw, 'r') as file:
      sequences = file.readlines()
  tx_id = sequences[::1]

  # used_nodes = used_ids
  used_nodes = set()
  selected_nodes = set()
  # greedy algorithms
  for i in tqdm(range(blast_id.shape[0])):
      u,v = blast_id.iloc[i][0], blast_id.iloc[i][1]
      if u not in used_nodes and v not in used_nodes:
          selected_nodes.add(u)
          # 标记与这个节点相连的节点
      used_nodes.add(u)
      used_nodes.add(v)
  
  ## blast里的Id和 没有在blast里的Id结合
  all_id = []
  for each in sequences[::2]:
      all_id.append(each[1:].strip())
  non_blast_id =  set(all_id)  - set(list(blast_id[0]))
  filtered_id = non_blast_id | selected_nodes
  
  # # 挑选序列
  s80_data = pd.read_csv(args.raw, header=None, sep='\t')
  f = open(args.output, 'w')
  for each in tqdm(filtered_id):
      id = each.split('(')[0]
      start = each.split('(')[1].split(',')[0]
      end =  each.split(',')[1][:-1]
      d = s80_data[ (s80_data[0] == id) & (s80_data[2] == int(start)) & (s80_data[3] == int(end))].iloc[0]
      f.write('\t'.join(map(str, d)) + '\n')
  main()

