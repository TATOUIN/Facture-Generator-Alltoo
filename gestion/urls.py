from django.urls import path
from . import views

urlpatterns = [
    path('', views.produit_list, name='produit_list'),
    path('produits/', views.produit_list, name='produit_list'),
    path('factures/creer/', views.facture_creer, name='facture_creer'),
    path('facture/<int:facture_id>/', views.facture_detail, name='facture_detail'),
    path('factures/', views.facture_list, name='facture_list'),
    path('produit/<int:produit_id>/supprimer/', views.produit_supprimer, name='produit_supprimer'),
    path('facture/<int:facture_id>/supprimer/', views.facture_supprimer, name='facture_supprimer'),
    path('produit/<int:produit_id>/modifier/', views.produit_modifier, name='produit_modifier'),
]
