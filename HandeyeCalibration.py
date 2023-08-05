# -*- coding: utf-8 -*-
"""

    This code replicates the hand-eye calibration protocol discussed in this paper: Calibration of Swept-Volume 3D Ultrasound: 
    https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=43070df1dc0937a6977fa9e07b6f1a4d4b23ae19

    This code is to find the transformation X for the calibration of a 3D ultrasound (US) probe attached to a self-tracked Robot Endeffector (RE).

    X is determined using hand-eye calibration AX=XB, where A and B are a corresponding pair of displacements. 

    A Knee Phantom was imaged 10 times using the 3D US probe, and the corresponding poses of RE were recorded as (Ts) in csv file, Kneecal.csv.
    Orientations were recorded in quaternions and Translations were in meters. 

    The displacements (B) between each RE pose recorded (Ts) were calculated using the forumal (B = Ts2^-1 Ts1).

    All the US volumes were manually registered to each other in a free medical image visualization software called ImFusion, 
    forming a 3D US model of the Knee phantom. These poses were labeled as (A). All 10 US volume files are stored in .mhd format in the folder (US volumes) 
    and can be visualized in ImFusion by simply importing them into the software and copying their corresponding A values.  

    X was calculated using the OpenCV function cv2.calibrateHandEye. 
    
    To test X, it was mutiplied by new (B) poses (B_test) to see if estimated (A) poses (A_est)  will register to each other in ImFusion. 
    Currently, estimted A_est are not registered to each other when visualized in ImFusion. The script is also missing a way to find the calibration error.
    I did not understand how they did it in the link attached above.
    
    To help you with the debugging, I'm completely unsure what the cause is, but it is possible that:
    There is a mistake somewhere in the code?
    The transformations obtained from ImFusion after registration, are perceived differently in Python (python maybe swaps X and Z components or rotate X before Y, for example?)
    Meter units of the RE poses should be changed to millimeters?
    This openCV hand-eye calibration function cannot be used for this task?
     
"""
r creating and breaking down Homogeneous matrices'''
# Decompose Homogeneous into Rot and Trans matrices
def decompHomogen(matr):
    rdec = []
    tdec = []
    for mat in matr:
        rdec.append(mat[0:3,0:3])
        tdec.append(mat[0:3,3])
    return rdec, tdec

# Compose Homogeneneous matrix from Rot and Trans matrices
def compHomogen(rdec, tdec):
    homogen = []
    for i in range(len(rdec)):
        temp = np.eye(4)
        temp[:3, :3] = rdec[i] 
        temp[:3, -1] = tdec[i].reshape(1,3)
        homogen.append(temp)
    return homogen

'''Read csv file for Robot Endeffector (RE) poses (TS)'''
# Read RE poses
df= pd.read_csv('Kneecal.csv')
# Store all 3 translation (original RE units are in m and quats) and 4 quaterion elements of the poses in a list
txt = df['tx']#*1000 # Not sure about units here. Should I change it to mm or keep it as it is?
tyt = df['ty']#*1000
tzt = df['tz']#*1000
rxt = df['rx']
ryt = df['ry']#from helpers import Tools
from scipy.spatial.transform import Rotation as R
#import pickle
import numpy as np
import scipy.io as sio
import cv2
import pandas as pd
import cv2

''' Functions fo
rzt = df['rz']
rwt = df['rw']

''' Convert all RE poses from quat to rotation matrices and store in rTs. Then, store RE translations in tTs'''
# Robot EF poses (rotation)
rTs = []
for i in range(len(rxt)):
    q = np.array([rxt[i], ryt[i], rzt[i], rwt[i]]) 
    rote = R.from_quat(q) #Output is a 3x3 #Convention for openCV conversion function is x, y, z, w
    rote = rote.as_matrix()
    rTs.append(rote)

# Robot EF poses (translations)
tTs=[]
for i in range(len(txt)):
    tar= np.array([txt[i], tyt[i], tzt[i]])
    tTs.append(tar)

# Combine rTs and tTs into a homogeneous representation, Ts
print("Original RE Poses:")
Ts = compHomogen(rTs, tTs)
print(Ts)

''' Find the displacement between each Ts (B) | Bi = Tsi_inv*Ts(i-1) | Break down all US poses into translations and rotations (tb and rb)'''
B = [Ts[0]]  # Initialize B with the first element of Tsc
for i in range(1, len(Ts)):
    Ts2_inv = np.linalg.inv(Ts[i])  # Calculate the inverse of Ts[i]
    Ts1 = B[i-1]  # Get the previous matrix B[i-1]
    result = np.matmul(Ts2_inv, Ts1)  # Multiply the inverse with the previous matrix
    B.append(result)  # Append the result to B

# Print the elements of B
for i, b in enumerate(B):
    print(f'B{i+1}:')
    print(b)

# Decompose B into rotational and translational elements, rb and tb
rb, tb = decompHomogen(B)

'''This is the relative pose of each US volume wrt to its previous US volume after image registration in ImFusion, (A). Store the poses in a homogeneous representation. '''
# Volume Transformations:
A1 = np.array([[1, 0, 0, 0],  [0, 1, 0, 0],  [0, 0, 1, 0],  [0, 0, 0, 1]])

