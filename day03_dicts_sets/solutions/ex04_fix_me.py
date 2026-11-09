"""Day 3 - Exercise 4: FIX ME (reference solution) - an inventory module.
An inventory is a dict {item_name: quantity}. Fixes marked # FIX."""


def add_item(inv, name, qty):
    """Add qty units of name (in place)."""
    inv[name] = inv.get(name, 0) + qty  # FIX: was inv[name] = qty


def remove_item(inv, name, qty):
    """Remove qty units (in place). Raise KeyError if the item is not present and
    ValueError if there aren't enough units. Items that reach 0 are deleted."""
    if name not in inv:
        raise KeyError(name)
    if inv[name] < qty:
        raise ValueError("not enough")
    inv[name] -= qty
    if inv[name] == 0:  # FIX: block was missing
        del inv[name]


def merge_inventories(a, b):
    """Return a NEW inventory with the quantities of a and b summed. Don't modify a or b."""
    result = dict(a)  # FIX: was result = a
    for name, qty in b.items():
        result[name] = result.get(name, 0) + qty
    return result


def low_stock(inv, threshold):
    """Names with quantity < threshold, sorted by quantity ascending then name."""
    return sorted((n for n, q in inv.items() if q < threshold),
                  key=lambda n: (inv[n], n))  # FIX: key was missing the name tie-break


def build_index(inventories):
    """inventories: {store_name: inventory}. Return {item_name: sorted list of stores
    that stock it}."""
    index = {}
    for store, inv in inventories.items():
        for name in inv:
            index.setdefault(name, []).append(store)  # FIX: was dict.fromkeys shared list
    return {name: sorted(stores) for name, stores in index.items()}


def total_units(inventories):
    """Total number of units across all stores."""
    total = 0
    for inv in inventories.values():
        total += sum(inv.values())  # FIX: was len(inv) (number of distinct items)
    return total
