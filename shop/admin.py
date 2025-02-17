from django.contrib import admin
from django import forms
from .models import ModelCar, CarVersion, Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["versions"].queryset = CarVersion.objects.none()

        if "models" in self.data:
            try:
                model_ids = self.data.getlist("models")  # Obtener múltiples modelos seleccionados
                self.fields["versions"].queryset = CarVersion.objects.filter(model_id__in=model_ids)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["versions"].queryset = self.instance.versions.all()

            
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "get_models", "get_versions", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name",)

    def get_models(self, obj):
        return ", ".join([m.name for m in obj.compatible_models.all()])
    get_models.short_description = "Modelos Compatibles"

    def get_versions(self, obj):
        return ", ".join([v.name for v in obj.versions.all()]) if obj.versions.exists() else "N/A"
    get_versions.short_description = "Versiones"

admin.site.register(Product, ProductAdmin)
admin.site.register(ModelCar)
admin.site.register(CarVersion)