def water_jug():
    capacity_A = 4
    capacity_B = 3

    jug_A, jug_B = 0, 0
    visited = set()
    steps = []

    while True:
        visited.add((jug_A, jug_B))
        steps.append((jug_A, jug_B))

        if jug_A == 2:
            print("Goal reached!")
            break

        if jug_A == 0:
            jug_A = capacity_A

        elif jug_B < capacity_B:
            transfer = min(jug_A, capacity_B - jug_B)
            jug_A -= transfer
            jug_B += transfer

        elif jug_B == capacity_B:
            jug_B = 0

        if (jug_A, jug_B) in visited:
            print("No solution found.")
            break

    for i, step in enumerate(steps):
        print(f"Step {i}: Jug A = {step[0]}, Jug B = {step[1]}")

water_jug()
