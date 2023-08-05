#The implementation of the SD algorithm with backtracking for finding the local minimizer of f(x) = 100(x1 - x2)^2 + (x2 - 1)^2 is as follows:

import numpy as np

def f(x):
    return 100*(x[0] - x[1])**2 + (x[1] - 1)**2

def grad_f(x):
    return np.array([200*(x[0] - x[1]), 200*(x[1] - 1)])

def sd_backtracking(x0, tol=1e-10, max_iter=1000, alpha=1e-3, rho=0.9):
    x = x0
    error = np.inf
    k = 0
    while error > tol and k < max_iter:
        pk = -grad_f(x)
        t = 1
        while f(x + t*pk) > f(x) + alpha*t*np.dot(grad_f(x), pk):
            t *= rho
        x_new = x + t*pk
        error = np.linalg.norm(x_new - x)
        x = x_new
        k += 1
    return x, k

#We can then use this function to find the local minimizer:
x0 = np.array([0, 0])
x_opt, num_iter = sd_backtracking(x0)
print('Local minimizer:', x_opt)
print('Number of iterations:', num_iter)


#We can also plot the error vs iteration number:
import matplotlib.pyplot as plt

def error_vs_iteration():
    x0 = np.array([0, 0])
    errors = []
    k = 0
    while k < 100:
        x, _ = sd_backtracking(x0, tol=1e-10, max_iter=k+1)
        error = np.linalg.norm(x - np.array([1, 1]))
        errors.append(error)
        k += 1
    plt.plot(range(1, len(errors)+1), errors)
    plt.xlabel('Iteration number')
    plt.ylabel('Error')
    plt.title('Steepest Descent with Backtracking')
    plt.show()

error_vs_iteration()


#4 The implementation of the BFGS algorithm for finding the local minimizer of f(x) = 100(x1 - x2)^2 + (x2 - 1)^2 is as follows:
def bfgs(x0, tol=1e-10, max_iter=1000):
    x = x0
    H = np.eye(2)
    error = np.inf
    k = 0
    while error > tol and k < max_iter:
        pk = -np.dot(H, grad_f(x))
        t = 1
        while f(x + t*pk) > f(x) + alpha*t*np.dot(grad_f(x), pk):
            t *= rho
        s = t*pk
        x_new = x + s
        y = grad_f(x_new) - grad_f(x)
        rho = 1/np.dot(y, s)
        A = np.eye(2) - rho*np.outer(s, y)
        B = np.eye(2) - rho*np.outer(y, s)
        H = np.dot(A, np.dot(H, B)) + rho*np.outer(s, s)
        error = np.linalg.norm(x_new - x)
        x = x_new
        k += 1
    return x, k

#We can then use this function to find the local minimizer:
x0 = np.array([0, 0])
x_opt, num_iter = bfgs(x0)
print('Local minimizer:', x_opt)
print('Number of iterations:', num_iter)

#We can also plot the error vs iteration number:
def error_vs_iteration_bfgs():
    x0 = np.array([0, 0])
    errors = []
    k = 0
    while k < 100:
        x, _ = bfgs(x0, tol=1e-10, max_iter=k+1)
        error = np.linalg.norm(x - np.array([1, 1]))
        errors.append(error)
        k += 1
    plt.plot(range(1, len(errors)+1), errors)
    plt.xlabel('Iteration number')
    plt.ylabel('Error')
    plt.title('BFGS')
    plt.show()

error_vs_iteration_bfgs()

