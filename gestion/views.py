from django.shortcuts import render, redirect
from .models import Produit
from django.core.paginator import Paginator
from .forms import ProduitForm
from .models import Facture
from django.shortcuts import get_object_or_404
from datetime import date
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def produit_list(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'id')

    produits = Produit.objects.all()

    # Recherche
    if search_query:
        if search_query.isdigit():
            produits = produits.filter(id=search_query)
        else:
            produits = produits.filter(nom__icontains=search_query)

    # Tri
    if sort_option in ['nom', '-nom', 'prix', '-prix', 'date_peremption', '-date_peremption', 'id', '-id']:
        produits = produits.order_by(sort_option)

    paginator = Paginator(produits, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si POST, traiter le formulaire ici
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm()

    produits_forms = {
        produit.id: ProduitForm(instance=produit)
        for produit in page_obj if produit.id is not None
    }
    produits_supprimer = [produit for produit in page_obj if produit.id is not None]

    return render(request, 'gestion/produit_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
        'form': form,
        'form_modifier': {
            'produits_forms': produits_forms
        },
        'produits_supprimer': produits_supprimer,

    })


def facture_creer(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'nom')

    produits = Produit.objects.all()

    # Filtre
    if search_query:
        if search_query.isdigit():
            produits = produits.filter(id=search_query)
        else:
            produits = produits.filter(nom__icontains=search_query)

    # Tri
    if sort_option in ['nom', '-nom', 'prix', '-prix']:
        produits = produits.order_by(sort_option)

    # Pagination
    paginator = Paginator(produits, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        produits_ids = request.POST.getlist('produits')
        if produits_ids:
            facture = Facture.objects.create()
            facture.produits.set(produits_ids)
            return redirect('facture_detail', facture.id)

    return render(request, 'gestion/facture_creer.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option
    })


from django.core.paginator import Paginator


def facture_detail(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'id')

    produits = facture.produits.all()

    # Filtre recherche
    if search_query:
        if search_query.isdigit():
            produits = produits.filter(id=search_query)
        else:
            produits = produits.filter(nom__icontains=search_query)

    # Tri
    if sort_option in ['id', '-id', 'nom', '-nom', 'prix', '-prix']:
        produits = produits.order_by(sort_option)

    # Pagination (5 produits par page)
    paginator = Paginator(produits, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion/facture_detail.html', {
        'facture': facture,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
    })


def facture_list(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', '-date')  # par défaut les plus récentes

    factures = Facture.objects.all()

    # Recherche par ID exact
    if search_query.isdigit():
        factures = factures.filter(id=search_query)
    # Autre possibilité : recherche plus large (à étendre si tu ajoutes des champs comme client)
    elif search_query:
        factures = factures.none()  # car on ne peut pas chercher sur autre chose ici

    # Tri
    if sort_option in ['date', '-date', 'total', '-total']:
        factures = factures.order_by(sort_option)

    paginator = Paginator(factures, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion/facture_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
    })


def produit_supprimer(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        produit.delete()
        return redirect('produit_list')
    return render(request, 'gestion/confirmer_suppression.html', {
        'objet': produit,
        'type': 'produit'
    })


def facture_supprimer(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        facture.delete()
        return redirect('facture_list')
    return render(request, 'gestion/confirmer_suppression.html', {
        'objet': facture,
        'type': 'facture'
    })


def produit_modifier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'gestion/produit_form.html', {'form': form})


def facture_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    produits = facture.produits.all()

    template = get_template('gestion/facture_pdf.html')
    html = template.render({'facture': facture, 'produits': produits})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="facture_{facture.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)

    return response