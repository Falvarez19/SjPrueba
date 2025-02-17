from django import forms
from .models import Product, CarVersion, ModelCar

class ProductForm(forms.ModelForm):
    compatible_models = forms.ModelMultipleChoiceField(
        queryset=ModelCar.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=True
    )

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image", "category", "compatible_models", "versions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["versions"].queryset = CarVersion.objects.all()  # ✅ Ahora carga todas las versiones disponibles

        if "compatible_models" in self.data:
            try:
                model_ids = [int(id) for id in self.data.getlist("compatible_models")]
                self.fields["versions"].queryset = CarVersion.objects.filter(model__id__in=model_ids)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["versions"].queryset = CarVersion.objects.filter(model__in=self.instance.compatible_models.all())

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["versions"].queryset = CarVersion.objects.all()  # ✅ Ahora carga todas las versiones disponibles

        if "models" in self.data:
            try:
                model_ids = [int(id) for id in self.data.getlist("models")]
                self.fields["versions"].queryset = CarVersion.objects.filter(model__id__in=model_ids)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["versions"].queryset = CarVersion.objects.filter(model__in=self.instance.compatible_models.all())
