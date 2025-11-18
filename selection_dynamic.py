import random
import time

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# ------------------------------------------------------------
# Deterministic Selection (Median of Medians)
# ------------------------------------------------------------

def median_of_medians(arr, k):
    if len(arr) <= 5:
        return sorted(arr)[k]

    groups = [arr[i:i + 5] for i in range(0, len(arr), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]

    pivot = median_of_medians(medians, len(medians) // 2)

    low = [x for x in arr if x < pivot]
    high = [x for x in arr if x > pivot]
    equal = [x for x in arr if x == pivot]

    if k < len(low):
        return median_of_medians(low, k)
    elif k < len(low) + len(equal):
        return pivot
    else:
        return median_of_medians(high, k - len(low) - len(equal))


# ------------------------------------------------------------
# Randomized Quickselect
# ------------------------------------------------------------

def quickselect(arr, k):
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)

    low = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]

    if k < len(low):
        return quickselect(low, k)
    elif k < len(low) + len(equal):
        return pivot
    else:
        return quickselect(high, k - len(low) - len(equal))


# ------------------------------------------------------------
# Benchmark Helper
# ------------------------------------------------------------

def benchmark(func, arr, k):
    start = time.time()
    result = func(arr.copy(), k)
    return result, time.time() - start


# ------------------------------------------------------------
# Multi-line number entry helper
# ------------------------------------------------------------

def get_numbers():
    while True:
        try:
            count = int(input("How many numbers do you want to enter? "))
            if count > 0:
                break
            print(f"{RED}Please enter a positive number.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input! Enter an integer.{RESET}")

    collected = []
    print(f"\nEnter {count} integers across multiple lines:")

    while len(collected) < count:
        remaining = count - len(collected)
        line = input(f"Enter up to {remaining} numbers: ").split()

        try:
            nums = list(map(int, line))
        except ValueError:
            print(f"{RED}Only integers allowed.{RESET}")
            continue

        if len(nums) + len(collected) > count:
            nums = nums[:count - len(collected)]

        collected.extend(nums)

    print(f"\n{GREEN}Collected numbers: {collected}{RESET}\n")
    return collected


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

print(f"\n{CYAN}========= ORDER STATISTICS SELECTION ========={RESET}\n")

arr = get_numbers()

# Set initial k
while True:
    try:
        k = int(input(f"Enter k (0 to {len(arr)-1}): "))
        if 0 <= k < len(arr):
            break
        print(f"{RED}k is out of range!{RESET}")
    except ValueError:
        print(f"{RED}Invalid input! Enter an integer.{RESET}")

try:
    while True:
        print(f"""
{CYAN}--------------- MAIN MENU ---------------{RESET}
1 → Run Algorithms (Deterministic/Randomized/Compare)
2 → Change k
3 → Enter new list of numbers
4 → Exit
""")

        choice = input("Enter choice (1/2/3/4): ").strip()

        # --------------------------------------------------------
        # Exit program
        # --------------------------------------------------------
        if choice == "4":
            print(f"{YELLOW}Program closed. Goodbye!{RESET}")
            break

        # --------------------------------------------------------
        # Change k
        # --------------------------------------------------------
        elif choice == "2":
            while True:
                try:
                    k = int(input(f"Enter new k (0 to {len(arr)-1}): "))
                    if 0 <= k < len(arr):
                        print(f"{GREEN}k updated successfully!{RESET}")
                        break
                    print(f"{RED}k is out of range!{RESET}")
                except ValueError:
                    print(f"{RED}Invalid input! Enter an integer.{RESET}")

        # --------------------------------------------------------
        # Enter new numbers
        # --------------------------------------------------------
        elif choice == "3":
            arr = get_numbers()

            while True:
                try:
                    k = int(input(f"Set new k (0 to {len(arr)-1}): "))
                    if 0 <= k < len(arr):
                        break
                    print(f"{RED}k is out of range!{RESET}")
                except ValueError:
                    print(f"{RED}Enter a valid integer.{RESET}")

        # --------------------------------------------------------
        # Algorithm submenu
        # --------------------------------------------------------
        elif choice == "1":
            while True:
                print(f"""
{CYAN}--------------- ALGORITHM MENU ---------------{RESET}
1 → Deterministic Selection (Median of Medians)
2 → Randomized Quickselect
3 → Compare Both
4 → Back to Main Menu
""")

                subchoice = input("Choose option: ").strip()

                if subchoice == "1":
                    result = median_of_medians(arr.copy(), k)
                    print(f"{GREEN}\nDeterministic Result: {result}{RESET}\n")

                elif subchoice == "2":
                    result = quickselect(arr.copy(), k)
                    print(f"{GREEN}\nRandomized Quickselect Result: {result}{RESET}\n")

                elif subchoice == "3":
                    res1, t1 = benchmark(median_of_medians, arr, k)
                    res2, t2 = benchmark(quickselect, arr, k)
                    print(f"""
{CYAN}------ Comparison ------{RESET}
{GREEN}Deterministic: {res1} (time: {t1:.6f}s){RESET}
{YELLOW}Quickselect:  {res2} (time: {t2:.6f}s){RESET}
""")

                elif subchoice == "4":
                    break
                else:
                    print(f"{RED}Invalid choice. Try again.{RESET}")

        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

except KeyboardInterrupt:
    print(f"\n{YELLOW}Program terminated by user. Goodbye!{RESET}\n")
