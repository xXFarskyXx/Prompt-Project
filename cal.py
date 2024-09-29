import numpy as np

# Constants (these values are percentages in decimal form)
Ams_commission_percent = 0.0749
Normal_commission_percent = 0.0535
Service_commission_percent = 0.0535
Transaction_commission_percent = 0.0321
delivery_fee = 20  # Example delivery fee

# Function to convert percentage input to decimal form
def to_percentage(value):
    return value / 100

# Inputs
cogs_unit = float(input("Enter COGS per unit: "))
unit = int(input("Enter number of units: "))

# Input for net profit income target range
min_net_income_input = float(input("Enter minimum target net income as a percentage of COGS (e.g., 27.5 for 27.5%): "))
max_net_income_input = float(input("Enter maximum target net income as a percentage of COGS (e.g., 100 for 100%): "))
target_net_income_min = to_percentage(min_net_income_input) * cogs_unit * unit
target_net_income_max = to_percentage(max_net_income_input) * cogs_unit * unit

# Input for discount sign range and promotion range
discount_sign_min_input = float(input("Enter minimum discount sign percentage (e.g., 0 for 0%): "))
discount_sign_max_input = float(input("Enter maximum discount sign percentage (e.g., 20 for 20%): "))
discount_promotion_min_input = float(input("Enter minimum discount promotion percentage (e.g., 5 for 5%): "))
discount_promotion_max_input = float(input("Enter maximum discount promotion percentage (e.g., 50 for 50%): "))

# Default step values for discount sign and promotion
discount_sign_step = 0.005  # Default step of 0.5%
discount_promotion_step = 0.005  # Default step of 1%

# Create ranges for discount sign and promotion based on inputs
discount_sign_percent_range = np.arange(to_percentage(discount_sign_min_input), to_percentage(discount_sign_max_input) + discount_sign_step, discount_sign_step)
discount_promotion_percent_range = np.arange(to_percentage(discount_promotion_min_input), to_percentage(discount_promotion_max_input) + discount_promotion_step, discount_promotion_step)

# Function to calculate net income
def calculate_net_income(init_sales, discount_sign, discount_promotion, unit, cogs_unit):
    # Calculate gross profit first
    gross_profit = unit * (init_sales/unit - discount_sign - cogs_unit/unit - discount_promotion)
    
    # Tax difference
    tax_diff = unit * 0.07 * gross_profit
    
    # Selling expense
    selling_expense = ((Ams_commission_percent + Normal_commission_percent + Service_commission_percent) * gross_profit) + (Transaction_commission_percent * (gross_profit + delivery_fee * unit))
    
    # Net income
    net_income = gross_profit - tax_diff - selling_expense
    
    return net_income

# Array to store all valid solutions
valid_solutions = []

# Starting the sales price iteration with an initial guess, e.g., 1.2 times the COGS per unit
for init_sales in np.arange(cogs_unit * 1.2, cogs_unit * 4, 0.05):
    for discount_sign_percent in discount_sign_percent_range:
        for discount_promotion_percent in discount_promotion_percent_range:
            # Calculate the actual discount sign and promotion values based on percentages
            discount_sign = discount_sign_percent * init_sales
            gross_profit = unit * (init_sales/unit - discount_sign - cogs_unit/unit)  # Updated gross profit before applying discount promotion
            discount_promotion = discount_promotion_percent * gross_profit
            
            # Calculate net income
            net_income = calculate_net_income(init_sales, discount_sign, discount_promotion, unit, cogs_unit)
            
            if target_net_income_min <= net_income <= target_net_income_max:
                # Add the solution to the array as a dictionary
                valid_solutions.append({
                    'init_sales': init_sales,
                    'discount_sign_percent': discount_sign_percent * 100,  # Store as a percentage
                    'discount_promotion_percent': discount_promotion_percent * 100,  # Store as a percentage
                    'net_income': net_income
                })

# Display results
if valid_solutions:
    # Convert the list of dictionaries into arrays for easier analysis
    init_sales_values = [sol['init_sales'] for sol in valid_solutions]
    discount_sign_percent_values = [sol['discount_sign_percent'] for sol in valid_solutions]
    discount_promotion_percent_values = [sol['discount_promotion_percent'] for sol in valid_solutions]
    net_income_values = [sol['net_income'] for sol in valid_solutions]
    
    # Display the range of results
    print(f"Found {len(valid_solutions)} valid solutions.")
    print(f"Initial Sales Price range: {min(init_sales_values):.2f} to {max(init_sales_values):.2f}")
    print(f"Discount Sign percentage range: {min(discount_sign_percent_values):.2f}% to {max(discount_sign_percent_values):.2f}%")
    print(f"Discount Promotion percentage range: {min(discount_promotion_percent_values):.2f}% to {max(discount_promotion_percent_values):.2f}%")
    print(f"Net Income range: {min(net_income_values):.2f} to {max(net_income_values):.2f}")
else:
    print("No solution found that matches the target net income range.")
