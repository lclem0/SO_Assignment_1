import random
import numpy as np
import matplotlib.pyplot as plt


# Simulation parameters
setup_cost = 32
incremental_cost = 3
holding_cost = 1
shortage_cost = 5

# Lists for plotting
time_points = []
inventory_levels = []
positive_inventory = []
backlog_levels = []
holding_costs = []
shortage_costs = []


def exponential_demand_time(mean):
    return random.expovariate(1 / mean)

def demand_size():
    return np.random.choice([1, 2, 3, 4], p=[1/6, 1/3, 1/3, 1/6])


def place_order(inventory_level, orders_in_transit, scheduled_order_amount, s, S, total_cost, sim_time, next_order_month, express_orders, normal_cost_list, express_cost_list):
    effective_inventory = inventory_level + scheduled_order_amount
    if sim_time >= next_order_month:
        if effective_inventory < 0:
            # Express order conditions
            needed = max(0, S + effective_inventory)
            if needed > 0:
                total_cost += 48 + 4 * needed
                express_cost = 48 + 4 * needed
                express_cost_list.append(express_cost)
                arrival_time = sim_time + random.uniform(0.25, 0.5)  # Faster delivery time for express orders
                orders_in_transit.append((arrival_time, needed))
                scheduled_order_amount += needed
                express_orders += 1
                # print(f"Effective inventory is at {effective_inventory}, placing express order of {needed} items with a cost of {express_cost} at time {sim_time:.2f}, arriving at {arrival_time:.2f}")
                express_cost = 0

        elif effective_inventory < s:
            # Normal order conditions
            needed = max(0, S - effective_inventory)
            if needed > 0:
                total_cost += setup_cost + incremental_cost * needed
                normal_cost = setup_cost + incremental_cost * needed
                normal_cost_list.append(normal_cost)
                arrival_time = sim_time + random.uniform(0.5, 1)  # Normal delivery time
                orders_in_transit.append((arrival_time, needed))
                scheduled_order_amount += needed
                # print(f"Effective inventory is at {effective_inventory}, placing normal order of {needed} items with a cost of {normal_cost} at time {sim_time:.2f}, arriving at {arrival_time:.2f}")
                normal_cost = 0
        next_order_month += 1  # Ensure next order not before next month

    return orders_in_transit, scheduled_order_amount, total_cost, next_order_month, express_orders, normal_cost_list, express_cost_list

def process_order_arrival(inventory_level, scheduled_order_amount, orders_in_transit, sim_time):
    orders_in_transit.sort()
    while orders_in_transit and orders_in_transit[0][0] <= sim_time:
        order = orders_in_transit.pop(0)
        inventory_level += order[1]
        scheduled_order_amount -= order[1]
        # print(f"Order of {order[1]} items arrived at time {sim_time:.2f}")
    return inventory_level, scheduled_order_amount, orders_in_transit

def process_demand(inventory_level, backorders):
    d = demand_size()
    if inventory_level >= d:
        inventory_level -= d
    else:
        additional_needed = d - inventory_level
        inventory_level = -additional_needed
        backorders += d
    # print(f"Demand of {d} at time {sim_time:.2f}, inventory {inventory_level}, backorders {backorders}")
    return inventory_level, backorders

