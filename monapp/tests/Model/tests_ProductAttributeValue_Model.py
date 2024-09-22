from django.test import TestCase
from monapp.models import ProductAttribute, ProductAttributeValue

class ProductAttributeValueModelTest(TestCase):
    def setUp(self):
        # Créer un attribut produit à utiliser dans les tests
        self.attribute = ProductAttribute.objects.create(name="Couleur")
        
        # Créer une valeur pour cet attribut
        self.value = ProductAttributeValue.objects.create(
            value="Vert",
            product_attribute=self.attribute,
            position=1
        )
    
    def test_product_attribute_value_creation(self):
        """
        Tester si une ProductAttributeValue est bien créée
        """
        self.assertEqual(self.value.value, "Vert")
        self.assertEqual(self.value.product_attribute.name, "Couleur")
        self.assertEqual(self.value.position, 1)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ProductAttributeValue
        """
        self.assertEqual(str(self.value), "Vert [Couleur]")

    def test_update_product_attribute_value(self):
        """
        Tester la mise à jour d'une ProductAttributeValue
        """
        self.value.value = "Orange"
        self.value.save()
        
        # Récupérer l'objet mis à jour
        updated_value = ProductAttributeValue.objects.get(id=self.value.id)
        self.assertEqual(updated_value.value, "Orange")

    def test_delete_product_attribute_value(self):
        """
        Tester la suppression d'une ProductAttributeValue
        """
        self.value.delete()
        self.assertEqual(ProductAttributeValue.objects.count(), 0)
