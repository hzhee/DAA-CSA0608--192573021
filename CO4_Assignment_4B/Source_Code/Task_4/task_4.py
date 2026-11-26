#!/usr/bin/env python3
"""Task 4: two-line assembly scheduling with route reconstruction."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class AssemblyInput:
    line1: tuple[int, ...]
    line2: tuple[int, ...]
    transfer_1_to_2: tuple[int, ...]
    transfer_2_to_1: tuple[int, ...]
    entry: tuple[int, int]
    exit: tuple[int, int]

    @property
    def stations(self):
        return len(self.line1)


def solve(data: AssemblyInput):
    n = data.stations
    if n == 0 or len(data.line2) != n:
        raise ValueError("both processing lines must have the same positive station count")
    if len(data.transfer_1_to_2) != n - 1 or len(data.transfer_2_to_1) != n - 1:
        raise ValueError("each transfer array must contain one value between adjacent stations")
    if len(data.entry) != 2 or len(data.exit) != 2:
        raise ValueError("entry and exit times must have two line values")
    all_times = (*data.line1, *data.line2, *data.transfer_1_to_2, *data.transfer_2_to_1, *data.entry, *data.exit)
    if any(time < 0 for time in all_times):
        raise ValueError("processing, transfer, entry, and exit times must be nonnegative")

    cost = [[0] * n for _ in range(2)]
    predecessor = [[None] * n for _ in range(2)]
    cost[0][0] = data.entry[0] + data.line1[0]
    cost[1][0] = data.entry[1] + data.line2[0]
    trace = []

    for station in range(1, n):
        stay_l1 = cost[0][station - 1] + data.line1[station]
        transfer_l2_to_l1 = cost[1][station - 1] + data.transfer_2_to_1[station - 1] + data.line1[station]
        stay_l2 = cost[1][station - 1] + data.line2[station]
        transfer_l1_to_l2 = cost[0][station - 1] + data.transfer_1_to_2[station - 1] + data.line2[station]
        if stay_l1 <= transfer_l2_to_l1:
            cost[0][station] = stay_l1
            predecessor[0][station] = 0
            selected_l1 = "stay on Line 1"
        else:
            cost[0][station] = transfer_l2_to_l1
            predecessor[0][station] = 1
            selected_l1 = "transfer from Line 2"
        if stay_l2 <= transfer_l1_to_l2:
            cost[1][station] = stay_l2
            predecessor[1][station] = 1
            selected_l2 = "stay on Line 2"
        else:
            cost[1][station] = transfer_l1_to_l2
            predecessor[1][station] = 0
            selected_l2 = "transfer from Line 1"
        trace.append((station + 1, stay_l1, transfer_l2_to_l1, selected_l1,
                      stay_l2, transfer_l1_to_l2, selected_l2,
                      cost[0][station], cost[1][station]))

    final_l1 = cost[0][-1] + data.exit[0]
    final_l2 = cost[1][-1] + data.exit[1]
    final_line = 0 if final_l1 <= final_l2 else 1
    total = min(final_l1, final_l2)
    route = [final_line]
    for station in range(n - 1, 0, -1):
        route.append(predecessor[route[-1]][station])
    route.reverse()
    transfers = [(i + 1, route[i - 1] + 1, route[i] + 1)
                 for i in range(1, n) if route[i] != route[i - 1]]
    return total, route, transfers, trace, cost, (final_l1, final_l2)


def show(label, data):
    total, route, transfers, trace, cost, final = solve(data)
    print(f"\n{label}")
    print("Entry costs at Station 1:", cost[0][0], "on Line 1;", cost[1][0], "on Line 2")
    print("Station | L1 stay | L1 transfer | choose L1 | L2 stay | L2 transfer | choose L2 | best L1 | best L2")
    for row in trace:
        print(" | ".join(str(value) for value in row))
    route_names = [f"Line {line + 1} - Station {i + 1}" for i, line in enumerate(route)]
    print("Route:", "Entry -> " + " -> ".join(route_names) + " -> Exit Line " + str(route[-1] + 1))
    print("Selected line at each station:", [line + 1 for line in route])
    print("Transfer points (destination station, from, to):", transfers or "none")
    print("Exit comparison:", {"Line 1": final[0], "Line 2": final[1]})
    print("Minimum production time:", total)
    return total, route, transfers


def main():
    base = AssemblyInput(
        line1=(7, 9, 3, 4, 8, 4),
        line2=(8, 5, 6, 4, 5, 7),
        transfer_1_to_2=(2, 3, 1, 3, 4),
        transfer_2_to_1=(2, 1, 2, 2, 1),
        entry=(2, 4),
        exit=(3, 2),
    )
    print("TASK 4 - SMART MANUFACTURING ASSEMBLY LINE SCHEDULING")
    base_result = show("BASELINE INPUT", base)

    print("\nTRANSFER-TIME PREDICTION BEFORE EXECUTION")
    print("Increase Line 1->Line 2 transfer before Station 4 from 1 to 20. Prediction: the transfer into Line 2 at Station 4 will no longer be selected; minimum time will not decrease.")
    transfer_values = list(base.transfer_1_to_2)
    transfer_values[2] = 20
    transfer_case = replace(base, transfer_1_to_2=tuple(transfer_values))
    transfer_result = show("TRANSFER-TIME CHALLENGE", transfer_case)
    print("Prediction check: route changed =", transfer_result[1] != base_result[1], "; time change =", transfer_result[0] - base_result[0])

    print("\nMACHINE-SLOWDOWN PREDICTION BEFORE EXECUTION")
    print("Increase Line 1 Station 3 processing time from 3 to 30. Prediction: production will prefer Line 2 at Station 3; minimum time will rise because a processing time only increased.")
    slow_line = list(base.line1)
    slow_line[2] = 30
    slow_case = replace(base, line1=tuple(slow_line))
    slow_result = show("PRODUCTION DISRUPTION", slow_case)
    print("Prediction check: route changed =", slow_result[1] != base_result[1], "; time change =", slow_result[0] - base_result[0])
    if slow_result[1][2] == 1:
        print("The route switches to Line 2 at Station 3 because its station time is now lower than staying on Line 1 plus any required transfer.")

    print("\nTHREE-LINE ENGINEERING EXTENSION (not implemented)")
    print("Use DP[line,station] for each of three lines. For every station, compare staying on line l with transfers from each of the other two lines, adding the appropriate transfer and processing time. Store predecessor line for every state to reconstruct the route. Time becomes O(L^2*n) and state storage O(L*n) for L lines; entry/exit costs and transfer data also become per-line/per-pair.")

    one_station = AssemblyInput((5,), (7,), (), (), (2, 1), (3, 4))
    assert solve(one_station)[0] == 10
    assert base_result[0] == 38
    assert transfer_result[0] >= base_result[0] and slow_result[0] >= base_result[0]
    assert len(base_result[1]) == base.stations and base_result[1][0] in (0, 1)
    try:
        solve(replace(base, transfer_1_to_2=(-1, 3, 1, 3, 4)))
    except ValueError:
        invalid_rejected = True
    else:
        invalid_rejected = False
    assert invalid_rejected
    print("Tests passed: baseline route, transfer change, station slowdown, one-station boundary, invalid negative time.")


if __name__ == "__main__":
    main()
