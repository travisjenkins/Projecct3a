from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import StockForm
from .charts import *


@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    
    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Get the form data to query the api
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            # start_date = convert_date(request.form['start_date'])
            # end_date = convert_date(request.form['end_date'])
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            #query the api using the form data
            # if get_date(end_date) <= get_date(start_date):
            #     #Generate error message as pass to the page
            #     err = "ERROR: End date cannot be earlier than Start date."
            #     chart = None
            # else:
                
            #     err = None
                 
            #THIS IS WHERE YOU WILL CALL THE METHODS FROM THE CHARTS.PY FILE AND IMPLEMENT YOUR CODE
            try:
                stock_data = StockData(symbol, int(time_series), start_date, end_date)
            except Exception as ex:
                err = f"ERROR:  {ex}"
                chart = None
            else:
                if not stock_data.data_dictionary.items():
                    err = "ERROR:  There was no data for the time period specified."
                    chart = None
                else:
                    err = None
                    stock_chart = StockChart(symbol, int(chart_type), start_date, end_date, stock_data)
        
                    #This chart variable is what is passed to the stock.html page to render the chart returned from the api
                    chart = stock_chart.get_chart()

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")
