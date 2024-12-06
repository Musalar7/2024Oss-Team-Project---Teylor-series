import sympy as sp
import numpy as np
import plotly.graph_objects as go

class TaylorSeriesPlotter:
    def __init__(self, function, variable='x'):
        self.function = sp.sympify(function)
        self.variable = sp.Symbol(variable)

    def taylor_series(self, center, order):
        """
        Sympy의 series 메서드가 지정된 차수보다 하나 높은 항까지 계산해서
        결과가 예상과 다르게 보일 수도 있습니다. 출력된 급수로 비교해 보세요. 일단 조금 손봤습니다
        """
        taylor_expr = sp.series(self.function, self.variable, center, order + 1).removeO()
        print(f"Taylor Series Expansion (Order {order}): {taylor_expr}")
        return taylor_expr

    def plot_comparison(self, center, orders, x_range=(-10, 10), num_points=500):
        x_vals = np.linspace(x_range[0], x_range[1], num_points)
        original_func = sp.lambdify(self.variable, self.function, modules="numpy")
        y_original = original_func(x_vals)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_original, mode='lines', name='Original Function'
        ))

        for order in orders:
            taylor_expr = self.taylor_series(center, order)
            taylor_func = sp.lambdify(self.variable, taylor_expr, modules="numpy")
            y_taylor = taylor_func(x_vals)

            fig.add_trace(go.Scatter(
                x=x_vals, y=y_taylor, mode='lines', name=f'Taylor Series (Order {order})'
            ))

        fig.update_layout(
            title=f"Taylor Series Approximation Comparison (Center: {center})",
            xaxis_title="x",
            yaxis_title="f(x)",
            legend_title="Functions",
            template="plotly_white"
        )

        fig.show()


if __name__ == "__main__":
    function_input = input("function(e.g., sin(x), exp(x), log(1+x)): ")
    center_input = float(input("center: "))
    orders_input = input("degrees(e.g., 2,4,6): ")
    orders = list(map(int, orders_input.split(',')))

    plotter = TaylorSeriesPlotter(function_input)
    plotter.plot_comparison(center=center_input, orders=orders)