def simulate(s, S):
    sim_time = 0
    next_order_month = 0
    orders_in_transit = []
    backorders = 0
    scheduled_order_amount = 0
    total_cost = 0
    inventory_level = 60  # Starting inventory level
    express_orders = 0
    backlog_time_points = 0  # To track the number of time points with a backlog
    monthly_backorders = []  # List to track backorders at the end of each month
    total_holding_cost = 0
    total_shortage_cost = 0
    inventory_level_items = []
    monthly_costs = []
    normal_cost_list = []
    express_cost_list = []

    time_points.clear()
    inventory_levels.clear()
    positive_inventory.clear()
    backlog_levels.clear()

    months = 120  # Duration of simulation in months

    demand_interval = sim_time + exponential_demand_time(0.1)

    while sim_time < months:
        time_points.append(sim_time)
        if inventory_level < 0:
            backlog_time_points += 1

        if orders_in_transit and orders_in_transit[0][0] <= sim_time:
            inventory_level, scheduled_order_amount, orders_in_transit = process_order_arrival(
                inventory_level, scheduled_order_amount, orders_in_transit, sim_time)

        if sim_time >= demand_interval:
            inventory_level, backorders = process_demand(inventory_level, backorders)
            demand_interval += exponential_demand_time(0.1)

        orders_in_transit, scheduled_order_amount, total_cost, next_order_month, express_orders, normal_cost_list, express_cost_list  = place_order(
            inventory_level, orders_in_transit, scheduled_order_amount, s, S, total_cost, sim_time, next_order_month, express_orders, normal_cost_list, express_cost_list)

        inventory_levels.append(inventory_level)
        positive_inventory.append(max(0, inventory_level))
        backlog_levels.append(max(0, -inventory_level))

        # Check if it's the end of a month
        if int(sim_time * 10) % 10 == 0:
            # print('End of Month:', int(sim_time) + 1)
            # print('It is the end of the month. The inventory level is:', inventory_level)
            # print('Total cost at end of the month:', total_cost)

            current_holding_cost = max(0, inventory_level) * holding_cost
            holding_costs.append(current_holding_cost)
            total_holding_cost += current_holding_cost
            # print('Holding cost applied for', max(0, inventory_level), 'items:', current_holding_cost)

            monthly_backorders.append(backorders)
            current_shortage_cost = backorders * shortage_cost
            shortage_costs.append(current_shortage_cost)
            total_shortage_cost += current_shortage_cost
            # print('Backlog at the end of the month:', backorders)
            # print('Shortage cost applied for', backorders, 'backlogged items:', current_shortage_cost)
            
            inventory_level_items.append(inventory_level)
            total_cost += current_holding_cost + current_shortage_cost
            monthly_cost = current_holding_cost + current_shortage_cost
            monthly_costs.append(monthly_cost)
            # Reset the backlog count for the new month
            backorders = 0

        sim_time += 1/10  # Increment time by approximately a 1/10 of month

    average_cost_per_month = total_cost / months
    proportion_of_time_with_backlog = (backlog_time_points/len(time_points))*100
    monthly_costs.pop(0)

    return proportion_of_time_with_backlog, express_orders, average_cost_per_month, monthly_backorders, holding_costs, shortage_costs, total_cost, inventory_level_items, monthly_costs, normal_cost_list, express_cost_list


def run_simulations(N, s, S):
    proportion_of_time_with_backlogs = []
    express_orders_n = []
    average_cost_per_month_list = []
    for _ in range(N):
        proportion_of_time_with_backlog, express_orders, average_cost_per_month, monthly_backorders, holding_costs, shortage_costs, total_cost, inventory_level_items, monthly_costs, normal_cost_list, express_cost_list = simulate(s, S)
        proportion_of_time_with_backlogs.append(proportion_of_time_with_backlog)
        express_orders_n.append(express_orders)
        average_cost_per_month_list.append(average_cost_per_month)
    return total_cost, proportion_of_time_with_backlog, express_orders_n, average_cost_per_month_list, monthly_backorders, holding_costs, shortage_costs, inventory_level_items, monthly_costs, normal_cost_list, express_cost_list


def average_express_orders(express_orders):
    return sum(express_orders)/len(express_orders)

def average_cost_per_month(average_cost_per_month_list):
    return sum(average_cost_per_month_list)/len(average_cost_per_month_list)

def obtain_results(proportion_of_time_with_backlog, express_orders, average_cost_per_month_list, N, s, S):
    avg_express_orders = average_express_orders(express_orders)
    avg_cost_per_months = average_cost_per_month(average_cost_per_month_list)
    print(f"Simulation for {N} runs with (s, S) = ({s}, {S})")
    print(f"Proportion of Time with Backlog: {proportion_of_time_with_backlog:.2f}%")
    print(f"Number of Express Orders: {avg_express_orders:.2f}")
    print(f"Average Total Cost per Month: {avg_cost_per_months:.2f}")

