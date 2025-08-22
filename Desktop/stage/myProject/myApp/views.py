from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .form import LoginForm, ReunionForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Stagiaire, Reunion
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import timedelta

def login_view(request):
    form = LoginForm(request.POST or None)
    message = ""
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                message = "Identifiants incorrects."
    return render(request, 'myApp/login.html', {'form': form, 'message': message})



def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@never_cache
@login_required
def home(request):
    # Date et heure actuelles
    today = timezone.now().date()

    # Récupérer les réunions prévues aujourd'hui
    reunions_du_jour = Reunion.objects.filter(date__date=today)

    return render(request, 'myApp/home.html', {
        'reunions_du_jour': reunions_du_jour
    })

@login_required(login_url='login')
@never_cache
def stagiaire(request):
    stagiaires = Stagiaire.objects.filter(archive=False)
    return render(request, 'myApp/stagiaire.html', {'stagiaires': stagiaires})

@login_required(login_url='login')
@never_cache
def archive(request):
    stagiaires = Stagiaire.objects.filter(archive=True)
    return render(request, 'myApp/archive.html', {'stagiaires': stagiaires})

@login_required(login_url='login')
def archiver_stagiaire(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    stagiaire.archive = True
    stagiaire.save()
    return redirect('stagiaire')

@login_required(login_url='login')
@never_cache
def ajouter(request):
    if request.method == 'POST':
        Stagiaire.objects.create(
            nom=request.POST['nom'],
            prenom=request.POST['prenom'],
            email=request.POST['email'],
            telephone=request.POST['telephone'],
            universite=request.POST['universite'],
            projet=request.POST['projet'],
            type_stage=request.POST['type_stage'],
            date_debut=request.POST['date_debut'],
            date_fin=request.POST['date_fin'],
        )
        return redirect('stagiaire')
    return render(request, 'myApp/ajouter.html')

@login_required(login_url='login')
@never_cache
def modifier_stagiaire(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    if request.method == 'POST':
        stagiaire.nom = request.POST['nom']
        stagiaire.prenom = request.POST['prenom']
        stagiaire.email = request.POST['email']
        stagiaire.telephone = request.POST['telephone']
        stagiaire.universite = request.POST['universite']
        stagiaire.projet = request.POST['projet']
        stagiaire.type_stage = request.POST['type_stage']
        stagiaire.date_debut = request.POST['date_debut']
        stagiaire.date_fin = request.POST['date_fin']
        stagiaire.save()
        return redirect('stagiaire')
    return render(request, 'myApp/modifier.html', {'stagiaire': stagiaire})

@login_required(login_url='login')
@never_cache
def supprimer_stagiaire(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    stagiaire.delete()
    return redirect('stagiaire')

@login_required(login_url='login')
def restaurer_stagiaire(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    stagiaire.archive = False
    stagiaire.save()
    return redirect('archive')

@login_required(login_url='login')
@never_cache
def ajouter_reunion(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, pk=stagiaire_id)
    if request.method == 'POST':
        form = ReunionForm(request.POST)
        if form.is_valid():
            reunion = form.save(commit=False)
            reunion.stagiaire = stagiaire
            reunion.save()
            return redirect('stagiaire')  # ou autre page
    else:
        form = ReunionForm()
    return render(request, 'myApp/ajouter_reunion.html', {'form': form, 'stagiaire': stagiaire})

@login_required(login_url='login')
@never_cache
def consulter_reunions(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)  # Plus de filtre sur archive
    reunions = stagiaire.reunions.all()
    return render(request, 'myApp/consulter_reunions.html', {'stagiaire': stagiaire, 'reunions': reunions})

@login_required(login_url='login')
@never_cache   
def modifier_reunion(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    stagiaire_id = reunion.stagiaire.id  # garde l'id avant suppression

    if request.method == 'POST':
        if 'supprimer' in request.POST:
            reunion.delete()
            return redirect('consulter_reunions', stagiaire_id=stagiaire_id)
        else:
            form = ReunionForm(request.POST, instance=reunion)
            if form.is_valid():
                form.save()
                return redirect('consulter_reunions', stagiaire_id=stagiaire_id)
    else:
        form = ReunionForm(instance=reunion)

    return render(request, 'myApp/modifier_reunion.html', {'form': form, 'reunion': reunion})

@login_required(login_url='login')
@never_cache 
def dashboard(request):
    now = timezone.now()
    demain = now + timedelta(days=1)

    prochaines_reunions = Reunion.objects.filter(date__gte=now).order_by('date')[:5]
    reunion_imminente = Reunion.objects.filter(date__gte=now, date__lte=demain).order_by('date').first()

    context = {
        'prochaines_reunions': prochaines_reunions,
        'reunion_imminente': reunion_imminente,
    }
    return render(request, 'myApp/dashboard.html', context)

