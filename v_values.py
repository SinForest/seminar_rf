#!/bin/env python3
# -*- coding: utf-8 -*-

error_rate = 0.2
moving_reward = 0
gamma = 0.9

A = ["N", "S", "W", "E"]

S = {}
S[(0,0)] = "free"
S[(0,1)] = "free"
S[(0,2)] = "free"
S[(0,3)] = "free"

S[(1,0)] = "free"
S[(1,1)] = "full"
S[(1,2)] = "term"
S[(1,3)] = "term"

S[(2,0)] = "free"
S[(2,1)] = "free"
S[(2,2)] = "free"
S[(2,3)] = "free"

S[(3,0)] = "free"
S[(3,1)] = "full"
S[(3,2)] = "term"
S[(3,3)] = "term"

V = {}
for s in S.keys():
	V[s] = 0
V[(1,2)] = -100
V[(1,3)] =  100

V[(3,2)] = -100
V[(3,3)] = -100

def target(s, a):
	if a == "N":
		ret = (s[0] - 1, s[1])
	if a == "S":
		ret = (s[0] + 1, s[1])
	if a == "W":
		ret = (s[0], s[1] - 1)
	if a == "E":
		ret = (s[0], s[1] + 1)

	if ret not in S.keys() or S[ret] == "full":
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

	elif S[s] == "term": #game over state
		return None
	elif S[s] == "full": #blocked state
		return None
	else:
		raise RuntimeError("transition from invalid state")

def update():
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
			Vv[s] = max(qval)
		else:
			Vv[s] = V[s]
	return Vv

def print_states():
	for i in range(4):
		print("-"*33)
		print("|", end="")
		for j in range(4):
			print("{0:7.1f}".format(V[(i,j)]), end="|")
		print()
	print("-"*33)

if __name__ == "__main__":
	print_states()
	while True:
		input()
		V = update()
		print_states()