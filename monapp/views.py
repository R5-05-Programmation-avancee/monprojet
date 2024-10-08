from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
        
# Create your views here.
from django.http import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.mail import send_mail
from monapp.forms import ContactUsForm, ProductAttributeForm, ProductAttributeValueForm, ProductForm, ProductItemForm
from monapp.models import Product, ProductAttribute, ProductAttributeValue, ProductItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(TemplateView):
    template_name = "monapp/hello.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context
    
    def post(self, request, **kwargs):
        print ("Action lors d'un post")
        return render(request, self.template_name)
    
def ContactView(request):
    
    titreh1 = "Contact us !"

    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MonProjet Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()

    return render(request, "monapp/contact.html",{'titreh1':titreh1, 'form':form})

class MailSendView(TemplateView):
    template_name = "monapp/hello.html"
    
    def get_context_data(self, **kwargs):
        context = super(MailSendView, self).get_context_data(**kwargs)
        context['titreh1'] = "Votre mail a bien été envoyé."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)

class AboutView(TemplateView):
    template_name = "monapp/hello.html"
    
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    
    def post(self, request, **kwargs):        
        return render(request, self.template_name)

class IndexView(TemplateView):
    template_name = "monapp/hello.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello " + self.kwargs.get('param') + " ! You're connected"
        return context
    
    def post(self, request, **kwargs):        
        return render(request, self.template_name)
    
class ProductListView(ListView):
    model = Product
    template_name = "monapp/list_products.html"
    context_object_name = "products"
  
    def get_queryset(self ):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        query = self.request.GET.get('search')  # Récupérer le terme de recherche depuis la requête GET
        if query:
            return Product.objects.filter(name__icontains=query)  # Filtre les produits par nom (insensible à la casse)
        
        return Product.objects.all()  # Si aucun terme de recherche, retourner tous les produits

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des produits"
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "monapp/detail_product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail produit"
        return context
    
@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class=ProductForm
    template_name = "monapp/new_product.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class=ProductForm
    template_name = "monapp/update_product.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('product-detail', product.id)

@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "monapp/delete_product.html"
    success_url = reverse_lazy('product-list')
   
class ProductItemListView(ListView):
    model = ProductItem
    template_name = "monapp/list_items.html"
    context_object_name = "productitems"
    
    def get_queryset(self ):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        query = self.request.GET.get('search')  # Récupérer le terme de recherche depuis la requête GET
        if query:
            return ProductItem.objects.filter(code__icontains=query)  # Filtre les produits par nom (insensible à la casse)
        
        return ProductItem.objects.select_related('product').prefetch_related('attributes')  
        
           
    def get_context_data(self, **kwargs):
        context = super(ProductItemListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des déclinaisons"
        return context

class ProductItemDetailView(DetailView):
    model = ProductItem
    template_name = "monapp/detail_item.html"
    context_object_name = "productitem"

    def get_context_data(self, **kwargs):
        context = super(ProductItemDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail déclinaison"

        # Récupérer les attributs associés à cette déclinaison
        context['attributes'] = self.object.attributes.all()           

        return context

@method_decorator(login_required, name='dispatch')
class ProductItemCreateView(CreateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "monapp/new_item.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('item-detail', item.id)

@method_decorator(login_required, name='dispatch')
class ProductItemUpdateView(UpdateView):
    model = ProductItem
    form_class=ProductItemForm
    template_name = "monapp/update_item.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = form.save()
        return redirect('item-detail', item.id)

@method_decorator(login_required, name='dispatch')
class ProductItemDeleteView(DeleteView):
    model = ProductItem
    template_name = "monapp/delete_item.html"
    success_url = reverse_lazy('item-list')

class ProductAttributeListView(ListView):
    model = ProductAttribute
    template_name = "monapp/list_attributes.html"
    context_object_name = "productattributes"

    def get_queryset(self ):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        query = self.request.GET.get('search')  # Récupérer le terme de recherche depuis la requête GET
        if query:
            return ProductAttribute.objects.filter(name__icontains=query)  # Filtre les produits par nom (insensible à la casse)
        
        return ProductAttribute.objects.all().prefetch_related('productattributevalue_set')  
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des attributs"
        return context

class ProductAttributeDetailView(DetailView):
    model = ProductAttribute
    template_name = "monapp/detail_attribute.html"
    context_object_name = "productattribute"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail attribut"
        context['values'] = ProductAttributeValue.objects.filter(product_attribute=self.object).order_by('position')
                       
        return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeCreateView(CreateView):
    model = ProductAttribute
    form_class=ProductAttributeForm
    template_name = "monapp/new_attribute.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attribute = form.save()
        return redirect('attribute-detail', attribute.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeUpdateView(UpdateView):
    model = ProductAttribute
    form_class=ProductAttributeForm
    template_name = "monapp/update_attribute.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        product = form.save()
        return redirect('attribute-detail', product.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeDeleteView(DeleteView):
    model = ProductAttribute
    template_name = "monapp/delete_attribute.html"
    success_url = reverse_lazy('attribute-list')
  
class RegisterView(TemplateView):

    template_name = 'monapp/register.html'
    
    def post(self, request, **kwargs):

        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monapp/login.html')
        else:
            return render(request, 'monapp/register.html')

class ConnectView(LoginView):

    template_name = 'monapp/login.html'

    def post(self, request, **kwargs):

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monapp/hello.html',{'titreh1':"hello "+username+", you're connected"})
        else:
            return render(request, 'monapp/register.html')
        
class DisconnectView(TemplateView):

    template_name = 'monapp/logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)

class ProductAttributeValueListView(ListView):
    model = ProductAttributeValue
    template_name = "monapp/list_values.html"
    context_object_name = "productattributevalues"

    def get_queryset(self ):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        query = self.request.GET.get('search')  # Récupérer le terme de recherche depuis la requête GET
        if query:
            return ProductAttributeValue.objects.filter(value__icontains=query)  # Filtre les produits par nom (insensible à la casse)
        
        return ProductAttributeValue.objects.all().select_related('product_attribute')  
    
    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste des valeurs des attributs"
        return context

class ProductAttributeValueDetailView(DetailView):
    model = ProductAttributeValue
    template_name = "monapp/detail_value.html"
    context_object_name = "productattributevalue"

    def get_context_data(self, **kwargs):
        context = super(ProductAttributeValueDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail valeur"
        return context

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueCreateView(CreateView):
    model = ProductAttributeValue
    form_class=ProductAttributeValueForm
    template_name = "monapp/new_value.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        valeur = form.save()
        return redirect('value-detail', valeur.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueUpdateView(UpdateView):
    model = ProductAttributeValue
    form_class=ProductAttributeValueForm
    template_name = "monapp/update_value.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        valeur = form.save()
        return redirect('value-detail', valeur.id)

@method_decorator(login_required, name='dispatch')
class ProductAttributeValueDeleteView(DeleteView):
    model = ProductAttributeValue
    template_name = "monapp/delete_value.html"
    success_url = reverse_lazy('value-list')