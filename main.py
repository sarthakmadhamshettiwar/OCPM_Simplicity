# Import the required module or class
from metrics_evaluation import ocel_metrics_calculation

# Define the filepath to the OCEL file
filepath = 'p2p-normal.jsonocel'

# Create an instance of the metrics calculation class
ocel_metrics = ocel_metrics_calculation(filepath)

# Calculate and print the simplicity metric
print('Simplicity of OCEL model is:', ocel_metrics.calculate_ocel_simplicity())
# print('Precision of OCEL model is:', ocel_metrics.calculate_ocel_fitness())
# print('Fitness of OCEL model is:', ocel_metrics.calculate_ocel_precision())