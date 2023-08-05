# Before you run the code ensure you have installed
If you're running this code in an environment that doesn't have OpenCV installed, you'll need to install it first. You can install OpenCV using pip by running the following command:
pip install opencv-python


# Also install scipy
Open a terminal or command prompt.
Run the following command to install scipy using pip:
pip install scipy
Wait for the installation to complete. If successful, you should see a message indicating that scipy has been successfully installed.

To run the program go to command line and navigate to the file directory of the program and type
py HandeyeCalibration.py


# About the code 
The provided code performs a hand-eye calibration using the AX=XB formulation. Here's a breakdown of the code:

# 1 Import necessary libraries:

numpy for numerical operations
scipy for scientific computing
cv2 for OpenCV functions
pandas for data manipulation

# 2 Define functions:
decompHomogen(matr): Decomposes a homogeneous matrix into rotation and translation matrices.
compHomogen(rdec, tdec): Composes rotation and translation matrices into a homogeneous matrix.

# 3 Read Robot Endeffector (RE) poses from a CSV file
 using pd.read_csv(). The poses include translation (txt, tyt, tzt) and rotation (rxt, ryt, rzt, rwt) information.

# 4 Convert the RE poses from quaternion to rotation matrices 
using R.from_quat() from the scipy library. Store the rotation matrices in rTs and translations in tTs.

# 5 
Combine the rotation matrices and translations into a homogeneous representation called Ts using the compHomogen() function.

# 6
Calculate the displacement between each Ts matrix and store the results in B. This is done by finding the inverse of each Ts matrix and multiplying it with the previous Ts matrix.

# 7
Decompose the elements of B into rotational (rb) and translational (tb) elements using the decompHomogen() function.

# 8
Define the ImFusion volume transformations (A1 to A10) as homogeneous matrices and store them in a list called A.

# 9
Split the A and B data into training and testing sets. Use the first 6 poses for training (A and B) and the last 3 poses for testing (B_test).

# 10
Decompose the elements of A into rotational (ra) and translational (ta) elements using the decompHomogen() function.

# 11
Perform the hand-eye calibration using the cv2.calibrateHandEye() function from OpenCV. This function takes the rotation and translation data for both A and B and returns the transformation matrix X that satisfies the AX=XB relationship.

# 12

Transform the poses in B_test using the estimated transformation matrix X to obtain the registered ImFusion volume poses (A_est).

# 13
Print the transformation details (rX and tX) and the transformed ImFusion poses (A_est).
