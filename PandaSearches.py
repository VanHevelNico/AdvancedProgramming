import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./data/database.csv')
print(df)


# Search between dates
def between(unit,start,end):
    if unit == "date":
        result = df[df["Launch Date"].between(start,end)]
    elif unit == "weight":
        result = df[df["Payload Mass (kg)"].between(start,end)]

    print(result)

def customer(customer_name):
    result = df[df['Customer Name']== customer_name]
    print(result)

def plot():
        plt.show(sns.countplot(x='Launch Year', data=df))


# function between dates
# between("date","2010-01-01", "2011-01-01")

# function between mass
#between("weight",7, 501)

# function on customer
# customer("NASA")

# make plot
plot()