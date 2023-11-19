from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages
from django.http import HttpResponse

def update_equipment(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    # Your logic to update the equipment
    return HttpResponse("Equipment updated successfully!")
def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    context = {
        "characters": characters,
        "equipements": equipements,
    }
    return render(request, 'blog/character_list.html', context)

 
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    lieu = character.lieu

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            nouveau_lieu = get_object_or_404(Equipement, id_equip=form.cleaned_data['lieu'].id_equip)

            if nouveau_lieu.id_equip == "école des ninjas" and character.etat == "apaisé":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                character.etat = "recherche de défi"
                character.lieu = nouveau_lieu

            elif nouveau_lieu.disponibilite == "libre":
                if (nouveau_lieu.id_equip == "guerre" and character.etat == "recherche de défi") or \
                   (nouveau_lieu.id_equip == "centre de soins" and character.etat == "bataille") or \
                   (nouveau_lieu.id_equip == "salle de méditation" and character.etat == "traumatisé/bléssé"):
                    ancien_lieu.disponibilite = "libre"
                    nouveau_lieu.disponibilite = "occupé"
                    character.etat = "bataille" if nouveau_lieu.id_equip == "guerre" else \
                                     "traumatisé/bléssé" if nouveau_lieu.id_equip == "centre de soins" else \
                                     "apaisé"
                    character.lieu = nouveau_lieu

                else:
                    messages.error(request, "Le changement n'est pas autorisé car l'état du personnage ne correspond pas.")
                    return redirect('character_detail', id_character=id_character)

            else:
                messages.error(request, "Le changement n'est pas autorisé car le lieu n'est pas libre.")
                return redirect('character_detail', id_character=id_character)

            ancien_lieu.save()
            nouveau_lieu.save()
            character.save()
            return redirect('character_detail', id_character=id_character)

    else:
        form = MoveForm(instance=character)
        return render(request, 'blog/character_detail.html', {'character': character, 'lieu': lieu, 'form': form})


