import random
import pandas as pd

df=pd.read_csv("results/event.csv", delimiter=",")

print(list(df))
extra=df["negemo"]+df["anx"]-df["you"]

print("extra:::",extra)


agree=df["you"] + df["social"] +df["friend"] +df["sexual"]
print("agree:::",agree)

consc=df["article"] + df["prep"]- df["posemo"] - df["social"] -df["family"] -df["time"] - df["focuspast"] - df["focuspresent"] -  df["motion"] -  df["leisure"] -  df["home"] - df["death"]
print("consc:::",consc)


neuro=df["we"] + df["posemo"] - df["negemo"] +df["family"] +df["space"] - df["anger"] +  df["motion"] +  df["leisure"] +  df["home"] - df["swear"]
print("neuro:::",neuro)


open_=df["achieve"] - df["negate"] - df["negemo"] - df["anger"] 
print("open_:::",open_)


print("power::",df["power"])
print("cogproc::",df["cogproc"])
print("percept::",df["percept"])