A2 = np.array([[   0.98836088521617,   0.107785664377759,  -0.107354604602472,   -5.29066492533651],  
               [ -0.112582207481205,   0.992850955803737, -0.0396513066400652,   0.417926749951883],  
               [  0.102313279359851,  0.0512760189001709,   0.993429797596379,   -13.3467898496292],  
               [                  0,                   0,                   0,                   1]])

A3 = np.array([[ 0.901625787001177,  0.376846054169096,  -0.21226867802785,  -19.6208270816462],  
               [-0.413924702718315,  0.894150904926571, -0.170764456777598,   2.32003215602326],  
               [ 0.125448318817202,  0.241828887183018,  0.962175404294747,   8.47813658793148],  
               [                 0,                  0,                  0,                  1]])

A4 = np.array([[  0.929741224960622,   0.367925923326271, -0.0145523040523777,    -16.725114546695],  
               [ -0.366633059173238,   0.928685000091255,  0.0558960689742876,    4.64155032446182],  
               [  0.034080119277884, -0.0466335238858953,   0.998330536405648,    4.51324384648427],  
               [                  0,                   0,                   0,                   1]])

A5 = np.array([[ 0.911287764774395, -0.409877766375776, 0.0394312871117815,   6.66947997988431],  
               [ 0.411109022283017,  0.900219519905781, -0.143506751681261,  -2.00521086381039],  
               [0.0233234124859235,  0.146986504861536,   0.98886348189151,   6.29354039688671],  
               [                 0,                  0,                  0,                  1]])

A6 = np.array([[ 0.864103441900467, -0.390667059742341,  0.317339707770774,   12.2337116516464],  
               [ 0.400443690243837,   0.91558393705114, 0.0367546617156602,  -1.69206892717323],  
               [-0.304909974647705, 0.0953168539462401,  0.947599390414603, -0.502493116293871],  
               [                 0,                  0,                  0,                  1]])

A7 = np.array([[  0.962024301125276,  -0.263534963944546, -0.0711236024338762,    4.49043855556447],  
               [  0.269213352826089,   0.959076558811728,  0.0877287011073938,    1.81639504847844],  
               [ 0.0450933997893365,  -0.103544565847762,     0.9936020874469,    12.9260603444122],  
               [                  0,                   0,                   0,                   1]])

A8 = np.array([[  0.979679514897398,  0.0938546650606772,  -0.177255042062975,   -7.27417864127672],  
               [-0.0905371495992811,   0.995534276681184,   0.026730665822391,    0.18990303885999],  
               [  0.178972267775866,  -0.010139319465282,   0.983801871093944,   -2.83674019368916],  
               [                  0,                   0,                   0,                   1]])

A9 = np.array([[  0.992313917840267, -0.0445966204520485,  -0.115430628105176,   -4.96753831348939],  
               [ 0.0484160060719659,   0.998361559585977,  0.0304973227856993,   0.283137597791479],  
               [  0.113881424369995, -0.0358516078483476,   0.992847260860476,    5.27935542169592],  
               [                  0,                   0,                   0,                   1]])

A10 = np.array([[   0.939246544576941,   -0.343082190963736,   0.0105137407139127,     10.3881269406746],  
                [    0.34322797540266,    0.939053013749268,   -0.019338931444329,    -1.94725560687586],  
                [-0.00323811693236026,   0.0217726344740411,    0.999757704139754,     2.04966815165751],  
                [                   0,                    0,                    0,                    1]])

''' Combine All the As into one list called A'''
A = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10]

''' Training and Testing Data (data used to calculate the transformation X, and data severing as new poses to test X)  '''
# Training
A = A[:6] # use the first 6 poses for A
rb= rb[:6] # use the first 6 poses for B
tb= tb[:6]
# Testing
B_test = B[7:] # use the last 3 poses for B_test to estimate A_est from them using X

''' Break down A into translations and rotations (ta and ra)'''
ra, ta = decompHomogen(A)

'''Calibraion: Find the transfromation matrix between A and B using AX=XB'''
# OpenCV approach
rX, tX = cv2.calibrateHandEye(rb, tb, ra, ta, method=cv2.CALIB_HAND_EYE_TSAI)

# Print rX and tX
print('Transform Details: rX and tX:')
print(rX)
print(tX)

# Combine rX and tX into X
X = np.eye(4)
X[:3, :3] = rX 
X[:3, -1] = tX.reshape(1,3)

#X = np.linalg.inv(X)

''' Estimating registered ImFusion Volume Poses (A_est) by multiplying X by B_test '''
# Transform each RE pose
A_est=[]
for i in range(len(B_test)):
    XB = np.matmul(B_test[i], X)
    XB[:3, -1] = XB[:3, -1]
    A_est.append(XB)

# Print the elements of A_est
print ("Transformed ImFusion Poses:")
print(A_est)

# Print the elements of A-est
# for i, b in enumerate(A_est):
#     print(f'A_est{i+1}:')
#     print(b)
