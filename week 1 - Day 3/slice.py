url1 = "Python Programming"
text = "Python Programming"

# Create a reusable slice object
get_domain = slice(8, -4)
sliced_marks = text[0:6] #Extracts characters from index 0 up to index 5.
sliced_marks2 = text[:6] #Omits start, defaulting to the beginning of the string.
sliced_marks3 = text[7:] #Omits stop, slicing from index 7 to the end.
sliced_marks4 = text[-11:] #Uses negative indexing to count 11 characters back from the end.
sliced_marks5 = text[::2] #	Uses a step of 2 to grab every second character.
sliced_marks6 = text[::-1] #Uses a step of -1 to reverse the entire string.

print(url1[get_domain])
print(sliced_marks)
print(sliced_marks2)
print(sliced_marks3)
print(sliced_marks4)
print(sliced_marks5)
print(sliced_marks6)

