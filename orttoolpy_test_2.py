from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

# SparkSessionの作成
spark = SparkSession.builder.getOrCreate()

# データの定義
weights = [10, 15, 8, 12, 6, 14]
capacities = [30, 40, 25]
num_trucks = len(capacities)
num_items = len(weights)

# データフレームの作成
df = spark.createDataFrame([(i, j) for i in range(num_items) for j in range(num_trucks)], ["item", "truck"])
df = df.withColumn("weight", spark_sum(spark.when(df["item"] == i, weights[i]) for i in range(num_items)))

# 目的関数を計算するための列を追加
df = df.withColumn("weight_x", df["weight"] * df["x"])

# 制約条件を追加
df_grouped = df.groupBy("truck").agg(spark_sum(df["weight_x"]).alias("total_weight"))
df = df.join(df_grouped, "truck")
df = df.withColumn("capacity_constraint", df["total_weight"] <= spark_sum(spark.when(df["truck"] == j, capacities[j]) for j in range(num_trucks)))

# 解決
solution = df.groupBy("truck").agg(spark_sum(df["weight_x"]).alias("total_weight"))
objective_value = solution.select(spark_sum(solution["total_weight"])).first()[0]

# 結果の表示
print("Objective:", objective_value)
solution.show()
