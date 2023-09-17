from django.shortcuts import render, redirect
from django import forms


class LabForm(forms.Form):
    temp = forms.FloatField(
        label="Temperature (K)",
        initial=273,
        min_value=1,
        max_value=20000,
    )


def index(request):
    if request.method == "POST":
        form = LabForm(request.POST)
        if form.is_valid():
            temp = form.cleaned_data["temp"]
            request.session["temp"] = temp
            return redirect("simulation", permanent=False)
    else:
        form = LabForm()
    return render(request, "lab/index.html", {"form": form})


def simulation(request):
    print(request.session.get("temp"))
    return render(request, "lab/simulation.html", {})
