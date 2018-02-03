import os
import sys
import time
from io import BytesIO

from flask import Flask, render_template, request, send_file

# Force matplotlib to not use any Xwindows backend in Linux.
if not sys.platform.startswith('win'):
    import matplotlib
    matplotlib.use('Agg')

from options.option import OptionType, Option
from options.pricing.monte_carlo import MonteCarloPricer
from options.pricing.black_scholes import BlackScholesPricer
from options.pricing.binomial_trees import BinomialTreePricer
from options.plotting.black_scholes_plot import get_bs_plot
from options.plotting.binomial_trees_plot import get_bt_plot
from options.plotting.black_scholes_greeks_plot import get_greeks_plot


app = Flask(__name__)


@app.route('/')
def index():
    print('cwd', os.getcwd(), 'list dir', os.listdir('.'))
    return render_template('index.html')


@app.route('/pricing', methods=['POST'])
def pricing():
    otype_map = {'call': OptionType.CALL, 'put': OptionType.PUT}
    otype = otype_map[request.form.get('option_type')]
    method = request.form.get('pricing_method')

    spot = float(request.form.get('spot'))
    strike = float(request.form.get('strike'))
    rate = float(request.form.get('rate'))
    expiry = float(request.form.get('expiry'))
    vol = float(request.form.get('vol'))
    coc = request.form.get('coc')
    coc = float(coc) if coc else rate
    price, time_ = get_price(otype, method, spot, strike, rate, expiry, vol, coc)

    return render_template('result.html', price=price, time=time_)


def get_price(otype, method, spot, strike, rate, expiry, vol, coc):
    t0 = time.time()
    if method == 'formula':
        pricer = BlackScholesPricer()
    elif method == 'bitree':
        num = int(request.form.get('bt_step_num'))
        pricer = BinomialTreePricer(num)
    else:  # simulation
        num = int(request.form.get('mc_simu_num'))
        pricer = MonteCarloPricer(num, 0)

    option = Option(otype, spot, strike, rate, expiry, vol, cost_of_carry=coc)
    price = pricer.price_option(option)
    t = time.time() - t0

    return price, t


@app.route('/plotting', methods=['POST'])
def plotting():
    selected = request.form.get('view_plot')
    fig = {'formula': get_bs_plot,
           'greek': get_greeks_plot,
           'bitree': get_bt_plot}[selected]()
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/images')
def images():
    return render_template('plot.html')


#
if __name__ == '__main__':
    app.run(debug=True)
