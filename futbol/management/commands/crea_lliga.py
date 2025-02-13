from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
 
from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            any_fundacio = randint(1890, 2010)
            equip = Equip(ciutat=ciutat,nom=nom,lliga=lliga, any_fundacio = any_fundacio)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                dorsal = randint(1,99)
                jugador = Jugador(nom=nom,posicio=posicio,
                    dorsal=dorsal,equip=equip)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for equip_local in lliga.equips.all():
            for equip_visitant in lliga.equips.all():
                if equip_local!=equip_visitant:
                    partit = Partit(equip_local=equip_local,equip_visitant=equip_visitant, lliga = lliga)
                    partit.save()
                    
                    # crear Event tipus gol
                    cantitat_gols = randint(0, 10)
                    for i in range(cantitat_gols):
                        temps = randint(1, 90)
                        # seleccionar jugador d'algun dels dos equips
                        if randint(0, 1) == 0:
                            jugador = equip_local.jugadors.order_by('?').first()  # Selecciona un jugador aleatorio del equipo local
                        else:
                            jugador = equip_visitant.jugadors.order_by('?').first()  # Selecciona un jugador aleatorio del equipo visitante
                        # guardar gol
                        event = Event(partit=partit, jugador=jugador, tipus_esdeveniment = "gol", minut=temps)
                        
                        event.save()