num_simulations = 10
total_cost_20_40, proportion_of_time_with_backlog_20_40, express_orders_20_40, average_cost_per_month_list_20_40, monthly_backorders_20_40, holding_cost_20_40, shortage_costs_20_40, inventory_level_items_20_40, monthly_costs_20_40, normal_cost_list_20_40, express_cost_list_20_40 = run_simulations(num_simulations, 20, 40)
obtain_results(proportion_of_time_with_backlog_20_40, express_orders_20_40, average_cost_per_month_list_20_40, num_simulations, 20, 40)

total_cost_20_60, proportion_of_time_with_backlog_20_60, express_orders_20_60, average_cost_per_month_list_20_60, monthly_backorders_20_60, holding_cost_20_60, shortage_costs_20_60, inventory_level_items_20_60, monthly_costs_20_60, normal_cost_list_20_60, express_cost_list_20_60 = run_simulations(num_simulations, 20, 60)
obtain_results(proportion_of_time_with_backlog_20_60, express_orders_20_60, average_cost_per_month_list_20_60, num_simulations, 20, 60)

total_cost_20_80, proportion_of_time_with_backlog_20_80, express_orders_20_80, average_cost_per_month_list_20_80, monthly_backorders_20_80, holding_cost_20_80, shortage_costs_20_80, inventory_level_items_20_80, monthly_costs_20_80, normal_cost_list_20_80, express_cost_list_20_80 = run_simulations(num_simulations, 20, 80)
obtain_results(proportion_of_time_with_backlog_20_80, express_orders_20_80, average_cost_per_month_list_20_80, num_simulations, 20, 80)

total_cost_20_100, proportion_of_time_with_backlog_20_100, express_orders_20_100, average_cost_per_month_list_20_100, monthly_backorders_20_100, holding_cost_20_100, shortage_costs_20_100, inventory_level_items_20_100, monthly_costs_20_100, normal_cost_list_20_100, express_cost_list_20_100 = run_simulations(num_simulations, 20, 100)
obtain_results(proportion_of_time_with_backlog_20_100, express_orders_20_100, average_cost_per_month_list_20_100, num_simulations, 20, 100)

total_cost_40_60, proportion_of_time_with_backlog_40_60, express_orders_40_60, average_cost_per_month_list_40_60, monthly_backorders_40_60, holding_cost_40_60, shortage_costs_40_60, inventory_level_items_40_60, monthly_costs_40_60, normal_cost_list_40_60, express_cost_list_40_60 = run_simulations(num_simulations, 40, 60)
obtain_results(proportion_of_time_with_backlog_40_60, express_orders_40_60, average_cost_per_month_list_40_60, num_simulations, 40, 60)

total_cost_40_80, proportion_of_time_with_backlog_40_80, express_orders_40_80, average_cost_per_month_list_40_80, monthly_backorders_40_80, holding_cost_40_80, shortage_costs_40_80, inventory_level_items_40_80, monthly_costs_40_80, normal_cost_list_40_80, express_cost_list_40_80 = run_simulations(num_simulations, 40, 80)
obtain_results(proportion_of_time_with_backlog_40_80, express_orders_40_80, average_cost_per_month_list_40_80, num_simulations, 40, 80)

total_cost_40_100, proportion_of_time_with_backlog_40_100, express_orders_40_100, average_cost_per_month_list_40_100, monthly_backorders_40_100, holding_cost_40_100, shortage_costs_40_100, inventory_level_items_40_100, monthly_costs_40_100, normal_cost_list_40_100, express_cost_list_40_100 = run_simulations(num_simulations, 40, 100)
obtain_results(proportion_of_time_with_backlog_40_100, express_orders_40_100, average_cost_per_month_list_40_100, num_simulations, 40, 100)

