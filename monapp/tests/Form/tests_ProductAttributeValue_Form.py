# tests/test_forms.py
from django.test import TestCase
from monapp.forms import ProductAttributeValueForm
from monapp.models import ProductAttribute, ProductAttributeValue

class ProductAttributeValueFormTest(TestCase):

    def setUp(self):
        self.attribute = ProductAttribute.objects.create(name="Couleur")

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec des données correctes
        """
        form = ProductAttributeValueForm(data={
            'value': 'Cyan',
            'product_attribute': self.attribute.id,
            'position': 1
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide si 'value' est manquant
        """
        form = ProductAttributeValueForm(data={
            'product_attribute': self.attribute.id,
            'position': 1
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('value', form.errors)  # Le champ 'value' doit contenir une erreur

    def test_form_invalid_product_attribute(self):
        """
        Tester que le formulaire est invalide si 'product_attribute' est manquant
        """
        form = ProductAttributeValueForm(data={
            'value': 'Cyan',
            'position': 1
        })
        self.assertFalse(form.is_valid())  # Le formulaire ne doit pas être valide
        self.assertIn('product_attribute', form.errors)  # Le champ 'product_attribute' doit contenir une erreur

    def test_form_optional_position(self):
        """
        Tester que le formulaire est valide même sans la position (champ facultatif)
        """
        form = ProductAttributeValueForm(data={
            'value': 'Vert',
            'product_attribute': self.attribute.id,
            'position': None
        })
        self.assertTrue(form.is_valid())  # Le formulaire doit être valide même sans la position

    def test_form_save(self):
        """
        Tester que le formulaire peut être enregistré avec des données valides
        """
        form = ProductAttributeValueForm(data={
            'value': 'Bleu',
            'product_attribute': self.attribute.id,
            'position': 2
        })
        self.assertTrue(form.is_valid())
        product_attribute_value = form.save()
        self.assertEqual(product_attribute_value.value, 'Bleu')
        self.assertEqual(product_attribute_value.product_attribute, self.attribute)
        self.assertEqual(product_attribute_value.position, 2)
