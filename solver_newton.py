import numpy as np


class KleinGordonSolverNewton:
    """
    Решатель обобщенного уравнения Клейна-Гордона с диссипацией методом Ньютона
    """

    def __init__(self, x_left=0.0, x_right=1.0, T=1.0, c2=1.0, k2=1.0,
                 k0=1.0, kn=1.0, M=100, N=100,
                 u0=None, u1=None, g0=None, g1=None,
                 u_exact=None, g_source_custom=None,
                 newton_tol=1e-8, max_newton_iter=30):

        self.x_left = x_left
        self.x_right = x_right
        self.L = x_right - x_left
        self.T = T

        self.c2 = c2
        self.k2 = k2
        self.k0 = k0
        self.kn = kn

        self.M = M
        self.N = N
        self.h = self.L / M
        self.tau = self.T / N

        self.newton_tol = newton_tol
        self.max_newton_iter = max_newton_iter

        self.x = np.linspace(x_left, x_right, M + 1)

        self.u0 = u0 if u0 is not None else (lambda x: np.sin(2 * np.pi * x))
        self.u1 = u1 if u1 is not None else (lambda x: -np.sin(2 * np.pi * x))
        self.g0 = g0 if g0 is not None else (lambda t: 0.0)
        self.g1 = g1 if g1 is not None else (lambda t: 0.0)

        self.u_exact_func = u_exact
        self.g_source_custom = g_source_custom

    def u_exact(self, x_val, t_val):
        if self.u_exact_func is not None:
            result = self.u_exact_func(x_val, t_val)
            if isinstance(result, np.ndarray):
                return result
            return result
        return np.sin(2 * np.pi * x_val) * np.exp(-t_val)

    def laplacian(self, U):
        M_local = len(U) - 1
        Lu = np.zeros(M_local + 1)
        for i in range(1, M_local):
            Lu[i] = (U[i + 1] - 2 * U[i] + U[i - 1]) / (self.h * self.h)
        return Lu

    def thomas_solver(self, A, B, C, D):
        """Решение трёхдиагональной системы A_i*x_{i-1} + B_i*x_i + C_i*x_{i+1} = D_i"""
        M_local = len(B) - 1
        alpha = np.zeros(M_local + 1)
        beta = np.zeros(M_local + 1)

        alpha[0] = -C[0] / B[0] if B[0] != 0 else 0
        beta[0] = D[0] / B[0] if B[0] != 0 else 0

        for i in range(1, M_local + 1):
            denom = B[i] + A[i] * alpha[i - 1]
            if abs(denom) < 1e-15:
                denom = 1e-15
            alpha[i] = -C[i] / denom
            beta[i] = (D[i] - A[i] * beta[i - 1]) / denom

        x = np.zeros(M_local + 1)
        x[M_local] = beta[M_local]
        for i in range(M_local - 1, -1, -1):
            x[i] = alpha[i] * x[i + 1] + beta[i]
        return x

    def g_source(self, x_val, t_val):
        if self.g_source_custom is not None:
            result = self.g_source_custom(x_val, t_val)
            if isinstance(result, np.ndarray):
                return result
            return result

        u = np.sin(2 * np.pi * x_val) * np.exp(-t_val)
        linear_part = (1 - self.k0 + 4 * np.pi ** 2 * (self.c2 - self.k2)) * u
        nonlinear_part = self.kn * u ** 3
        return linear_part + nonlinear_part

    def compute_RHS(self, U_curr, U_prev, Delta_U_prev, x, t_n):
        """Вычисление правой части системы"""
        M_local = len(U_curr) - 1
        RHS = np.zeros(M_local + 1)

        for i in range(1, M_local):
            RHS[i] = self.g_source(x[i], t_n) \
                     + (2 / self.tau ** 2) * U_curr[i] \
                     - (1 / self.tau ** 2) * U_prev[i] \
                     - (self.k2 / (2 * self.tau)) * Delta_U_prev[i] \
                     + (self.k0 / (2 * self.tau)) * U_prev[i] \
                     + (self.c2 / 2) * Delta_U_prev[i] \
                     - (self.kn / 4) * (U_prev[i]) ** 3

        RHS[0] = self.g0(t_n + self.tau)
        RHS[M_local] = self.g1(t_n + self.tau)

        return RHS

    def compute_residual(self, U, U_prev, RHS, A_coeff, B_lin):
        """Вычисление невязки F(U)"""
        M_local = len(U) - 1
        F = np.zeros(M_local + 1)
        for i in range(1, M_local):
            F[i] = A_coeff * (U[i - 1] + U[i + 1]) \
                   + B_lin * U[i] \
                   + (self.kn / 4.0) * (U[i] ** 3 + (U_prev[i] ** 2) * U[i] + U[i] ** 2 * U_prev[i]) \
                   - RHS[i]
        return F

    def build_jacobian(self, U, U_prev, A_coeff, B_lin):
        """Построение Якобиана (трёхдиагональная матрица)"""
        M_local = len(U) - 1
        A = np.zeros(M_local + 1)
        B = np.zeros(M_local + 1)
        C = np.zeros(M_local + 1)

        for i in range(1, M_local):
            A[i] = A_coeff
            C[i] = A_coeff
            B[i] = B_lin + (3 * self.kn / 4.0) * U[i] ** 2 \
                   + (self.kn / 4.0) * U_prev[i] ** 2 \
                   + (self.kn / 2.0) * U[i] * U_prev[i]

        B[0] = 1.0
        C[0] = 0.0
        B[M_local] = 1.0
        A[M_local] = 0.0

        return A, B, C

    def compute_energy(self, U_prev, U_curr, U_next):
        """Вычисление энергии E^n для нелинейной схемы"""
        M_local = len(U_curr) - 1

        dtU = np.zeros(M_local + 1)
        for i in range(1, M_local):
            dtU[i] = (U_next[i] - U_prev[i]) / (2 * self.tau)

        norm_dtU2 = self.h * np.sum(dtU[1:M_local] ** 2)

        H1_next = 0.0
        H1_curr = 0.0
        for i in range(1, M_local + 1):
            H1_next += (U_next[i] - U_next[i - 1]) ** 2
            H1_curr += (U_curr[i] - U_curr[i - 1]) ** 2
        H1_next /= self.h
        H1_curr /= self.h

        F_next = (self.kn / 4.0) * np.sum(U_next[1:M_local] ** 4)
        F_curr = (self.kn / 4.0) * np.sum(U_curr[1:M_local] ** 4)

        E = norm_dtU2 + (self.c2 / 2.0) * (H1_next + H1_curr) + self.h * (F_next + F_curr)
        return E

    def solve(self):
        """Основной метод решения"""
        U0 = np.array([self.u0(xi) for xi in self.x])
        u1 = np.array([self.u1(xi) for xi in self.x])

        U0[0] = self.g0(0)
        U0[self.M] = self.g1(0)

        L_U0 = self.laplacian(U0)
        L_u1 = self.laplacian(u1)

        U1 = U0 + self.tau * u1 + (self.tau ** 2 / 2.0) * (
                self.k2 * L_u1 - self.k0 * u1 + self.c2 * L_U0
                - self.kn * U0 ** 3 + self.g_source(self.x, 0)
        )

        U1[0] = self.g0(self.tau)
        U1[self.M] = self.g1(self.tau)

        U_prev = U0.copy()
        U_curr = U1.copy()
        U_next = np.zeros(self.M + 1)

        A_coeff = - (self.k2 / (2 * self.tau) + self.c2 / 2) / (self.h * self.h)
        B_lin = 1.0 / self.tau ** 2 + self.k2 / (self.tau * self.h * self.h) \
                + self.k0 / (2 * self.tau) + self.c2 / (self.h * self.h)

        error_history = []
        time_history = []
        energy_history = []
        newton_iterations_history = []

        all_solutions = [U0.copy(), U1.copy()]
        all_times = [0.0, self.tau]

        for n in range(1, self.N):
            t_n = n * self.tau
            t_next = t_n + self.tau

            Delta_U_prev = self.laplacian(U_prev)

            RHS = self.compute_RHS(U_curr, U_prev, Delta_U_prev, self.x, t_n)

            if n == 1:
                U = U_curr.copy()
            else:
                U = 2.0 * U_curr - U_prev

            newton_iter = 0
            F_norm = 0.0

            for newton_iter in range(self.max_newton_iter):
                F = self.compute_residual(U, U_prev, RHS, A_coeff, B_lin)
                F_norm = np.max(np.abs(F[1:self.M]))

                if F_norm < self.newton_tol:
                    break

                A_jac, B_jac, C_jac = self.build_jacobian(U, U_prev, A_coeff, B_lin)
                D_sys = -F.copy()
                delta = self.thomas_solver(A_jac, B_jac, C_jac, D_sys)

                alpha = 1.0
                for _ in range(8):
                    U_test = U + alpha * delta
                    F_test = self.compute_residual(U_test, U_prev, RHS, A_coeff, B_lin)
                    if np.max(np.abs(F_test[1:self.M])) < F_norm * 0.99:
                        break
                    alpha *= 0.5

                U = U + alpha * delta

            newton_iterations_history.append(newton_iter + 1)
            U_next = U.copy()

            energy = self.compute_energy(U_prev, U_curr, U_next)
            energy_history.append(energy)

            exact_at_t = np.array([self.u_exact(xi, t_next) for xi in self.x])
            err = np.sqrt(self.h * np.sum((U_next[1:self.M] - exact_at_t[1:self.M]) ** 2))
            error_history.append(err)
            time_history.append(t_next)

            all_solutions.append(U_next.copy())
            all_times.append(t_next)

            U_prev = U_curr.copy()
            U_curr = U_next.copy()

        return {
            'x': self.x,
            'U_final': U_curr,
            'U_exact': np.array([self.u_exact(xi, self.T) for xi in self.x]),
            'time_history': time_history,
            'error_history': error_history,
            'energy_history': energy_history,
            'newton_iterations_history': newton_iterations_history,
            'all_solutions': all_solutions,
            'all_times': all_times,
            'M': self.M,
            'N': self.N,
            'h': self.h,
            'tau': self.tau,
            'A_coeff': A_coeff,
            'B_lin': B_lin
        }