import numpy as np

# 1. Create the 4x3 marks array and print shape, dtype, and size
marks = np.array([[70, 80, 90],
                  [60, 75, 85],
                  [88, 92, 79],
                  [55, 65, 70]])

print("Shape:", marks.shape)
print("Dtype:", marks.dtype)
print("Size:", marks.size)

# 2. Slice the first two students and the last subject
sliced_marks = marks[:2, -1]  #Multi-dimensional Slicing (marks[:2, -1]). Using :2 selects rows 0 and 1 (the first two students), while -1 selects the final column (the last subject), returning [90, 85]
print("\nFirst two students, last subject:", sliced_marks)

# 3. Compute each student's average (axis=1) and each subject's average (axis=0) Setting axis=1 computes the mean across columns for each row (student averages), whereas axis=0 computes the mean down rows for each column (subject averages). ex:70+80+90=80 , 70+60+88+55=68.25
student_averages = np.mean(marks, axis=1)
subject_averages = np.mean(marks, axis=0)

print("\nStudent averages:", np.round(student_averages, 2))
print("Subject averages:", subject_averages)

# 4. Use broadcasting to add 5 grace marks to every value , automatically stretches the scalar 5 across the entire 4x3 grid to add grace marks without needing loops.
grace_marks = marks + 5
print("\nGrace marks:\n", grace_marks)

# 5. Compute weighted scores using np.dot (or @) and reshape np.arange(12), np.dot(a, b) -> 0.3*70 + 0.3*80 + 0.4*90 = 21 + 24 + 36 = 81.
weights = np.array([0.3, 0.3, 0.4])
weighted_scores = np.dot(marks, weights)
print("\nWeighted scores:", weighted_scores)

reshaped_array = np.arange(12).reshape(3, 4) #The reshape function is used to construct the two-dimensional array
print("\nReshaped 3x4 array:\n", reshaped_array)

