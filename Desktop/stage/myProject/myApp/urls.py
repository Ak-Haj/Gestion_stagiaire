from . import views
from django.urls import path

urlpatterns = [
   path('login/', views.login_view, name='login'),  # <== mise à jour ici
    path('home/', views.home, name='home'),
    path("stagiaire/", views.stagiaire, name="stagiaire"),
    path('archive/', views.archive, name='archive'),
    path('logout/', views.logout_view, name='logout'), 
    path('ajouter/', views.ajouter, name='ajouter'),
    path("modifier/<int:stagiaire_id>/", views.modifier_stagiaire, name="modifier_stagiaire"),
    path("supprimer/<int:stagiaire_id>/", views.supprimer_stagiaire, name="supprimer_stagiaire"),
    path("archiver/<int:stagiaire_id>/", views.archiver_stagiaire, name="archiver_stagiaire"),
    path("restaurer/<int:stagiaire_id>/", views.restaurer_stagiaire, name="restaurer_stagiaire"),
    path('stagiaire/<int:stagiaire_id>/ajouter-reunion/', views.ajouter_reunion, name='ajouter_reunion'),
    path('stagiaire/<int:stagiaire_id>/reunions/', views.consulter_reunions, name='consulter_reunions'),
    path('reunion/<int:reunion_id>/modifier/', views.modifier_reunion, name='modifier_reunion'),
    path('dashboard/', views.dashboard, name='dashboard'),
]