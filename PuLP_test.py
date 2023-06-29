from pulp import *
from ortoolpy import *

# 問題の初期化
prob = LpProblem("Example_Problem", LpMinimize)

# 変数の定義
x = LpVariable("x", lowBound=0, cat='Integer')
y = LpVariable("y", lowBound=0, cat='Integer')

# 目的関数の定義
prob += 2*x + 3*y

# 制約条件の追加
prob += 4*x + 3*y >= 8
prob += 2*x + 5*y >= 10

# PuLPを使用して問題を解く
status = prob.solve()

# 結果の表示
print("Status:", LpStatus[status])
print("Optimal Solution:")
print("x =", value(x))
print("y =", value(y))
