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

df["vendor"] = df["vendor"].str.strip()
print("\n",df)

df["vendor"] = df["vendor"].str.lower()
print("\n", df)

df = pd.read_csv("invoices.csv")

df["date"]=pd.to_datetime(df["date"], dayfirst=True)
print("\n", df)
print("\n", df.dtypes)