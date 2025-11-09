# Python code to simulate a double pendulum using the Lagrangian angular-acceleration formulas,
# then use the kinematic relations (positions, velocities, accelerations) you requested.
# This is intentionally minimal and focused on the equations + RK4 integrator.
# It will run a short simulation and plot the two bob trajectories.
import numpy as np
import matplotlib.pyplot as plt

# Parameters
m1 = 1.0
m2 = 1.0
L1 = 1.0
L2 = 1.0
g  = 9.81

# Lagrangian-derived angular accelerations (from earlier), written as functions
def angular_accelerations(theta1, theta2, omega1, omega2):
    # Denominators and helpers
    d = 2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2)
    # theta1 double dot
    num1 = (-g*(2*m1 + m2)*np.sin(theta1)
            - m2*g*np.sin(theta1 - 2*theta2)
            - 2*np.sin(theta1 - theta2)*m2*(omega2**2*L2 + omega1**2*L1*np.cos(theta1-theta2)))
    ddtheta1 = num1 / (L1 * d)
    # theta2 double dot
    num2 = (2*np.sin(theta1 - theta2) * 
            (omega1**2*L1*(m1 + m2) + g*(m1 + m2)*np.cos(theta1) + omega2**2*L2*m2*np.cos(theta1-theta2)))
    ddtheta2 = num2 / (L2 * d)
    return ddtheta1, ddtheta2

# Convert second-order system to first-order: state = [theta1, omega1, theta2, omega2]
def deriv(state):
    theta1, omega1, theta2, omega2 = state
    ddtheta1, ddtheta2 = angular_accelerations(theta1, theta2, omega1, omega2)
    return np.array([omega1, ddtheta1, omega2, ddtheta2])

# RK4 integrator step
def rk4_step(f, y, dt):
    k1 = f(y)
    k2 = f(y + 0.5*dt*k1)
    k3 = f(y + 0.5*dt*k2)
    k4 = f(y + dt*k3)
    return y + dt*(k1 + 2*k2 + 2*k3 + k4)/6.0

# Kinematic relations (positions, velocities, accelerations) given theta, omega, alpha
def kinematics(theta1, omega1, alpha1, theta2, omega2, alpha2):
    x1 = L1*np.sin(theta1)
    y1 = -L1*np.cos(theta1)
    x2 = x1 + L2*np.sin(theta2)
    y2 = y1 - L2*np.cos(theta2)
    vx1 = L1*np.cos(theta1)*omega1
    vy1 = L1*np.sin(theta1)*omega1
    vx2 = L1*np.cos(theta1)*omega1 + L2*np.cos(theta2)*omega2
    vy2 = L1*np.sin(theta1)*omega1 + L2*np.sin(theta2)*omega2
    ax1 = -L1*np.sin(theta1)*omega1**2 + L1*np.cos(theta1)*alpha1
    ay1 =  L1*np.cos(theta1)*omega1**2 + L1*np.sin(theta1)*alpha1
    ax2 = -L1*np.sin(theta1)*omega1**2 + L1*np.cos(theta1)*alpha1 - L2*np.sin(theta2)*omega2**2 + L2*np.cos(theta2)*alpha2
    ay2 =  L1*np.cos(theta1)*omega1**2 + L1*np.sin(theta1)*alpha1 + L2*np.cos(theta2)*omega2**2 + L2*np.sin(theta2)*alpha2
    return (x1,y1,x2,y2, vx1,vy1,vx2,vy2, ax1,ay1,ax2,ay2)

# Simulation settings
dt = 0.005
T = 10.0
steps = int(T/dt)

# Initial conditions (angles in radians)
state = np.array([np.pi/2 - 0.2, 0.0, np.pi/2 + 0.4, 0.0])  # [theta1, omega1, theta2, omega2]

# Storage arrays
traj = np.zeros((steps, 12))  # will store x1,y1,x2,y2,vx1,vy1,...,ax2,ay2
times = np.zeros(steps)

for i in range(steps):
    theta1, omega1, theta2, omega2 = state
    a1, a2 = angular_accelerations(theta1, theta2, omega1, omega2)
    kin = kinematics(theta1, omega1, a1, theta2, omega2, a2)
    traj[i, :] = kin
    times[i] = i*dt
    state = rk4_step(deriv, state, dt)

# Quick plots: bob trajectories and angles over time
x1 = traj[:,0]; y1 = traj[:,1]; x2 = traj[:,2]; y2 = traj[:,3]

plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.plot(x1, y1, label='bob1 path')
plt.plot(x2, y2, label='bob2 path')
plt.gca().invert_yaxis()
plt.axis('equal')
plt.legend()
plt.title('Trajectories')

plt.subplot(1,2,2)
plt.plot(times, np.arctan2(y1, x1), label='theta1 (from pos)')
plt.plot(times, np.arctan2(y2 - y1, x2 - x1), label='theta2 (from pos)')
plt.legend()
plt.title('Angles (derived)')

plt.tight_layout()
plt.show()

# Print first 5 lines of kinematic outputs as a quick sanity check
print("t, x1, y1, x2, y2, vx1, vy1, vx2, vy2, ax1, ay1, ax2, ay2")
for i in range(5):
    line = np.concatenate(([times[i]], traj[i,:]))
    print(", ".join(f"{v:.6f}" for v in line))

