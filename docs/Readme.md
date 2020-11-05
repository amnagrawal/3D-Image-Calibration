**Task:**  

- Write a program to extract feature points from the calibration target and show them on the image. Save the image points detected in a file. 
- Read the file(s) containing 3D-2D points, generated in the previous task. Compute the intrinsic and extrinsic parameters of the camera as determined by the calibration process. Display the mean square error between the known and computed position of the image points 
- Implement the RANSAC algorithm for robust estimation. Parameters used in the RANSAC algorithm should be read from a text file named “RANSAC.config”. Final values of the Estimation should be displayed by the program. 

**Proposed Solution:** 

- To extract feature points from the calibration target we can use the OpenCV functions: cv2.findChessboardCorners and cv2.drawChessboardCorners 
- To perform camera calibration, use the following steps: 

![](Assignment%204.001.png)

- Mean Squared Error can be calculated using: 

![](Assignment%204.002.png)

- Implement the RANSAC algorithm for robust estimation.  
- Repeat k times:  
  - Draw n points uniformly at random with replacement.  
  - Fit a model to points.  
  - Find inliers in the entire set with distance less than t.  
  - Recompute model (if at least d inliers)  
  - Update parameters (k, t).  
- Number of points drawn at each attempt should be small in a hope that atleast one set will not have any outliers.  

**Implementation Details** 

- To extract feature points from the calibration target the OpenCV functions are used: cv2.findChessboardCorners and cv2.drawChessboardCorners 
- After running the first program, two files containing 2D image points and 3D object points are generated. 
- The second program performs non-coplanar camera calibration. 
- The intrinsic and extrinsic parameters of the camera are calculated using the equations above. 
- The points used for camera calibration are used as an input to the RANSAC algorithm to remove outliers. 

**Results and Inferences:** 

**Task 1:** 

![](Assignment%204.003.png)![](Assignment%204.004.png)

**Task 2 & 3** 

- Using non-coplanar calibration data: The computed camera parameters are:  rho = -419526.1371019501 

u0 = 320.00017039455435 

v0 = 239.9999709523749 

alpha\_v = 652.1740748292576 

s = -3.3983725194096597e-05 alpha\_u = 652.1740688650467 

T\* = [-2.57726950e-04  3.26846052e-05  1.04880905e+03] 

R\* = [[-7.68221190e-01  6.40184508e-01  1.46359878e-07]  [ 4.27274298e-01  5.12729182e-01 -7.44678091e-01] 

` `[-4.76731452e-01 -5.72077427e-01 -6.67423808e-01]] 

K\* = [[ 6.52174069e+02 -3.39837252e-05  3.20000170e+02]  [ 0.00000000e+00  6.52174075e+02  2.39999971e+02] 

` `[ 0.00000000e+00  0.00000000e+00  1.00000000e+00]] 

Projection Error = 4.0749739165542744e-05 

![](Assignment%204.005.png)

- It can be verified that the 2D points calculated using this algorithm are approximately 

same as the corresponding known points 

- The computed camera parameters are close to the known parameters 
- As a result, the projection error is approximately zero 
- Almost the same result is obtained after running RANSAC. This is because the data had no noise and almost all the points are inliers 



**Using Noisy version 1 data:** 

The computed camera parameters are:  

rho = -409477.35666256276 

u0 = 315.7238135738941 

v0 = 226.54021469073083 

alpha\_v = 634.9075274681129 

s = -0.5543763125583949 

alpha\_u = 633.7364518446168 

T\* = [   6.95860689   20.46810505 1024.85215282] 

R\* = [[-0.77110273  0.63668761 -0.00542859] 

` `[ 0.42023859  0.50251562 -0.75556441] 

` `[-0.47833055 -0.58489909 -0.65505187]] 

K\* = [[ 6.33736452e+02 -5.54376313e-01  3.15723814e+02]  [ 0.00000000e+00  6.34907527e+02  2.26540215e+02] 

` `[ 0.00000000e+00  0.00000000e+00  1.00000000e+00]] Projection Error = 2.148654651959668 

The camera parameters computed with RANSAC are: rho = -421625.1200856333 

u0 = 333.17407124900456 

v0 = 222.8513643938868 

alpha\_v = 641.8273212009808 

s = -6.2799993508852685 

alpha\_u = 638.4308273240985 

T\* = [ -16.43969931   29.46007292 1046.39773905] R\* = [[-0.76567813  0.64322189 -0.0016156 ] 

` `[ 0.41379236  0.49064382 -0.76684061] 

` `[-0.49245598 -0.58782161 -0.64183554]] 

K\* = [[638.43082732  -6.27999935 333.17407125] 

` `[  0.         641.8273212  222.85136439] 

` `[  0.           0.           1.        ]] 

- It can be verified that the 2D points calculated using this algorithm are close but not the same as the corresponding known points. 
- The computed camera parameters are close to the known parameters 
- A small positive projection error is obtained 
- Slightly different results are obtained after running RANSAC. This is because the data 

some noise and the outlier points are filtered out by RANSAC algorithm 



**Using Noisy version 2 data:** 

The computed camera parameters are:  

rho = 337380.17301030864 

u0 = 312.01561914740125 

v0 = 212.28232542599807 

alpha\_v = 495.9304955415624 

s = -5.519106731698332 

alpha\_u = 491.30087042436793 

T\* = [ 13.76328947  44.83081558 845.73240226] R\* = [[-0.77214303  0.63524585 -0.01605778] 

` `[ 0.41336662  0.48293491 -0.77194683] 

` `[-0.48262116 -0.60269111 -0.63548426]] 

K\* = [[491.30087042  -5.51910673 312.01561915]  [  0.         495.93049554 212.28232543] 

` `[  0.           0.           1.        ]] 

Projection Error = 7.2731994912474445 

The camera parameters computed with RANSAC are: rho = -336734.395498627 

u0 = 766.8827761179151 

v0 = 51.9270664251118 

alpha\_v = 571.1535958186623 

s = 63.99319526993775 

alpha\_u = 326.6495988831112 

T\* = [-1190.22723317   282.09151664   832.43119202] R\* = [[-0.02765392  0.89317199  0.44886419] 

` `[ 0.22551985  0.44303368 -0.86767618] 

` `[-0.97384601  0.07723314 -0.21367963]] 

K\* = [[326.64959888  63.99319527 766.88277612]  [  0.         571.15359582  51.92706643]  [  0.           0.           1.        ]] 

- It can be verified that the 2D points calculated using this algorithm are not even close to the corresponding known points. 
- The computed camera parameters are quite different from the known parameters 
- A significant positive projection error is obtained 
- Each run of the algorithm with RANSAC produces different results. Thus, RANSAC 

fails to converge to a single solution. This is because of the presence of a significant number of outliers.  

**References:** 

- <http://www.cs.iit.edu/~agam/cs512/share/intro-opencv.pdf>  
- <http://www.cs.iit.edu/~agam/cs512/share/calibeq-summary.pdf>  
- <http://www.cs.iit.edu/~agam/cs512/share/caliba.pdf>  
- [http://www.cs.iit.edu/~agam/cs512/share/calibb.pdf](http://www.cs.iit.edu/~agam/cs512/share/caliba.pdf)  
- <http://www.cs.iit.edu/~agam/cs512/share/calibc.pdf>  
