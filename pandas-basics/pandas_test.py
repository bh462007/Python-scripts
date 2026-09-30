import pandas as pd

# data = [
#     ["INV001", "ABC Ltd", 5000],
#     ["INV002", "XYZ Ltd", 3200],
#     ["INV003", "ABC Ltd", 7000],
# ]

df=pd.read_csv("invoices.csv")

print(df["vendor"])

print("\n",df[["invoice_id", "amount"]])

print("\n", df[df["amount"]>4000])

print("\n",df[df["vendor"] == "ABC Ltd"])

print("\n",df[(df["vendor"] == "ABC Ltd") & (df["amount"]>4000)] )