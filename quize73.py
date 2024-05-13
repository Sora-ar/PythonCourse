class InstanceCounter:
    num_instances = 0

    def __init__(self):
        InstanceCounter.num_instances += 1

    def __del__(self):
        InstanceCounter.num_instances -= 1


# Testing the class
print("Initial number of instances:", InstanceCounter.num_instances)

# Creating instances
obj1 = InstanceCounter()
obj2 = InstanceCounter()
obj3 = InstanceCounter()

print("Number of instances after creating objects:", InstanceCounter.num_instances)
