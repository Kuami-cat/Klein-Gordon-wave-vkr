import numpy as np


class KleinGordonSolverLinearized:
    """
    Решатель обобщенного уравнения Клейна-Гордона с диссипацией линеаризованным методом
    """

    def __init__(self, x_left=0.0, x_right=1.0, T=1.0, c2=1.0, k2=1.0,
                 k0=1.0, kn=1.0, M=100, N=100,
                 u0=None, u1=None, g0=None, g1=None,
                 u_exact=None, g_source_custom=None):

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

    def solve_tridiagonal(self, A, B, C, D):
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

    def solve(self):
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

        c2_3 = (self.k2 / (2 * self.tau) + self.c2 / 2) / (self.h * self.h)

        error_history = []
        time_history = []

        all_solutions = [U0.copy(), U1.copy()]
        all_times = [0.0, self.tau]

        for n in range(1, self.N):
            t_n = n * self.tau
            t_next = t_n + self.tau

            L_Uprev = self.laplacian(U_prev)

            A = np.zeros(self.M + 1)
            B = np.zeros(self.M + 1)
            C = np.zeros(self.M + 1)
            D = np.zeros(self.M + 1)

            for i in range(1, self.M):
                A[i] = -c2_3
                C[i] = -c2_3
                B[i] = 1.0 / self.tau ** 2 + self.k0 / (2 * self.tau) + (self.kn / 2.0) * (U_curr[i] ** 2) + 2 * c2_3
                D[i] = (2.0 * U_curr[i] - U_prev[i]) / self.tau ** 2 \
                       - (self.k2 / (2 * self.tau)) * L_Uprev[i] \
                       + (self.k0 / (2 * self.tau)) * U_prev[i] \
                       + (self.c2 / 2.0) * L_Uprev[i] \
                       - (self.kn / 2.0) * (U_curr[i] ** 2) * U_prev[i] \
                       + self.g_source(self.x[i], t_n)

            B[0] = 1.0
            C[0] = 0.0
            D[0] = self.g0(t_next)

            B[self.M] = 1.0
            A[self.M] = 0.0
            D[self.M] = self.g1(t_next)

            U_next = self.solve_tridiagonal(A, B, C, D)

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
            'all_solutions': all_solutions,
            'all_times': all_times,
            'M': self.M,
            'N': self.N,
            'h': self.h,
            'tau': self.tau
        }