total_cost_60_80, proportion_of_time_with_backlog_60_80, express_orders_60_80, average_cost_per_month_list_60_80, monthly_backorders_60_80, holding_cost_60_80, shortage_costs_60_80, inventory_level_items_60_80, monthly_costs_60_80, normal_cost_list_60_80, express_cost_list_60_80 = run_simulations(num_simulations, 60, 80)
obtain_results(proportion_of_time_with_backlog_60_80, express_orders_60_80, average_cost_per_month_list_60_80, num_simulations, 60, 80)

total_cost_60_100, proportion_of_time_with_backlog_60_100, express_orders_60_100, average_cost_per_month_list_60_100, monthly_backorders_60_100, holding_cost_60_100, shortage_costs_60_100, inventory_level_items_60_100, monthly_costs_60_100, normal_cost_list_60_100, express_cost_list_60_100 = run_simulations(num_simulations, 60, 100)
obtain_results(proportion_of_time_with_backlog_60_100, express_orders_60_100, average_cost_per_month_list_60_100, num_simulations, 60, 100)

# Plotting for visualization
def plot_values(value_lists, labels, title, x_label, y_label):
    plt.figure(figsize=(10, 5))
    for i, values in enumerate(value_lists):
        plt.plot(values, marker='o', label=labels[i])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(title='(s, S) Values')
    plt.grid(True)
    plt.show()

def plot_bar_values(value_lists, labels, title, x_label, y_label):
    # Create a bar plot
    plt.figure(figsize=(12, 6))
    # Setting the positions and width for the bars
    positions = range(len(value_lists))
    plt.bar(positions, value_lists, align='center', alpha=0.7, color='b')
    
    # Adding the aesthetics
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Adding labels to each bar
    plt.xticks(positions, labels, rotation=45)  # Rotate labels to avoid overlap
    plt.legend(title='(s, S) Values')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    
    # Show the plot
    plt.show()



labels = ['20/40', '20/60', '20/80', '20/100', '40/60', '40/80', '40/100', '60/80', '60/100']

# Plot express orders:
express_orders_values = [express_orders_20_40, express_orders_20_60, express_orders_20_80, express_orders_20_100,
                         express_orders_40_60, express_orders_40_80, express_orders_40_100,
                         express_orders_60_80, express_orders_60_100]
# plot_values(express_orders_values, labels, 'Express Orders for Different (s, S) Combinations', 'Run Number', 'Express Orders')


#Plot average cost per month
average_cost_per_month_values = [average_cost_per_month_list_20_40, average_cost_per_month_list_20_60, average_cost_per_month_list_20_80, average_cost_per_month_list_20_100,
                        average_cost_per_month_list_40_60, average_cost_per_month_list_40_80, average_cost_per_month_list_40_100,
                        average_cost_per_month_list_60_80, average_cost_per_month_list_60_100]
# plot_values(average_cost_per_month_values, labels, 'Average Cost per Month for Different (s, S) Combinations, with express orders', 'Run Number', 'Average Cost per Month')

#plot proportion of time with backlog
proportion_of_time_with_backlog_values = [proportion_of_time_with_backlog_20_40, proportion_of_time_with_backlog_20_60, proportion_of_time_with_backlog_20_80, proportion_of_time_with_backlog_20_100,
                        proportion_of_time_with_backlog_40_60, proportion_of_time_with_backlog_40_80, proportion_of_time_with_backlog_40_100,
                        proportion_of_time_with_backlog_60_80, proportion_of_time_with_backlog_60_100]
for i, value in enumerate(proportion_of_time_with_backlog_values):
    proportion_of_time_with_backlog_values[i] = value

# plot_bar_values(
#     proportion_of_time_with_backlog_values, 
#     labels, 
#     'Proportion of Time with Backlog for Different (s, S) Combinations, with express orders',
#     'Inventory Policy (s, S)', 
#     'Proportion of Time with Backlog (%)'
# )
