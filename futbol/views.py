from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django import forms

 
from futbol.models import *

# Create your views here.

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    
class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"
        
def nou_jugador(request):
    form = JugadorForm()
    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            # cridem a /classificacio/<lliga_id>
            return redirect('nou_jugador')
    return render(request, "nou_jugador.html", {
        "form": form
        })
 
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

def menuPichichi(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('pichichi',lliga.id)
    return render(request, "menu_pichichi.html",{
                    "form": form,
            })
    
def classificacio(request, lliga_id):
    lliga = get_object_or_404( Lliga, pk=lliga_id)
    equips = lliga.equips.all()
    classi = []
     
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        gols_favor = 0
        gols_contra = 0
        victories = 0
        derrotes = 0
        empates = 0
        
        for partit in lliga.partits.filter(equip_local=equip):
            gols_favor += partit.gols_local()
            gols_contra += partit.gols_visitant()
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
                victories += 1
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
                empates += 1
            else:
                derrotes += 1
        for partit in lliga.partits.filter(equip_visitant=equip):
            gols_favor += partit.gols_visitant()
            gols_contra += partit.gols_local()
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
                victories += 1
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
                empates += 1
            else:
                derrotes += 1
        classi.append({
            "nom": equip.nom,
            "punts": punts,
            "gols_favor": gols_favor,
            "gols_contra": gols_contra,
            "victories": victories,
            "derrotes": derrotes,
            "empates": empates
        })
    # ordenem llista
    # classi.sort(reverse=True, key=lambda x: x["punts"])
    classi.sort(key=lambda x: (x["punts"], x["gols_favor"] / x["gols_contra"] if x["gols_contra"] != 0 else float('inf')), reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga_nom": lliga.nom
                })
    
def pichichi(request, lliga_id):
    lliga = get_object_or_404( Lliga, pk=lliga_id)
    classi = []
    
    # Obtener todos los jugadores de los equipos de la liga
    jugadors = Jugador.objects.filter(equip__lliga=lliga)
    
    for jugador in jugadors:
        classi.append({
            "nom": jugador.nom,
            "gols": jugador.gols_marcats()
        })
    
    classi.sort(key=lambda x: x["gols"], reverse=True)

    # ordenem llista
    return render(request,"pichichi.html",
                {
                    "classificacio":classi,
                    "lliga_nom": lliga.nom
                })
        
def taulaPartits(request):
    equips = list(Equip.objects.all())  # Llista ordenada d'equips
    n = len(equips)

    # Creem una matriu buida de mida n x n amb 'x' en la diagonal
    resultats = [['' for _ in range(n + 1)] for _ in range(n + 1)]

    # Assignem noms d'equips a la primera fila i columna
    resultats[0][0] = ""
    for i in range(n):
        resultats[i + 1][0] = equips[i].nom
        resultats[0][i + 1] = equips[i].nom
        resultats[i + 1][i + 1] = "X"  # Marca la diagonal

    # Omplim la taula amb els resultats dels partits
    partits = Partit.objects.all()
    index_map = {equip.id: idx + 1 for idx, equip in enumerate(equips)}

    for partit in partits:
        i = index_map[partit.equip_local.id]
        j = index_map[partit.equip_visitant.id]
        resultat = f"{partit.gols_local()} - {partit.gols_visitant()}"
        resultats[i][j] = resultat
        resultat2 = f"{partit.gols_visitant()}-{partit.gols_local()}"
        resultats[j][i] = resultat2
    
    return render(request, 'taula_partits.html', {'resultats': resultats})