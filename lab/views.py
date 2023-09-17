from django.shortcuts import render, redirect
from django import forms

from .simulation import Simulation

PARTICLES = 50
MASS = 1.2e-20
RADIUS = 0.01
V0, Vf = 0.5, 15


class LabForm(forms.Form):
    temp = forms.FloatField(
        label="Temperature (K)",
        initial=273,
        min_value=1,
        max_value=20000,
    )
    time = forms.FloatField(
        label="Time (s)",
        initial=5,
        min_value=1,
        max_value=20,
    )


def index(request):
    if request.method == "POST":
        form = LabForm(request.POST)
        if form.is_valid():
            request.session["temp"] = form.cleaned_data["temp"]
            request.session["time"] = form.cleaned_data["time"]
            return redirect("simulation", permanent=False)
    else:
        form = LabForm()
    return render(request, "lab/index.html", {"form": form, "particles": PARTICLES})


def simulation(request):
    temp = request.session.get("temp")
    time = request.session.get("time")
    ani = Simulation(PARTICLES, MASS, RADIUS, temp, 2, time, 0.05)
    video = ani.to_html5_video()
    return render(request, "lab/simulation.html", {"video": video})
