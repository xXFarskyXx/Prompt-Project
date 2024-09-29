import numpy as np
import pandas as pd

all_discount = 5 #Change this value when you make discount
cogs = 0 #Pull cogs from cogs_modify.xlsx
gross_revenue = 0

def compute_profit_margin():
    net_receive = gross_revenue - all_discount
    tax = 0.07 * (gross_revenue - cogs)
    market_expense = (gross_revenue * (0.0749 + 0.0535 + 0.0535)) + (0.0321 * net_receive)
    gross_profit = net_receive - cogs - tax
    net_income = gross_profit - market_expense
    profit_margin = (net_income/cogs) * 100

    return profit_margin