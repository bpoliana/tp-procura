import django_tables2 as tables
from .models import Medicine
from .models import Patient
from .models import HealthCenterOk


class MedicineTable(tables.Table):
	class Meta:
		model = Medicine

class PatientTable(tables.Table):
	class Meta:
		model = Patient

class HealthCenterOkTable(tables.Table):
	class Meta:
		model = HealthCenterOk
