import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

class Sampling_frequency:
    # Initialize variables
    def __init__(self,k):
        self.k = k
        self.filter_length = 2*self.k+1
        self.max_num=self.filter_length*500
        self.ideal_filter_0 = None
        self.ideal_filter = None
        self.r0 = None
        self.r1 = None
        self.r2 = None

    # Ideal filter Hd (-0.5 ~ 0.5)
    def H(self,F):
        return 2*math.pi*1j*F

    # Ideal filter Hd (0 ~ 1)
    def HH(self,F):
        if(F <= 0.5 and F >= 0):
            return self.H(F)
        elif(F <= 1 and F > 0.5):
            return  self.H(F-1)

    # Compute R(F)
    def R(self,F):
        result = 0
        center = len(self.r2)//2
        #center = 0
        for i in range(len(self.r2)):
            result += self.r2[i]*cmath.exp(-1*1j*2*math.pi*F*(i-center))
        return result

    # Compute r1[n], r[n]
    def compute(self):
        # ideal filter
        x0 = np.linspace(-0.5,0.5,self.max_num)
        x = np.linspace(0,1,self.max_num)
        self.ideal_filter_0 = np.empty(self.max_num,dtype = 'complex_')
        for i in range(len(x0)):
            self.ideal_filter_0[i] = self.H(x0[i])

        # ideal filter with shift
        self.ideal_filter = np.empty(self.max_num,dtype = 'complex_')
        for i in range(len(x)):
            self.ideal_filter[i] = self.HH(x[i])

        # sampled points
        x = np.linspace(0,1,self.filter_length+1)
        self.r0 = np.empty(self.filter_length,dtype = 'complex_')
        for i in range(self.filter_length):
            if(i == self.k or i == self.k+1):
                self.r0[i] = 0.7*self.HH(x[i])
            else:
                self.r0[i] = self.HH(x[i])

        # r1[n]
        self.r1 = np.fft.ifft(self.r0).real

        # r[n]
        self.r2 = np.empty(len(self.r1))
        self.r2[:self.filter_length//2] = self.r1[self.filter_length//2+1:]
        self.r2[self.filter_length//2:] = self.r1[:self.filter_length//2+1]

        print(f'r0: {self.r0}')
        print(f'r1: {self.r1}')
        print(f'r2: {self.r2}')

    # Show results
    def show(self):
        n0 = np.linspace(0,1,self.filter_length+1)[:self.filter_length]
        n1 = np.linspace(0,self.filter_length-1,self.filter_length)
        n2 = np.linspace(-1*self.filter_length//2,self.filter_length//2,self.filter_length)
        x0 = np.linspace(-0.5,0.5,self.max_num)
        x = np.linspace(0,1,self.max_num)

        # Setting the figure
        super_title = f'Hd(F) = j*2*pi*F, -0.5 < F < 0.5\nk = {self.k}, number of sampled points = 2*k+1'
        plt.figure(figsize=(10,4))
        plt.suptitle(super_title,fontsize = 8)

        #ideal filter
        plt.subplot(231)
        plt.title('Hd (-0.5 ~ 0.5)')
        plt.xlabel('F')
        plt.ylabel('imag')
        plt.plot(x,self.ideal_filter_0.imag)

        # r0
        plt.subplot(232)
        plt.title('Hd (0 ~ 1)')
        plt.xlabel('F')
        plt.ylabel('imag')
        plt.plot(x,self.ideal_filter.imag,label='ideal')
        plt.plot(n0,np.array(self.r0).imag,'*',label='sample')
        plt.legend(loc='upper right',fontsize=5)

        # r1[n]
        plt.subplot(233)
        plt.title('r1[n]')
        plt.xlabel('n')
        plt.ylabel('real')
        plt.bar(n1,self.r1)

        #r[n]
        plt.subplot(234)
        plt.title('r[n]')
        plt.xlabel('n')
        plt.ylabel('real')
        plt.bar(n2,self.r2)

        #h[n]
        plt.subplot(235)
        plt.title('h[n] (Impulse Response)')
        plt.xlabel('n')
        plt.ylabel('real')
        plt.bar(n1,self.r2)

        # R(F)
        y1 = []
        y2 = []
        y3 = []
        for i in range(len(x)): 
            y1.append(self.R(x[i]))
            y2.append(self.R(x[i]).real)
            y3.append(self.R(x[i]).imag)

        plt.subplot(236)
        plt.title('R(f) (Frequncy Response)')
        plt.xlabel('F')
        plt.ylabel('imag')
        plt.plot(x,self.ideal_filter.imag,label='ideal')
        plt.plot(n0,np.array(self.r0).imag,'*',label='sample')
        plt.plot(x,y3,label='R(F) (Frequncy Response)')
        plt.legend(loc='upper right',fontsize=5)

        # Save and show the graph
        plt.tight_layout()
        plt.savefig('results.png', dpi=300)
        plt.show()

        




