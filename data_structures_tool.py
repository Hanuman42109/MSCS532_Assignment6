"""
data_structures_tool.py
Pro interactive console for basic data structures:
- Array (simple wrapper over Python list with insert/delete/access)
- Stack (LIFO)
- Queue (FIFO)
- Singly Linked List

Run: python data_structures_tool.py
"""

import sys

# -------------------------
# ANSI Colors
# -------------------------
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# -------------------------
# Helper Input Utilities
# -------------------------
def input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            s = input(prompt).strip()
            val = int(s)
            if min_val is not None and val < min_val:
                print(f"{RED}Value must be >= {min_val}.{RESET}")
                continue
            if max_val is not None and val > max_val:
                print(f"{RED}Value must be <= {max_val}.{RESET}")
                continue
            return val
        except ValueError:
            print(f"{RED}Please enter a valid integer.{RESET}")

def input_ints_multiline(count):
    """Collect exactly `count` integers; user can enter across multiple lines."""
    collected = []
    print(f"\nEnter {count} integers across one or more lines:")
    while len(collected) < count:
        remaining = count - len(collected)
        line = input(f"Enter up to {remaining} numbers: ").strip()
        if not line:
            print(f"{YELLOW}No input entered — try again.{RESET}")
            continue
        parts = line.split()
        try:
            nums = list(map(int, parts))
        except ValueError:
            print(f"{RED}Only integers allowed. Try that line again.{RESET}")
            continue
        if len(nums) + len(collected) > count:
            nums = nums[: count - len(collected)]
        collected.extend(nums)
    return collected

def press_enter_to_continue():
    input(f"\n{CYAN}Press Enter to continue...{RESET}")

# -------------------------
# Data Structure Implementations
# -------------------------
# Array (simple wrapper)
class ArrayDS:
    def __init__(self):
        self.data = []

    def init_with(self, lst):
        self.data = list(lst)

    def insert(self, index, value):
        if index < 0 or index > len(self.data):
            raise IndexError("Index out of bounds")
        self.data.insert(index, value)

    def delete(self, index):
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of bounds")
        return self.data.pop(index)

    def access(self, index):
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of bounds")
        return self.data[index]

    def display(self):
        return list(self.data)

# Stack
class StackDS:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if not self.stack:
            raise IndexError("Stack underflow")
        return self.stack.pop()

    def peek(self):
        if not self.stack:
            raise IndexError("Stack empty")
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def display(self):
        return list(self.stack)

# Queue
class QueueDS:
    def __init__(self):
        self.queue = []

    def enqueue(self, val):
        self.queue.append(val)

    def dequeue(self):
        if not self.queue:
            raise IndexError("Queue underflow")
        return self.queue.pop(0)

    def front(self):
        if not self.queue:
            raise IndexError("Queue empty")
        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        return list(self.queue)

# Singly Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListDS:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_at_end(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete_value(self, key):
        cur = self.head
        prev = None
        while cur:
            if cur.data == key:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

    def search(self, key):
        cur = self.head
        while cur:
            if cur.data == key:
                return True
            cur = cur.next
        return False

    def display(self):
        elems = []
        cur = self.head
        while cur:
            elems.append(cur.data)
            cur = cur.next
        return elems

