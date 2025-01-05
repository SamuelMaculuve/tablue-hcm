from django_unicorn.components import UnicornView

from prodHCM.models import Procedure, Level, InsuranceCompanyProcedure


class AddProcedureToPlanView(UnicornView):
    level_id: int = None  # ID do Level ao qual os procedimentos serão adicionados
    insurance_company_id: int = None  # ID da InsuranceCompany (hidden input)
    supplier_id: int = None  # ID do Supplier (hidden input)
    procedures: list = []  # Lista de procedimentos exibidos na tabela
    selected_procedures: dict = {}  # Dicionário com procedimentos selecionados e seus plafons

    def mount(self):
        # Carregar procedimentos iniciais
        self.procedures = list(Procedure.objects.all().values("id", "name", "code", "base_price"))

    def toggle_procedure(self, procedure_id):
        # Selecionar ou desmarcar um procedimento
        if procedure_id in self.selected_procedures:
            del self.selected_procedures[procedure_id]
        else:
            self.selected_procedures[procedure_id] = {"plafon": 0}

    def update_plafon(self, procedure_id, plafon):
        # Atualizar o plafon de um procedimento
        if procedure_id in self.selected_procedures:
            self.selected_procedures[procedure_id]["plafon"] = plafon

    def save(self):
        # Salvar os procedimentos no nível correspondente
        level = Level.objects.get(id=self.level_id)

        for procedure_id, data in self.selected_procedures.items():
            procedure = Procedure.objects.get(id=procedure_id)

            InsuranceCompanyProcedure.objects.create(
                insuranceCompany_id=self.insurance_company_id,
                supplier_id=self.supplier_id,
                negotiated_price=data["plafon"],
                procedure=procedure
            )

        # Limpar os selecionados após salvar
        self.selected_procedures = {}
