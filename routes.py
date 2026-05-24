"""
Маршруты Flask для обработки запросов
"""

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import render_template_string, jsonify
import numpy as np
import io
import base64

from config import THEMES, EQUATION_FONT_SIZE, COEFF_LABEL_FONT_SIZE, SECTION_FONT_SIZE, LABEL_FONT_SIZE, \
    INPUT_FONT_SIZE, LABEL_COLOR
from templates import HTML_TEMPLATE
from utils import make_function_with_coeffs
from solver import KleinGordonSolver
from solver2 import KleinGordonSolverLinearized
from solver_newton import KleinGordonSolverNewton


def register_routes(app):
    """Регистрация маршрутов в приложении Flask"""
    @app.route('/')
    @app.route('/set_theme/<theme_name>')
    def home(theme_name='paper'):
        """Главная страница с выбором темы"""
        if theme_name not in THEMES:
            theme_name = 'paper'

        return render_template_string(
            HTML_TEMPLATE,
            themes=THEMES,
            current_theme=theme_name,
            theme=THEMES[theme_name],
            equation_font_size=EQUATION_FONT_SIZE,
            coeff_label_font_size=COEFF_LABEL_FONT_SIZE,
            section_font_size=SECTION_FONT_SIZE,
            label_font_size=LABEL_FONT_SIZE,
            input_font_size=INPUT_FONT_SIZE,
            label_color=LABEL_COLOR
        )

    @app.route('/solve', methods=['POST'])
    def solve():
        """API endpoint для решения уравнения"""
        from flask import request

        try:
            data = request.json

            method = data.get('method', 'iterative')

            k0_val = float(data.get('k0', 1))
            k2_val = float(data.get('k2', 1))
            c2_val = float(data.get('c2', 1))
            kn_val = float(data.get('kn', 1))
            no_exact_solution = data.get('no_exact_solution', False)
            num_x_output = data.get('num_x_output', 5)
            num_t_output = data.get('num_t_output', 11)
            find_u_at_x = data.get('find_u_at_x', '').strip()
            find_x_at_u = data.get('find_x_at_u', '').strip()
            enable_research = data.get('enable_research', False)
            research_param_names = data.get('research_param_names', [])
            research_rows = data.get('research_rows', [])

            custom_vars = data.get('custom_variables', {})

            base_coefficients = {
                'k0': k0_val, 'k_0': k0_val,
                'k2': k2_val, 'k_2': k2_val,
                'c2': c2_val, 'c_2': c2_val, 'c^2': c2_val,
                'kn': kn_val, 'k_n': kn_val
            }

            custom_values = {}
            for var_name, var_expr in custom_vars.items():
                if var_name and var_expr:
                    try:
                        expr_processed = var_expr
                        for name, val in custom_values.items():
                            expr_processed = expr_processed.replace(name, str(val))
                        for coeff_name, coeff_val in base_coefficients.items():
                            expr_processed = expr_processed.replace(coeff_name, str(coeff_val))

                        from utils import parse_expression
                        f = parse_expression(expr_processed, [], {})
                        val = float(f())
                        custom_values[var_name] = val
                        base_coefficients[var_name] = val
                    except Exception as e:
                        raise ValueError(f"Ошибка вычисления переменной '{var_name}' = '{var_expr}': {str(e)}")

            base_params = {
                'x_left': float(data.get('x_left', 0)),
                'x_right': float(data.get('x_right', 1)),
                'T': float(data.get('T', 1)),
                'c2': c2_val,
                'k2': k2_val,
                'k0': k0_val,
                'kn': kn_val,
                'M': int(data.get('M', 100)),
                'N': int(data.get('N', 100)),
            }

            ic_str = data.get('ic', 'sin(2*pi*x)')
            ic_deriv_str = data.get('ic_deriv', '-sin(2*pi*x)')
            bc_left_str = data.get('bc_left', '0')
            bc_right_str = data.get('bc_right', '0')
            exact_solution_str = data.get('exact_solution', 'sin(2*pi*x)*exp(-t)') if not no_exact_solution else '0'
            source_str = data.get('source', '0')

            u0_func = make_function_with_coeffs(ic_str, ['x'], base_coefficients)
            u1_func = make_function_with_coeffs(ic_deriv_str, ['x'], base_coefficients)
            g0_func = make_function_with_coeffs(bc_left_str, ['t'], base_coefficients)
            g1_func = make_function_with_coeffs(bc_right_str, ['t'], base_coefficients)

            if no_exact_solution:
                exact_func = None
            else:
                exact_func = make_function_with_coeffs(exact_solution_str, ['x', 't'], base_coefficients)

            source_func = make_function_with_coeffs(source_str, ['x', 't'], base_coefficients)

            if method == 'iterative':
                solver_params = {
                    **base_params,
                    'nonlinear_type': data.get('nonlinear_type', 'cubic'),
                    'max_iter': int(data.get('max_iter', 50)),
                    'tol': 10 ** int(data.get('tol_exp', -8)),
                    'u0': u0_func, 'u1': u1_func, 'g0': g0_func, 'g1': g1_func,
                    'u_exact': exact_func, 'g_source_custom': source_func
                }
                solver = KleinGordonSolver(**solver_params)
            elif method == 'linearized':
                solver_params = {
                    **base_params,
                    'u0': u0_func, 'u1': u1_func, 'g0': g0_func, 'g1': g1_func,
                    'u_exact': exact_func, 'g_source_custom': source_func
                }
                solver = KleinGordonSolverLinearized(**solver_params)
            else:  # method == 'newton'
                solver_params = {
                    **base_params,
                    'u0': u0_func, 'u1': u1_func, 'g0': g0_func, 'g1': g1_func,
                    'u_exact': exact_func, 'g_source_custom': source_func,
                    'newton_tol': 10 ** int(data.get('newton_tol_exp', -8)),
                    'max_newton_iter': int(data.get('newton_max_iter', 30))
                }
                solver = KleinGordonSolverNewton(**solver_params)

            results = solver.solve()

            x_min = base_params['x_left']
            x_max = base_params['x_right']
            output_x = np.linspace(x_min, x_max, num_x_output)

            x_indices = []
            for x_val in output_x:
                idx = np.argmin(np.abs(results['x'] - x_val))
                x_indices.append(idx)

            all_times = results.get('all_times', [0.0])
            total_times = len(all_times)
            time_indices = np.linspace(0, total_times - 1, min(num_t_output, total_times), dtype=int)

            table_html = '<div class="table-wrapper">\n<table>\n<thead>\n<tr>\n<th>t</th>'
            for x_val in output_x:
                table_html += f'<th>x={x_val:.4f}</th>'
            if method == 'iterative':
                table_html += '<th>итераций</th>'
            elif method == 'newton':
                table_html += '<th>итераций</th>'
            if not no_exact_solution:
                table_html += '<th>ошибка</th>'
            table_html += '</tr>\n</thead>\n<tbody>\n'

            all_solutions = results.get('all_solutions', [results['U_final']])
            all_iterations = results.get('all_iterations', [0] * len(all_solutions)) if method == 'iterative' else []
            newton_iterations_history = results.get('newton_iterations_history', []) if method == 'newton' else []
            error_history = results.get('error_history', [])

            for t_idx in time_indices:
                if t_idx >= len(all_solutions):
                    continue
                t_val = all_times[t_idx]
                solution = all_solutions[t_idx]
                iter_count = all_iterations[t_idx] if t_idx < len(all_iterations) else 0

                table_html += '<tr>\n'
                table_html += f'<td>t={t_val:.4f}</td>\n'
                for idx in x_indices:
                    if idx < len(solution):
                        table_html += f'<td>{solution[idx]:.6f}</td>\n'
                    else:
                        table_html += '<td>0.000000</td>\n'
                if method == 'iterative':
                    table_html += f'<td>{iter_count}</td>\n'
                elif method == 'newton':
                    if t_idx < len(newton_iterations_history):
                        table_html += f'<td>{newton_iterations_history[t_idx]}</td>\n'
                    else:
                        table_html += '<td>0</td>\n'
                if not no_exact_solution:
                    if t_idx == 0:
                        error_val = 0.0
                    else:
                        error_idx = t_idx - 1
                        if error_idx < len(error_history):
                            error_val = error_history[error_idx]
                        else:
                            error_val = 0.0
                    table_html += f'<td>{error_val:.6e}</td>\n'
                table_html += '</tr>\n'

            table_html += '</tbody>\n</table>\n</div>'

            search_results_html = ''

            if find_u_at_x:
                try:
                    x_target = float(find_u_at_x)
                    if x_min <= x_target <= x_max:
                        idx = np.argmin(np.abs(results['x'] - x_target))
                        u_value = results['U_final'][idx]
                        exact_x = results['x'][idx]
                        search_results_html += f'<p>При x = {exact_x:.6f} значение u(x,T) = <span class="result-value">{u_value:.6f}</span></p>'
                    else:
                        search_results_html += f'<p style="color: red;">Ошибка: x = {x_target} вне интервала [{x_min}, {x_max}]</p>'
                except ValueError:
                    search_results_html += f'<p style="color: red;">Ошибка: неверное значение x = "{find_u_at_x}"</p>'

            if find_x_at_u:
                try:
                    u_target = float(find_x_at_u)
                    diffs = np.abs(results['U_final'] - u_target)
                    min_diff = np.min(diffs)
                    if min_diff <= 1e-6:
                        indices = np.where(diffs <= 1e-6)[0]
                        x_values = [results['x'][i] for i in indices]
                        if len(x_values) == 1:
                            search_results_html += f'<p>Значение u = {u_target:.6f} достигается при x = <span class="result-value">{x_values[0]:.6f}</span></p>'
                        else:
                            x_str = ', '.join([f'{x:.6f}' for x in x_values])
                            search_results_html += f'<p>Значение u = {u_target:.6f} достигается при x = {x_str}</p>'
                    else:
                        closest_idx = np.argmin(diffs)
                        closest_u = results['U_final'][closest_idx]
                        closest_x = results['x'][closest_idx]
                        search_results_html += f'<p>Точное значение u = {u_target:.6f} не найдено. Ближайшее значение u = {closest_u:.6f} достигается при x = {closest_x:.6f}</p>'
                except ValueError:
                    search_results_html += f'<p style="color: red;">Ошибка: неверное значение u = "{find_x_at_u}"</p>'

            fig1, ax1 = plt.subplots(figsize=(8, 5))
            ax1.plot(results['x'], results['U_final'], 'b-', linewidth=2, label='Численное решение')

            if not no_exact_solution and exact_func is not None:
                exact_final = np.array([exact_func(xi, base_params['T']) for xi in results['x']])
                ax1.plot(results['x'], exact_final, 'r--', linewidth=2, label='Точное решение')
                ax1.legend()

            ax1.set_xlabel('x', fontsize=12)
            ax1.set_ylabel('u(x,T)', fontsize=12)
            ax1.grid(True)
            ax1.set_facecolor('white')
            fig1.patch.set_facecolor('white')
            plt.tight_layout()

            buf1 = io.BytesIO()
            fig1.savefig(buf1, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf1.seek(0)
            plot_solution = base64.b64encode(buf1.read()).decode()
            plt.close(fig1)

            plot_error = None
            if not no_exact_solution and exact_func is not None and results.get('error_history'):
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                ax2.plot(results['time_history'], results['error_history'], 'b-', linewidth=2)
                ax2.set_xlabel('Время t', fontsize=12)
                ax2.set_ylabel('L₂ ошибка', fontsize=12)
                ax2.grid(True)
                ax2.set_yscale('log')
                ax2.set_facecolor('white')
                fig2.patch.set_facecolor('white')
                plt.tight_layout()

                buf2 = io.BytesIO()
                fig2.savefig(buf2, format='png', dpi=100, bbox_inches='tight', facecolor='white')
                buf2.seek(0)
                plot_error = base64.b64encode(buf2.read()).decode()
                plt.close(fig2)

            plot_energy = None
            if method == 'newton' and results.get('energy_history'):
                fig3, ax3 = plt.subplots(figsize=(8, 5))
                ax3.plot(results['time_history'], results['energy_history'], 'g-', linewidth=2)
                ax3.set_xlabel('Время t', fontsize=12)
                ax3.set_ylabel('Энергия E(t)', fontsize=12)
                ax3.grid(True)
                ax3.set_facecolor('white')
                fig3.patch.set_facecolor('white')
                plt.tight_layout()

                buf3 = io.BytesIO()
                fig3.savefig(buf3, format='png', dpi=100, bbox_inches='tight', facecolor='white')
                buf3.seek(0)
                plot_energy = base64.b64encode(buf3.read()).decode()
                plt.close(fig3)

            research_plots = []
            if enable_research and research_rows and research_param_names:
                for row_idx, row_values in enumerate(research_rows):
                    current_coeffs = base_coefficients.copy()
                    run_params = base_params.copy()

                    param_str_parts = []
                    for i, param_name in enumerate(research_param_names):
                        if i < len(row_values) and row_values[i] is not None and str(row_values[i]).strip() != '':
                            value = row_values[i]
                            param_str_parts.append(f"{param_name}={value}")

                            if param_name == 'k0':
                                run_params['k0'] = float(value)
                                current_coeffs['k0'] = float(value)
                                current_coeffs['k_0'] = float(value)
                            elif param_name == 'k2':
                                run_params['k2'] = float(value)
                                current_coeffs['k2'] = float(value)
                                current_coeffs['k_2'] = float(value)
                            elif param_name == 'c2' or param_name == 'c^2':
                                run_params['c2'] = float(value)
                                current_coeffs['c2'] = float(value)
                                current_coeffs['c_2'] = float(value)
                                current_coeffs['c^2'] = float(value)
                            elif param_name == 'kn':
                                run_params['kn'] = float(value)
                                current_coeffs['kn'] = float(value)
                                current_coeffs['k_n'] = float(value)
                            elif param_name == 'T':
                                run_params['T'] = float(value)
                            elif param_name == 'M':
                                run_params['M'] = int(float(value))
                            elif param_name == 'N':
                                run_params['N'] = int(float(value))
                            elif param_name in current_coeffs:
                                current_coeffs[param_name] = float(value)

                    param_str = ', '.join(param_str_parts)

                    run_u0_func = make_function_with_coeffs(ic_str, ['x'], current_coeffs)
                    run_u1_func = make_function_with_coeffs(ic_deriv_str, ['x'], current_coeffs)
                    run_g0_func = make_function_with_coeffs(bc_left_str, ['t'], current_coeffs)
                    run_g1_func = make_function_with_coeffs(bc_right_str, ['t'], current_coeffs)
                    run_source_func = make_function_with_coeffs(source_str, ['x', 't'], current_coeffs)

                    try:
                        if method == 'iterative':
                            run_solver = KleinGordonSolver(
                                **run_params,
                                nonlinear_type=data.get('nonlinear_type', 'cubic'),
                                max_iter=int(data.get('max_iter', 50)),
                                tol=10 ** int(data.get('tol_exp', -8)),
                                u0=run_u0_func, u1=run_u1_func, g0=run_g0_func, g1=run_g1_func,
                                u_exact=None, g_source_custom=run_source_func
                            )
                        elif method == 'linearized':
                            run_solver = KleinGordonSolverLinearized(
                                **run_params,
                                u0=run_u0_func, u1=run_u1_func, g0=run_g0_func, g1=run_g1_func,
                                u_exact=None, g_source_custom=run_source_func
                            )
                        else:  # method == 'newton'
                            run_solver = KleinGordonSolverNewton(
                                **run_params,
                                u0=run_u0_func, u1=run_u1_func, g0=run_g0_func, g1=run_g1_func,
                                u_exact=None, g_source_custom=run_source_func,
                                newton_tol=10 ** int(data.get('newton_tol_exp', -8)),
                                max_newton_iter=int(data.get('newton_max_iter', 30))
                            )
                        run_results = run_solver.solve()

                        fig, ax = plt.subplots(figsize=(6, 4))
                        ax.plot(run_results['x'], run_results['U_final'], 'b-', linewidth=2, label='Численное решение')
                        ax.set_xlabel('x', fontsize=10)
                        ax.set_ylabel('u(x,T)', fontsize=10)
                        ax.set_title(f'{param_str}', fontsize=10)
                        ax.grid(True)
                        ax.set_facecolor('white')
                        fig.patch.set_facecolor('white')
                        plt.tight_layout()

                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
                        buf.seek(0)
                        plot_img = base64.b64encode(buf.read()).decode()
                        plt.close(fig)

                        research_plots.append({
                            'title': param_str,
                            'image': plot_img
                        })
                    except Exception as e:
                        print(f"Ошибка при исследовании параметров: {e}")

            return jsonify({
                'error': None,
                'l2_error': f"{results['error_history'][-1]:.2e}" if results.get('error_history') else "Нет данных",
                'h': f"{results['h']:.6f}",
                'tau': f"{results['tau']:.6f}",
                'courant': f"{results['tau'] / results['h']:.4f}",
                'M': base_params['M'],
                'N': base_params['N'],
                'c2': base_params['c2'],
                'k2': base_params['k2'],
                'k0': base_params['k0'],
                'kn': base_params['kn'],
                'plot_solution': plot_solution,
                'plot_error': plot_error,
                'plot_energy': plot_energy,
                'table_html': table_html,
                'search_results_html': search_results_html,
                'research_plots': research_plots
            })

        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500