# -------------------------
# Menus and Interaction
# -------------------------
def array_menu(array_ds):
    while True:
        print(f"""
{MAGENTA}--- ARRAY MENU ---{RESET}
1 → Initialize / Replace array
2 → Insert at index
3 → Delete at index
4 → Access by index
5 → Display array
6 → Back
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            n = input_int("How many elements? ", min_val=0)
            if n == 0:
                array_ds.init_with([])
                print(f"{GREEN}Array initialized empty.{RESET}")
            else:
                nums = input_ints_multiline(n)
                array_ds.init_with(nums)
                print(f"{GREEN}Array initialized: {array_ds.display()}{RESET}")
            press_enter_to_continue()

        elif choice == "2":
            try:
                idx = input_int(f"Insert index (0 to {len(array_ds.data)}): ", min_val=0, max_val=len(array_ds.data))
                val = input_int("Value to insert: ")
                array_ds.insert(idx, val)
                print(f"{GREEN}Inserted. Current array: {array_ds.display()}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()

        elif choice == "3":
            try:
                if len(array_ds.data) == 0:
                    print(f"{YELLOW}Array empty.{RESET}")
                else:
                    idx = input_int(f"Delete index (0 to {len(array_ds.data)-1}): ", min_val=0, max_val=len(array_ds.data)-1)
                    removed = array_ds.delete(idx)
                    print(f"{GREEN}Deleted {removed}. Current array: {array_ds.display()}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()

        elif choice == "4":
            try:
                if len(array_ds.data) == 0:
                    print(f"{YELLOW}Array empty.{RESET}")
                else:
                    idx = input_int(f"Access index (0 to {len(array_ds.data)-1}): ", min_val=0, max_val=len(array_ds.data)-1)
                    val = array_ds.access(idx)
                    print(f"{GREEN}Element at index {idx} is {val}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()

        elif choice == "5":
            print(f"{CYAN}Array: {array_ds.display()}{RESET}")
            press_enter_to_continue()

        elif choice == "6":
            break
        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

def stack_menu(stack_ds):
    while True:
        print(f"""
{MAGENTA}--- STACK MENU ---{RESET}
1 → Push
2 → Pop
3 → Peek
4 → Display
5 → Back
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            val = input_int("Value to push: ")
            stack_ds.push(val)
            print(f"{GREEN}Pushed. Stack: {stack_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "2":
            try:
                popped = stack_ds.pop()
                print(f"{GREEN}Popped: {popped}. Stack: {stack_ds.display()}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()
        elif choice == "3":
            try:
                top = stack_ds.peek()
                print(f"{GREEN}Top element: {top}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()
        elif choice == "4":
            print(f"{CYAN}Stack (bottom -> top): {stack_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "5":
            break
        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

def queue_menu(queue_ds):
    while True:
        print(f"""
{MAGENTA}--- QUEUE MENU ---{RESET}
1 → Enqueue
2 → Dequeue
3 → Front
4 → Display
5 → Back
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            val = input_int("Value to enqueue: ")
            queue_ds.enqueue(val)
            print(f"{GREEN}Enqueued. Queue: {queue_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "2":
            try:
                d = queue_ds.dequeue()
                print(f"{GREEN}Dequeued: {d}. Queue: {queue_ds.display()}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()
        elif choice == "3":
            try:
                f = queue_ds.front()
                print(f"{GREEN}Front element: {f}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            press_enter_to_continue()
        elif choice == "4":
            print(f"{CYAN}Queue (front -> rear): {queue_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "5":
            break
        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

def linked_list_menu(llist_ds):
    while True:
        print(f"""
{MAGENTA}--- LINKED LIST MENU ---{RESET}
1 → Insert at head
2 → Insert at end
3 → Delete by value
4 → Search
5 → Display
6 → Back
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            val = input_int("Value to insert at head: ")
            llist_ds.insert_at_head(val)
            print(f"{GREEN}Inserted at head. List: {llist_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "2":
            val = input_int("Value to insert at end: ")
            llist_ds.insert_at_end(val)
            print(f"{GREEN}Inserted at end. List: {llist_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "3":
            val = input_int("Value to delete (first occurrence): ")
            ok = llist_ds.delete_value(val)
            if ok:
                print(f"{GREEN}Deleted {val}. List: {llist_ds.display()}{RESET}")
            else:
                print(f"{YELLOW}Value {val} not found.{RESET}")
            press_enter_to_continue()
        elif choice == "4":
            val = input_int("Value to search: ")
            found = llist_ds.search(val)
            print(f"{GREEN if found else YELLOW}{'Found' if found else 'Not found'}{RESET}")
            press_enter_to_continue()
        elif choice == "5":
            print(f"{CYAN}Linked List (head -> ...): {llist_ds.display()}{RESET}")
            press_enter_to_continue()
        elif choice == "6":
            break
        else:
            print(f"{RED}Invalid option. Try again.{RESET}")

# -------------------------
# Main program loop
# -------------------------
def main():
    print(f"\n{CYAN}====== DATA STRUCTURES TOOL ======{RESET}\n")
    array_ds = ArrayDS()
    stack_ds = StackDS()
    queue_ds = QueueDS()
    llist_ds = LinkedListDS()

    try:
        while True:
            print(f"""
{CYAN}--- MAIN MENU ---{RESET}
1 → Work with Array
2 → Work with Stack
3 → Work with Queue
4 → Work with Linked List
5 → Exit
""")
            choice = input("Choose option: ").strip()
            if choice == "1":
                array_menu(array_ds)
            elif choice == "2":
                stack_menu(stack_ds)
            elif choice == "3":
                queue_menu(queue_ds)
            elif choice == "4":
                linked_list_menu(llist_ds)
            elif choice == "5":
                print(f"{YELLOW}Exiting tool. Goodbye!{RESET}")
                break
            else:
                print(f"{RED}Invalid option. Try again.{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Terminated by user (Ctrl+C). Goodbye!{RESET}\n")
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()