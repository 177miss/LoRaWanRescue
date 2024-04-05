import ctypes
import numpy as np
import math
# 加载动态链接库
lib = ctypes.CDLL("appexpress/tdoa.so")  # 替换成你实际的动态链接库文件名

# 指定函数的参数和返回类型
lib.tdoa_cal.argtypes =[np.ctypeslib.ndpointer(dtype=np.float64,flags="C_CONTIGUOUS"),np.ctypeslib.ndpointer(dtype=np.float64,flags="C_CONTIGUOUS"),ctypes.c_int,np.ctypeslib.ndpointer(dtype=np.float64,flags="C_CONTIGUOUS")]
lib.tdoa_cal.restype = ctypes.POINTER(ctypes.c_double * 2)
x,y = [],[]
for i in range(5):
    x1,y1 = eval(input()),eval(input())
    x.append(x1)
    y.append(y1)
#x=[1.0, 3.0, 3.0,4.0,5.0]
#y=[1.0, 3.0, 1.0,3.0,7.0]
#gx=59.0
#gy=6.0
gx = eval(input())
gy = eval(input())
d=[]
#for (xx,yy) in zip(x,y):
 #   d.append(math.sqrt(pow(xx-gx,2)+pow(yy-gy,2)))
#for i in range(1,len(d)):
 #   d[i]=d[i]-d[0]
#d[0]=0
for i in range(5):
    t = eval(input())
    d.append(t)
input_x = np.array(x, dtype=np.float64)
input_y=np.array(y, dtype=np.float64)
# 创建整型变量和双精度变量
size = ctypes.c_int(len(input_x))
diff = np.array(d, dtype=np.float64)

# 调用C函数
result = lib.tdoa_cal(input_x,input_y,size,diff)
r=np.array(result.contents)
print(r)