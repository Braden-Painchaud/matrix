from fractions import Fraction
import copy

# Main function that converts a matrix to Reduced Row Echelon Form (RREF)
def RREF(matrix):
    # Display the original matrix
    print("Your Matrix: ")
    print_matrix(matrix)
    
    # Validate that all rows have the same number of columns
    if check_matrix(matrix) != True:
        print("Error with size of matrix.")
        return
    
    # Get the dimensions of the matrix
    row_index = len(matrix) - 1
    column_index = len(matrix[0]) - 1
    check_order(matrix, row_index, column_index)
    
    # Process each row to convert to RREF
    for order in range (row_index + 1):
        # Find the first non-zero element (pivot) in the current row
        factor = first_non_zero(matrix[order])
        if factor == 0:
            continue  # Skip rows that are all zeros
        
        # Scale the row so the pivot becomes 1
        for column_again in range (column_index + 1):
            if factor != 1:
                matrix[order][column_again] /= factor
                # Fix floating point error that creates -0
                if (matrix[order][column_again] == -0):
                    matrix[order][column_again] = 0
        
        # Display the row operation performed
        if factor != 1:
            print("R" + str(order+1) + " is equal to R" + str(order+1) + "*" + str(Fraction(1/factor).limit_denominator(1000)))
            print_matrix(matrix)
            
        # Eliminate the pivot column in all rows below the current row
        for row_again in range(order + 1, row_index + 1):
            sub_value = matrix[row_again][order]  # Get the value to eliminate
            print("R" + str(row_again+1) + " is equal to R" + str(row_again+1) + " - R"+ str(order+1) + "*" + str(Fraction(sub_value).limit_denominator(1000)))
            
            # Perform row operation: subtract (sub_value * current_row) from this row
            for col in range(column_index + 1):
                if(col == 0):
                    matrix[row_again][col] = 0  # First column becomes zero
                else:
                    matrix[row_again][col] -= sub_value*matrix[order][col]
                    # Clean up floating point errors (very small numbers become 0)
                    if abs(matrix[row_again][col]) < 1e-10:
                        matrix[row_again][col] = 0

            print_matrix(matrix)
        
        # Back substitution: eliminate the pivot column in all rows above the current row
        if (order != 0):
            # Create a copy of current row scaled by the value to eliminate in the row above
            temp_row = copy.deepcopy(matrix[order])
            for i in range(column_index + 1):
                temp_row[i] *= matrix[order-1][order]
            
            print("R" + str(order) + " is equal to R" + str(order) + " - R" + str(order + 1) + "*" + str(Fraction(matrix[order-1][order]).limit_denominator(1000)))
            # Eliminate the value above the pivot
            for column in range(column_index + 1):
                matrix[order-1][column] -= temp_row[column] 
                
            print_matrix(matrix)
        
        # Reorder rows to ensure proper RREF format
        check_order(matrix, row_index, column_index)
    
    # Final pass to ensure all entries above each pivot are zero
    final_check_order(matrix, row_index, column_index)

# Swaps rows to ensure leading ones are in the correct positions (staircase pattern)
def check_order(matrix, row_index, column_index):
    # Check each column for non-zero elements
    for column in range(column_index + 1):
        # Work from bottom to top
        for row in range (row_index, -1 , -1):
                # If a non-zero element is found
                if (matrix[row][column] != 0 ):
                    # Check if the row above has all zeros up to this column
                    if ((row - 1) >= 0):
                        if(all(element == 0 for element in matrix[row - 1][0:column + 1])):
                            # Swap the rows to maintain proper order
                            temp_row = matrix[row]
                            matrix[row] = matrix[row - 1]
                            matrix[row - 1] = temp_row  
                            print("Order Swapped:")   
                            print_matrix(matrix)               


# Validates that the matrix is properly formed (all rows have same number of columns)
def check_matrix(matrix):
    # Check if matrix is empty
    if not matrix:
        return False

    # Get the number of columns
    num_of_items = len(matrix[0])
    
    # Verify all rows have the same number of columns
    for row in matrix:
        if len(row) != num_of_items:
            return False
    return True

# Final elimination pass: ensures all entries above each leading 1 are zero (reduced form)
def final_check_order(matrix, row_index, column_index):
    # For each row starting from the top
    for both in range (row_index):
        # If a leading 1 is found on the diagonal
        if matrix[both][both] == 1:
            # Eliminate all other entries in this column
            for row in range(row_index + 1):
                if row != both:  # Don't process the pivot row itself
                    if matrix[row][both] != 0:
                        # Get the multiplier needed for elimination
                        num = matrix[row][both]
                        # Eliminate the entry in this column for all columns from the pivot onward
                        for current_colum in range(both, column_index + 1):
                            matrix[row][current_colum] -= num*matrix[both][current_colum]

# Display the matrix in a formatted way
def print_matrix(matrix):
    print("______________________")
    # Convert matrix elements to fractions for cleaner display
    matrix = convert_matrix(matrix)
    # Print each row
    for row in matrix:
        for element in row:
            print(element, end="   ")  # Print elements separated by spaces
            
        print()  # New line after each row
    
    print("______________________")
        
# Converts matrix elements to fractions for cleaner display
def convert_matrix(matrix):
    converted_matrix = []
    for row in matrix:
        converted_row = []
        for element in row:
            # Keep integers as-is
            if isinstance(element, int):
                converted_row.append(element)
            # Convert floats to fractions (e.g., 0.5 becomes 1/2)
            elif isinstance(element, float):
                converted_row.append(Fraction(element).limit_denominator())
        converted_matrix.append(converted_row)
    return converted_matrix

       
# Finds the first non-zero element in an array (used to find the pivot)
def first_non_zero(arr):
    for element in arr:
        if element != 0:
            return element
    # Return 0 if all elements are zero
    return 0

# Test case: a 4x5 augmented matrix [A|b] to be converted to RREF
test_array = [
    [4, 2, -2, 0, 2],
    [4, 2, 1, 0, 3],
    [2, 4, 2, -2, 4],
    [1/3, -1/3, 1/3, 1/3, 0]
]

# Run the RREF algorithm on the test matrix
RREF(test_array)