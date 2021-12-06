import mysql.connector
import pandas as pd
from faker import Faker
from collections import defaultdict
from random import randint
import random

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

fake = Faker()
fake_data = defaultdict(list)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Wohenni123!",
  database="driver"
)

mycursor = mydb.cursor()

for _ in range(1000):
    fake_data["ssn"].append(random_with_N_digits(9))
    fake_data["first_name"].append( fake.first_name() )
    fake_data["last_name"].append( fake.last_name() )
    fake_data["address"].append( fake.address() )
    fake_data["dob"].append( fake.date_of_birth() )
    fake_data["height"].append( random.randint(150,200) )
    if (random.randint(0,1) == 0):
        fake_data["eye"].append("black")
    else:
        fake_data["eye"].append("blue")
    if (random.randint(0,1) == 0):
        fake_data["sex"].append("m")
    else:
        fake_data["sex"].append("f")
    

sql = "INSERT INTO driver (SSN, First_Name, Last_Name, Address, Birthday, Height, Eye, Sex) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
df_fake_data = pd.DataFrame(fake_data)
i = 0
print(type(str(df_fake_data.loc[i].at["ssn"].item())))
for _ in range(1000):
    print(len(df_fake_data.loc[i].at["address"]))
    mycursor.execute(sql, (str(df_fake_data.loc[i].at["ssn"].item()), 
                        df_fake_data.loc[i].at["first_name"], df_fake_data.loc[i].at["last_name"] ,
                            df_fake_data.loc[i].at["address"],df_fake_data.loc[i].at["dob"], str(df_fake_data.loc[i].at["height"].item())
                            , df_fake_data.loc[i].at["eye"], df_fake_data.loc[i].at["sex"]))
    i = i + 1
mydb.commit()
print(df_fake_data)
print(type(df_fake_data))