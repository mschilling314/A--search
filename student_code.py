from tkinter import Y
import common


MOVES = [[-1, 0], [1, 0], [0, -1], [0, 1]] # up down left right


class Node:
	def __init__(self, location, parent=None, val=0, depth=0):
		self.loc = location
		self.par = parent
		self.val = val
		self.dep = depth


def bounds_check(loc):
	if loc[0] < 0 or loc[0] >= common.constants.MAP_HEIGHT:
		return False
	if loc[1] < 0 or loc[1] >= common.constants.MAP_WIDTH:
		return False
	return True


def manh(loc1, loc2):
	y = loc2[0] - loc1[0]
	x = loc2[1] - loc1[1]
	if x < 0:
		x = -x
	if y < 0:
		y = -y
	return x + y


def vc(loc, board):
	n = board[loc[0]][loc[1]]
	if n == 4:
		return True
	return False


def gc(loc, board):
	n = board[loc[0]][loc[1]]
	if n == 3:
		return True
	return False


def sc(loc, board):
	n = board[loc[0]][loc[1]]
	if n == 0:
		return True
	return False


def find_start(board):
	for i in range(common.constants.MAP_HEIGHT):
		for j in range(common.constants.MAP_WIDTH):
			n = board[i][j]
			if n == 2:
				return [i, j]
	else:
		raise Exception("Start not found")


def find_goal(board):
	for i in range(common.constants.MAP_HEIGHT):
		for j in range(common.constants.MAP_WIDTH):
			n = board[i][j]
			if n == 3:
				return [i, j]
	else:
		raise Exception("Goal not found")


def loc_add(loc1, loc2):
	y = loc1[0] + loc2[0]
	x = loc1[1] + loc2[1]
	return [y, x]


def expand(loc, board):
	res = []
	for mov in MOVES:
		m = loc_add(loc, mov)
		if bounds_check(m):
			if sc(m, board) or gc(m, board):
				res.append(m)
	return res


def front_add(frontier, lol, par, g):
	# for each location in possible locations
	for l in lol:
		# find the value of the location
		v = par.dep + manh(l, g)
		# create a node
		n = Node(l, par, v, par.dep+1)
		# make an iterator
		i = 0
		nf = True
		while i < len(frontier) and nf:
			fv = frontier[i].val
			if fv > v:
				nf = False
				frontier.insert(i, n)
			i += 1
		if i == len(frontier):
			frontier.append(n)
	return frontier


def print_board(board):
	for x in board:
		print(x)


def print_frontier(frontier):
	for el in frontier:
		print(el.loc, el.val)


def astar_search(board):
	found = False
	curr_l = find_start(board)
	goal_loc = find_goal(board)
	ini = Node(curr_l, None, manh(curr_l, goal_loc))
	frontier = [ini]
	while len(frontier) != 0 and not found:
		curr = frontier.pop(0)
		if not vc(curr.loc, board):
			if gc(curr.loc, board):
				# handling for goal
				found = True
				n = curr
				while n is not None:
					board[n.loc[0]][n.loc[1]] = 5
					n = n.par
			else:
				lols = expand(curr.loc, board)
				frontier = front_add(frontier, lols, curr, goal_loc)
				board[curr.loc[0]][curr.loc[1]] = 4
	return found
