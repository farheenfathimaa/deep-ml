import pandas as pd
import numpy as np

df = pd.DataFrame({
    "fare": [100, 200, None, 300, 500]
})

df_original = df.copy() # copying the original


# 1. Fill missing values with the median
df["fare"] = df["fare"].fillna(df["fare"].median())
print(df)
print("\n-------\n")
'''
output:
0    100.0
1    200.0
2    250.0
3    300.0
4    500.0
'''

# 2. Drop missing rows and duplicates
df = pd.DataFrame({
    "zone": ["A", "B", None, "A"],
    "fare": [100, 200, 300, 100]
})
df_original = df.copy()
df = df.dropna(subset = ["zone"]).drop_duplicates()
print(df)
print("\n-------\n")

'''
output:
  zone  fare
0    A   100
1    B   200
'''

# 3. Calculate IQR (Interquartile Range)
fare = pd.Series([10, 20, 30, 40, 50, 60, 70, 80])
q1, q3 = fare.quantile([0.25, 0.75])
iqr = q3 - q1

print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("\n-------\n")

'''
notes: iqr measures the spread of the middle 50% of your data.

output:

Q1: 27.5
Q3: 62.5
IQR: 35.0

'''

# 4. Remove outliers using IQR
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

clean = fare[fare.between(lower, upper)]

print("Lower:", lower)
print("Upper:", upper)
print("Clean:", clean.tolist())
print("\n-------\n")

'''
notes: between() keeps rows whose fare falls within those limits (inclusive).

output:
Lower: 50.0
Upper: 250.0
Clean: [50, 60, 70, 80]
'''

# 5. Group data and calculate statistics
df = pd.DataFrame({
    "zone": ["A", "A", "B", "B", "B"],
    "fare": [100, 200, 300, 400, 500]
})
df_original = df.copy()
summary = df.groupby('zone').agg(
    n = ('fare', 'size'),
    avg = ('fare', "mean")
    ).reset_index()
print(summary)
print("\n-------\n")

'''
notes: agg() calculates the number of records (n) and average fare (avg) for each zone.

output:
  zone  n    avg
0    A  2  150.0
1    B  3  400.0
'''

# 6. Merge two DataFrames (JOIN)
clean = pd.DataFrame({
    "zone": ["A", "B", "C"],
    "fare": [100, 200, 300]
})

zones = pd.DataFrame({
    "zone": ["A", "B"],
    "city": ["Hyderabad", "Mumbai"]
})
merged = clean.merge(zones, on = 'zone', how = 'left')
print(merged)
print("\n-------\n")

'''
notes:
- merge() combines two DataFrames using a common column (zone).
- how="left" keeps every row from clean, even if there is no matching zone in zones.

output:
  zone  fare       city
0    A   100  Hyderabad
1    B   200     Mumbai
2    C   300        NaN
'''

# 7. Resample data monthly
df = pd.DataFrame({
    "d": pd.to_datetime([
        "2026-01-05",
        "2026-01-20",
        "2026-02-10",
        "2026-02-15"
    ]),
    "fare": [100, 200, 300, 400]
})

monthly = df.set_index('d').resample('MS')['fare'].sum()
print(monthly)
print("\n-------\n")

'''
notes:
- set_index("d") makes the date column the DataFrame index.
- resample("MS") groups records by month-start frequency, and sum() calculates monthly fare totals.

output:
d
2026-01-01    300
2026-02-01    700
Freq: MS, Name: fare, dtype: int64
'''

# 8. Create a 2D array
a = np.array([[1,2],[3,4]])
print(a)
print(a.shape)
print("\n-------\n")

'''
notes: np.array() converts a Python list into a NumPy array.

output:
[[1 2]
 [3 4]]

(2, 2)
'''

# 9. Calculate column-wise mean
print(a.mean(axis=0))
print(a.mean(axis=1))
print("\n-------\n")

'''
output:
[2. 3.]  # Column-wise mean
[1.5 3.5]  # Row-wise mean
'''

# 10. Conditional replacement using np.where()
result = np.where(a>2, 1, 0)
print(result)
'''
notes:
- np.where(condition, value_if_true, value_if_false)

- Checks whether each element in the array is greater than 2.
- If True, returns 1; otherwise, returns 0.

output:
[[0 0]
 [1 1]]
 '''
 
print("\n-------\n")
 # retype add_item, group_by and counted from memory. They’re due from Day 2.
import functools, defaultdict
 
def add_item(list):
    bag = []
    for ch in list:
        if ch not in bag:
            bag.append(ch)

def group_by(str):
    list = defaultdict()
    for ch in str:
        if ch not in list:
            list[k].append(v)

def counted(list):
    @functools wrap
    def wrap():
        wrap += 1
    return wrap
    
    