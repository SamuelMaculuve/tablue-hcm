from django.core.management.base import BaseCommand
from prodHCM.models import SupplierType


class Command(BaseCommand):
    help = "Seed the database with default healthcare suppliersType."

    def handle(self, *args, **kwargs):
        suppliersType = [
            "Hospitais",
            "Clínicas e Consultórios",
            "Laboratórios de Diagnóstico",
            "Centros de Reabilitação",
            "Casas de Repouso",
            "Agentes Comunitários de Saúde",
            "Plataformas de Telemedicina",
            "Postos de Saúde Móveis",
            "Nutricionistas e Dietistas",
            "Massoterapeutas",
            "ONGs de Saúde",
            "Centros de Saúde Primária",
        ]

        for suppliersType_data in suppliersType:
            supplierType, created = SupplierType.objects.get_or_create(
                name=suppliersType_data["name"],
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {supplierType.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{supplierType.name} already exists."))
