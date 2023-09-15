def append_in_sequence(arr, obj):
    # If the array is empty, simply append the object
    if not arr:
        arr.append(obj)
        return True

    # Get the last sequence number in the array
    last_sequence = arr[-1]['sequence']

    # Check if the current object's sequence is correct
    if obj['sequence'] == last_sequence + 1:
        arr.append(obj)
        return True
    else:
        return False

# Test data with correct sequence
data_correct_sequence = [
    {'sequence': 1, 'field1': 'abc'},
    {'sequence': 2, 'field1': 'def'},
    {'sequence': 3, 'field1': 'ghi'},
    {'sequence': 4, 'field1': 'jkl'},
]

# Test data with incorrect sequence
data_incorrect_sequence = [
    {'sequence': 1, 'field1': 'abc'},
    {'sequence': 3, 'field1': 'def'},  # Incorrect sequence, should be 2
    {'sequence': 4, 'field1': 'ghi'},
]

# Initialize an empty array
result_array = []

# Append objects to the array with correct sequence
for obj in data_correct_sequence:
    if not append_in_sequence(result_array, obj):
        break

print("Array with correct sequence:", result_array)

# Clear the result_array
result_array.clear()

# Append objects to the array with incorrect sequence
for obj in data_incorrect_sequence:
    if not append_in_sequence(result_array, obj):
        break

print("Array with incorrect sequence:", result_array)
