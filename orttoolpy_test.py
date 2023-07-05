from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from ortoolpy import addvars, addvals, addbinvars

# 問題の初期化
problem = LpProblem("Truck Loading Problem", LpMinimize)

# データの定義
weights = [10, 15, 8, 12, 6, 14]  # 荷物の重さ
capacities = [30, 40, 25]  # トラックの容量
num_trucks = len(capacities)
num_items = len(weights)

# 変数の作成
x = addbinvars(num_items, num_trucks)  # 荷物をトラックに割り当てる変数

# 目的関数
problem += lpSum(weights[i] * x[i][j] for i in range(num_items) for j in range(num_trucks))

# 制約条件
# 各荷物はちょうど1つのトラックに割り当てられる
for i in range(num_items):
    problem += lpSum(x[i][j] for j in range(num_trucks)) == 1

# トラックの容量制約
for j in range(num_trucks):
    problem += lpSum(weights[i] * x[i][j] for i in range(num_items)) <= capacities[j]

# 問題の解決
problem.solve()

# 結果の表示
print("Objective:", problem.objective.value())
for j in range(num_trucks):
    truck_items = [i for i in range(num_items) if x[i][j].varValue == 1]
    print(f"Truck {j+1}:", truck_items)

