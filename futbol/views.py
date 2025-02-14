from django.shortcuts import render

from futbol.models import Lliga

# Create your views here.
def classificacio(request):
    lliga = Lliga.objects.first()
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

