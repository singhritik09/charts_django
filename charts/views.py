# charts/views.py

from django.shortcuts import render, redirect
from .models import Application
from .forms import ApplicationForm
from django import forms
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2020, datetime.now().year + 1)),
        required=False,
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2020, datetime.now().year + 1)),
        required=False,
        label="End Date"
    )

# View for submitting the application data
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_applications')
    else:
        form = ApplicationForm()

    return render(request, 'charts/submit_application.html', {'form': form})

# View for viewing all submitted applications
def view_applications(request):
    applications = Application.objects.all()
    form = DateRangeForm(request.GET)

    type_counts = {
        'emergency': 0,
        'planned': 0,
        'superfix': 0
    }

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date:
            applications = applications.filter(date_of_register__gte=start_date)
        if end_date:
            applications = applications.filter(date_of_register__lte=end_date)

        type_counts['emergency'] = applications.filter(application_type='emergency').count()
        type_counts['planned'] = applications.filter(application_type='planned').count()
        type_counts['superfix'] = applications.filter(application_type='superfix').count()

    # Plotly Bar Chart
    types = list(type_counts.keys())
    counts = list(type_counts.values())

    bar_data = [go.Bar(x=types, y=counts, marker=dict(color=['red', 'blue', 'green']))]
    layout = go.Layout(title='Applications by Type', xaxis=dict(title='Application Type'), yaxis=dict(title='Number of Applications'))

    fig = go.Figure(data=bar_data, layout=layout)
    plot_div = plot(fig, output_type='div')

    return render(request, 'charts/view_applications.html', {
        'applications': applications,
        'form': form,
        'plot_div': plot_div
    })

# View for viewing all submitted applications (Chart.js)
def view_applications_chart(request):
    applications = Application.objects.all()
    form = DateRangeForm(request.GET)

    type_counts = {
        'emergency': 0,
        'planned': 0,
        'superfix': 0
    }

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date:
            applications = applications.filter(date_of_register__gte=start_date)
        if end_date:
            applications = applications.filter(date_of_register__lte=end_date)

        # Debugging: print the filtered queryset
        print("Filtered Applications:", applications)

        type_counts['emergency'] = applications.filter(application_type='emergency').count()
        type_counts['planned'] = applications.filter(application_type='planned').count()
        type_counts['superfix'] = applications.filter(application_type='superfix').count()

        # Debugging: print the counts
        print("Type Counts:", type_counts)

    # Prepare data for Chart.js
    types = list(type_counts.keys())
    counts = list(type_counts.values())

    return render(request, 'charts/newchart.html', {
        'applications': applications,
        'form': form,
        'types': types,
        'counts': counts
    })
