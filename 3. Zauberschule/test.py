def path_between(arr: list, location_item_a: dict, location_item_b: dict):
    # Get slices between points
    if location_item_a["row"] == location_item_b["row"]:
        sl = arr[location_item_a["row"]][min(location_item_a["col"], location_item_b["col"]) + 1 : max(location_item_a["col"], location_item_b["col"])]
    elif location_item_a["col"] == location_item_b["col"]:
        sl = [row[location_item_a["row"]] for row in arr[min(location_item_a["row"], location_item_b["row"]) + 1 : max(location_item_a["row"], location_item_b["row"])]]
    else:
        return False    

    # Validate slices only contain 1
    return all(x == 1 for x in sl)

# Example usage  
data = [[1,1,1,0],
        [1,1,0,1],
        [1,0,1,0]]

print(validate_between(data, {"row": 0, "col": 0}, {"row": 2, "col": 0})) # True 
print(validate_between(data, {"row": 0, "col": 0}, {"row": 2, "col": 3})) # False
