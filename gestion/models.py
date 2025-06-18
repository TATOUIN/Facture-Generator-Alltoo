from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_peremption = models.DateField()

    def __str__(self):
        return self.nom

class Facture(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        # Calcul du total à partir des lignes de la facture
        return sum(ligne.prix_total for ligne in self.lignes.all())

    @property
    def nb_produits(self):
        # Somme des quantités de toutes les lignes
        return sum(ligne.quantite for ligne in self.lignes.all())


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)
    prix_total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.prix_total = self.prix_unitaire * self.quantite
        super().save(*args, **kwargs)
