import matplotlib.pyplot as plt
import scipy.optimize
import math
import scipy.linalg
from scipy import linalg
from scipy.linalg import expm
import numpy as np
import sys
import time

from IBMQuantumExperience import IBMQuantumExperience
import IBMQuantumExperience

import Qconfig
api = IBMQuantumExperience.IBMQuantumExperience(Qconfig.APItoken, Qconfig.config)

args = sys.argv

a = int(args[1])
b = int(args[2])

def Bin(a,b):
    La,Lb=str(bin(a))[2:],str(bin(b))[2:]
    x=""""""
    for i in range(len(La)):
        if La[i] == "1":
            x=x+"""x a[{}];""".format(len(La)-i-1)
    for j in range(len(Lb)):
        if Lb[j] == "1":
            x=x+"""x b[{}];""".format(len(Lb)-j-1)
    return(x)

circuit1 = """
include "qelib1.inc";
gate majority a,b,c 
{ 
  cx c,b; 
  cx c,a; 
  ccx a,b,c; 
}
gate unmaj a,b,c 
{ 
  ccx a,b,c; 
  cx c,a; 
  cx a,b; 
}

// add a to b, storing result in b
gate add8 a0,a1,a2,a3,a4,a5,a6,a7,b0,b1,b2,b3,b4,b5,b6,b7,cin,cout 
{
  majority cin,b0,a0;
  majority a0,b1,a1;
  majority a1,b2,a2;
  majority a2,b3,a3;
  majority a3,b4,a4;
  majority a4,b5,a5;
  majority a5,b6,a6;
  majority a6,b7,a7;
  cx a7,cout;
  unmaj a6,b7,a7;
  unmaj a5,b6,a6;
  unmaj a4,b5,a5;
  unmaj a3,b4,a4;
  unmaj a2,b3,a3;
  unmaj a1,b2,a2;
  unmaj a0,b1,a1;
  unmaj cin,b0,a0;
}

gate add7 a0,a1,a2,a3,a4,a5,a6,b0,b1,b2,b3,b4,b5,b6,cin,cout 
{
  majority cin,b0,a0;
  majority a0,b1,a1;
  majority a1,b2,a2;
  majority a2,b3,a3;
  majority a3,b4,a4;
  majority a4,b5,a5;
  majority a5,b6,a6;
  cx a6,cout;
  unmaj a5,b6,a6;
  unmaj a4,b5,a5;
  unmaj a3,b4,a4;
  unmaj a2,b3,a3;
  unmaj a1,b2,a2;
  unmaj a0,b1,a1;
  unmaj cin,b0,a0;
}

// add two 8-bit numbers by calling the 4-bit ripple-carry adder
// carry bit on output lives in carry[0]
qreg carry[2];
qreg a[15];
qreg b[15];
creg ans[16];
"""

iv = Bin(a,b)

circuit2 = """
add8 a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],carry[0],carry[1];
add7 a[8],a[9],a[10],a[11],a[12],a[13],a[14],b[8],b[9],b[10],b[11],b[12],b[13],b[14],carry[1],carry[0];

measure b[0] -> ans[0];
measure b[1] -> ans[1];
measure b[2] -> ans[2];
measure b[3] -> ans[3];
measure b[4] -> ans[4];
measure b[5] -> ans[5];
measure b[6] -> ans[6];
measure b[7] -> ans[7];
measure b[8] -> ans[8];
measure b[9] -> ans[9];
measure b[10] -> ans[10];
measure b[11] -> ans[11];
measure b[12] -> ans[12];
measure b[13] -> ans[13];
measure b[14] -> ans[14];
measure carry[0] -> ans[15];
"""

circuit = circuit1 + iv + circuit2

qcircuit=[{'qasm': 'OPENQASM 2.0;\n' + circuit}]

def get_result_simulator():
    backend = 'ibmq_qasm_simulator'
    #backend = 'ibmqx2'
    #backend = 'ibmqx4'
    
    #jobを投げる
    response = api.run_job(qcircuit, backend ,shots = 8192, max_credits = 15) 
    #print(response)

    #id を取得する
    id = response["id"]
    
    #resulttmpに情報を格納する
    resulttmp = api.get_job(id)
    
    #'RUNNING'担っている間ずっと問い合わせる
    while(resulttmp["status"]=='RUNNING'):
        time.sleep(1)
        resulttmp = api.get_job(id)
        print("request...{}, return {}".format(id,resulttmp["status"]))
    
    #'RUNNING'が終わると get_jobの値を返す
    #print(resulttmp)
    return resulttmp

start = time.time()
result = get_result_simulator()
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

num_sample = result["shots"]
#prob0 = 1.0* result["qasms"][0]["data"]["counts"]["0000"]/num_sample
#prob1 = 1.0* result["qasms"][0]["data"]["counts"]["0001"]/num_sample

result_list = list(result["qasms"][0]["data"]["counts"])

print(int(result_list[0],2))