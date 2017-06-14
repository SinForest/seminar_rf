#!/bin/env python3
# -*- coding: utf-8 -*-

import argparse

error_rate = 0.2
moving_reward = 0
gamma = 0.9

A = ["N", "S", "W", "E"]
pretty_A = {}
pretty_A["N"] = "🡹"
pretty_A["S"] = "🡻"
pretty_A["W"] = "🡸"
pretty_A["E"] = "🡺"
pretty_A["X"] = "🞭"

S = {}
S[(0,0)] = "free"
S[(0,1)] = "free"
S[(0,2)] = "free"
S[(0,3)] = "free"

S[(1,0)] = "free"
S[(1,1)] = "block"
S[(1,2)] = "term-"
S[(1,3)] = "term+"

S[(2,0)] = "free"
S[(2,1)] = "free"
S[(2,2)] = "free"
S[(2,3)] = "free"

S[(3,0)] = "free"
S[(3,1)] = "block"
S[(3,2)] = "term-"
S[(3,3)] = "term-"

def target(s, a):
	if a == "N":
		ret = (s[0] - 1, s[1])
	if a == "S":
		ret = (s[0] + 1, s[1])
	if a == "W":
		ret = (s[0], s[1] - 1)
	if a == "E":
		ret = (s[0], s[1] + 1)

	if ret not in S.keys() or S[ret] == "block":
		return s
	else:
		return ret

def turns(a):
	NS = ["N", "S"]
	WE = ["W", "E"]
	if a in NS:
		return WE
	if a in WE:
		return NS
	else:
		return None

def transitions(s, a):
	if S[s] == "free": # normal transition
		ret = [target(s, a)]
		for d in turns(a):
			ret.append(target(s, d))
		return ret

	elif S[s][:4] == "term": #game over state
		return None
	elif S[s] == "block": #blocked state
		return None
	else:
		raise RuntimeError("transition from invalid state type {}".format(S[s]))

def update(extract=False):
	Vv = {}
	for s in S.keys():
		qval = []
		for a in A:
			tran = transitions(s, a)
			if not tran:
				continue
			qval.append( ( 1 - error_rate) * (moving_reward + gamma * V[tran[0]]) +
			                error_rate / 2 * (moving_reward + gamma * V[tran[1]]) +
			                error_rate / 2 * (moving_reward + gamma * V[tran[1]]) )
		if qval:
			Vv[s] = max(qval) if not extract else A[qval.index(max(qval))]
		else:
			Vv[s] = V[s] if not extract else "X"
	return Vv

def print_states(pol=None):
	delim = ("+" + "-" * 8) * 4 + "+"
	for i in range(4):
		print(delim)
		print("|", end="")
		for j in range(4):
			if not pol:
				print(color_me(V[(i,j)], S[(i,j)]), end="|")
			else:
				print("   {}    ".format(pretty_A[pol[(i,j)]]), end="|")
		print()
	print(delim)

def color_me(v, col):
	if col == "free":
		return "{:7.1f} ".format(v)
	elif col == "term-":
		col = "\033[31m"
	elif col == "term+":
		col = "\033[32m"
	elif col == "block":
		col = "\033[36m"
	return "{}{:7.1f} \033[37m".format(col, v)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-r', action="store", dest="reward", type=int)
	parser.add_argument('-g', action="store", dest="gamma", type=float)
	parser.add_argument('-p', action="store_true", default=False, dest="auto_pol")
	results = parser.parse_args()
	if results.reward:
		moving_reward = results.reward
	if results.gamma:
		gamma = results.gamma

	V = {}
	for s in S.keys():
		V[s] = moving_reward
	V[(1,2)] = -100
	V[(1,3)] =  100
	V[(3,2)] = -100
	V[(3,3)] = -100
	V[(1,1)] =    0
	V[(3,1)] =    0

	c = 0;
	print_states()
	while True:
		inp = input()
		if inp == "e":
			exit()
		if inp == "":
			V = update()
			c += 1
			print("Nach {} Iterationen:".format(c))
			print_states()
		if inp == "p" or results.auto_pol:
			print("Policy nach {} Iterationen:".format(c))
			print_states(update(extract=True))
		if results.auto_pol:
			print("\n" + "#"*38)