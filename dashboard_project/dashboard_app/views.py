from django.shortcuts import render, redirect
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as opy
import os
import ast
from django.http import HttpResponse

DATA = pd.read_csv(os.path.join('dashboard_app', 'static', 'csv', 'web_data.csv'))
chromosomes = ['chr' + str(i) for i in range(1, 23)]
seq_number = 100

# Create your views here.
def dashboard_view(request):
    selected_chr = request.POST.get('selected_chr')
    selected_chr_data = DATA.loc[DATA["name"] == selected_chr]
    seq_number = 0  # Default value if no matching rows found
    if not selected_chr_data.empty:
        prediction = ast.literal_eval(selected_chr_data.iloc[0, 2])
        seq_number = len(prediction)
    return render(request, 'dashboard_app/dashboard.html', {'chromosomes': chromosomes, 'row_length': seq_number})


def handle_form_submission(request):
    if request.method == 'POST':
        selected_chr = request.POST.get('selected_chr')
        selected_chr_data = DATA.loc[DATA["name"] == selected_chr]
        mean_length = selected_chr_data.iloc[0, 1]
        prediction_percent = ast.literal_eval(selected_chr_data.iloc[0, 2])
        seq_number = len(prediction_percent)
        selected_start = int(request.POST.get('selected_row_start'))
        selected_end = int(request.POST.get('selected_row_end'))

        hovertext = [f"Probability: {value}" for value in prediction_percent[selected_start:selected_end]]
        # Create the bar plot
        fig = go.Figure(data=[go.Bar(x=[i * 1800 for i in range(selected_start, selected_end)], y=prediction_percent[selected_start:selected_end], hovertext=hovertext)])
        # Set axes labels and title
        fig.update_layout(
            xaxis_title="Index of first nucleotide in sequence",
            yaxis_title='Probability of the sequence being an enhancer',
            title=f'Our prediction plot for {selected_chr} where mean enhancer length is {mean_length}',
        )
        div = opy.plot(fig, auto_open=False, output_type='div')

        return render(request, 'dashboard_app/dashboard.html', context={'plot_div': div, 'chromosomes': chromosomes, 'row_length': seq_number})

    else:
        # If not POST, redirect to the main view
        return redirect('dashboard_view')



def download_data(request):
    file_path = os.path.join('dashboard_app', 'static', 'csv', 'web_data.csv')
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=web_data.csv'
        return response