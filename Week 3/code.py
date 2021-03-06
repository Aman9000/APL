
# Importing necessary libraries
from pylab import *
from scipy import special as sp
import sys

# QUESTION: 1
# Run the following command in terminal
# python3 generate_data.py

# QUESTION: 2
try:
    rawFileData = np.loadtxt("fitting.dat", usecols=(1,2,3,4,5,6,7,8,9))
except OSError:
    sys.exit("fitting.dat not found! Please run the code in generate_data.py before you run this code.")
# Creating list of columns
fileDataColumns = [[],[],[],[],[],[],[],[],[]]
# Extracting data as columns from the raw data
for i in range(len(rawFileData)):
    for j in range(len(rawFileData[i])):
        fileDataColumns[j].append(rawFileData[i][j])

# QUESTION: 3
t = linspace(0,10,101)
sigma = logspace(-1,-3,9)
# Rounding off to 3 decimal places
sigma = around(sigma,3)

# Starting new figure/plot
figure(0)
for i in range(len(fileDataColumns)):
    # Plotting the data in file
    plot(t,fileDataColumns[i],label='$\sigma_{} = {}$'.format(i, sigma[i]))

# QUESTION: 4
# Defining the vectorized form of the fitting function
def g_t(t, A, B):
    return A*sp.jn(2,t) + B*t
A = 1.05
B = -0.105
trueFunction = g_t(t, A, B)
# Plotting
plot(t, trueFunction, label='true value', color='#000000')
xlabel('$t$')
ylabel('$f(t)+n(t)$')
title('Noisy plots vs True plot')
legend()
grid()
show()

# QUESTION: 5
# Starting new figure/plot
figure(1)
xlabel('$t$')
ylabel('$f(t)$')
title('Errorbar Plot')
plot(t, trueFunction, label='f(t)', color='#000000')
# Making errorbar plot
errorbar(t[::5], fileDataColumns[0][::5], 0.1, fmt='bo', label='Error Bar')
legend()
grid()
show()

# QUESTION: 6
# Creating column vector for peforming least-squares estimation
jColumn = sp.jn(2,t)
M = c_[jColumn, t]
p = array([A, B])
# Creating matrix out of the column vectors
actual = c_[t,trueFunction]

# QUESTION: 7
# Calculating the error in fit for various combinations of A and B
A = arange(0,2,0.1)
B = arange(-0.2,0,0.01)
epsilon = zeros((len(A), len(B)))
for i in range(len(A)):
    for j in range(len(B)):
            epsilon[i][j] = mean(square(fileDataColumns[0][:] - g_t(t[:], A[i], B[j])))

# QUESTION: 8
# Starting a new figure/plot
figure(2)
# Contour plot of epsilon with A and B on axes
contPlot=contour(A,B,epsilon,levels=20)
xlabel("A")
ylabel("B")
title("Contours of $\epsilon_{ij}$")
clabel(contPlot, inline=1, fontsize=10)
# Annotating the graph with exact location of minima
plot([1.05], [-0.105], 'ro')
grid()
annotate("Exact Location\nof Minima", (1.05, -0.105), xytext=(-50, -40), textcoords="offset points", arrowprops={"arrowstyle": "->"})
show()

# QUESTION: 9
# Least squares estimation
p, *rest = lstsq(M,trueFunction,rcond=None)

# QUESTION: 10
# Starting a new plot/figure
figure(3)
perr=zeros((9, 2))
# Doing the above least square estimation by taking different columns of fitting.dat file as data
for k in range(len(fileDataColumns)):
    perr[k], *rest = lstsq(M, fileDataColumns[k], rcond=None)
# Calculating Aerr and Berr for each lstsq estimation
Aerr = array([square(x[0]-p[0]) for x in perr])
Berr = array([square(x[1]-p[1]) for x in perr])
plot(sigma, Aerr, 'o--', label='$A_{err}$')
plot(sigma, Berr, 'o--', label='$B_{err}$')
xlabel("$\sigma_{noise}$")
title("Variation of error with noise")
ylabel("MS error")
legend()
grid()
show()

# QUESTION: 11
# Starting a new plot/figure
figure(4)
# Plotting Aerr and Berr vs. sigma in a log-log scale
loglog(sigma, Aerr, 'ro', label="$A_{err}$")
loglog(sigma, Berr, 'bo', label="$B_{err}$")
legend()
errorbar(sigma, Aerr, std(Aerr), fmt='ro')
errorbar(sigma, Berr, std(Berr), fmt='bo')
xlabel("$\sigma_{noise}$")
title("Variation of error with noise")
ylabel("MS error")
legend(loc='upper right')
grid()
show()
