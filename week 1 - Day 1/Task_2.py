# ==============================================================================
#  Sales Report Processing Loop
# ==============================================================================
sales = [12000, 0, 8500, 15000, -200, 9800]
total = 0
target_value = 30000

for x in sales:
    # Skip zero or negative values
    if x <= 0:
        print(f"Skipped invalid value {x}")
        continue
    
    # Update running total and print progress
    total += x
    print(f"Added {x} total {total}")
    
    # Break loop as soon as total goes above target
    if total > target_value:
        break

# Final conditional message check after the loop
if total > target_value:
    print(f"Target reached. Stopped at {total}")
else:
    print("Target not reached")