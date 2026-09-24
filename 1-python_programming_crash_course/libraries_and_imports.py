import os
from dotenv import load_dotenv # 1.0.0
import time # 1.0.1
import random

load_dotenv()

name = os.getenv("NAME")
grade = os.getenv("GRADE")

os.environ["PI"] = "3.14"

pi_num = os.getenv("PI")

print(name, grade, pi_num)