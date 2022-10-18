# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 11:16:10 2022
@author: shikhar
"""
from qiskit import QuantumCircuit, Aer, QuantumRegister, ClassicalRegister
import qiskit
import numpy as np
from qiskit.circuit.library import QFT


def preprocess(first,second):

    a_bit='{0:{fill}3b}'.format(first,fill='0')
    b_bit='{0:{fill}3b}'.format(second,fill='0')
    """
    a_bit=bin(first)[2:]
    b_bit=bin(second)[2:]
    """
    
    l1=len(a_bit)
    l2=len(b_bit)
    
    
    #Making sure that 'first' and 'second' are of the same length 
    #by padding the smaller string with zeros
    if l2>l1:
        a_bit,b_bit = b_bit, a_bit
        l2, l1 = l1, l2
    b_bit = ("0")*(l1-l2) + b_bit
    l2=len(b_bit)
    
    r_a=QuantumRegister(l1,'a')
    r_b=QuantumRegister(l2,'b')
    cr=ClassicalRegister(l1, 'c')
    qc=QuantumCircuit(r_a,r_b,cr)
    
    for i in range(l1):
        if a_bit[i]=="1":
            qc.x(r_a[l1-(i+1)])
        if b_bit[i]=="1":
            qc.x(r_b[l2-(i+1)])
    return  qc, r_a, r_b, cr, l1, l2
   
def addition(inp1,inp2):
    
    qc, r_a, r_b, cr, l1, l2 = preprocess(inp1,inp2)
    
    def controlledrotations(qc,r_a,r_b, n):
        for i in range(0,n+1):  #here for each n means for each a(n), we need contribution from all b, n is 2, 1, 0, a0 rotates pi/4, and so on
            print(i,n+1)
            qc.cu1(np.pi/2**i,r_b[n-i],r_a[n])
    
    qc.append(QFT(l1,do_swaps=False),[(l1-1)-i for i in range(l1)])
    
    
    
    for i in range(0,l2):
        controlledrotations(qc,r_a,r_b,(l2-1)-i)
    
    qc.append(QFT(l1,do_swaps=False).inverse(),[(l1-1)-i for i in range(l1)])
    
    qc.measure(r_a,cr)
    
    backend=Aer.get_backend("qasm_simulator")
    job=qiskit.execute(qc,backend,shots=1000)
    
    result=job.result()
    counts=result.get_counts(qc)
    
    final=max(counts, key=counts.get)
    return (int(final,2))



def multiply(inp1,inp2):
    csum = 0
    for i in range(inp2):
        print("ghgh",csum)
        csum=addition(inp1,csum)
    return csum

if __name__ == "__main__":
    answer=multiply(2,2)    


