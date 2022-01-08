from django.contrib import admin
from .models import Person, Role, Hosted_Centres, Appointment, Availability, Slot, Child_Case_Data, Intervention, \
    Assessment_psy, Pre_Evaluation, Evaluation_regular, Cognitive_assessment, Intervention_Cancelled, \
    All_Intervention, Skill_English, Skill_Arabic, Test, Arabic_Letter, Session, Homeworks


# Register your models here.


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'role', 'mobile_number', 'country_code', 'email']
    list_editable = ['email']

    # prepopulated_fields = {'slug': ('full_name',)}

    class Meta:
        model = Person


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_date']

    class Meta:
        model = Role


@admin.register(Hosted_Centres)
class Hosted_CentresAdmin(admin.ModelAdmin):
    list_display = ['id', 'centre_name', 'spoc_f_name', 'spoc_email']

    class Meta:
        model = Hosted_Centres


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'child', 'appointment_s_time', 'appointment_e_time', 'psychologist']

    class Meta:
        model = Appointment


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id', 'psychologist']

    class Meta:
        model = Availability


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'psychologist', 's_time', 'e_time', 'available', 'day']

    class Meta:
        model = Slot


@admin.register(Child_Case_Data)
class Child_Case_DataAdmin(admin.ModelAdmin):
    list_display = ['id', 'child']

    class Meta:
        model = Child_Case_Data


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'student', 'status']
    list_editable = ['status']

    class Meta:
        model = Intervention


@admin.register(Cognitive_assessment)
class Cognitive_assessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'test_name']

    class Meta:
        model = Assessment_psy


@admin.register(Assessment_psy)
class Assessment_psyAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'test_name', 'sub_test_name', 'sub_score', 'sub_time']
    list_editable = ['sub_score', 'sub_time']

    class Meta:
        model = Assessment_psy


@admin.register(Pre_Evaluation)
class Pre_EvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention']

    class Meta:
        model = Pre_Evaluation


@admin.register(Evaluation_regular)
class Evaluation_regularAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention']

    class Meta:
        model = Evaluation_regular


@admin.register(Intervention_Cancelled)
class Intervention_CancelledAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'reason', 'date']

    class Meta:
        model = Intervention_Cancelled


@admin.register(All_Intervention)
class All_InterventionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'status']
    list_editable = ['status']

    class Meta:
        model = All_Intervention


@admin.register(Skill_English)
class Skill_EnglishAdmin(admin.ModelAdmin):
    list_display = ['id', 'skill_name', 'a_intervention']

    class Meta:
        model = Skill_English


@admin.register(Arabic_Letter)
class Arabic_LetterAdmin(admin.ModelAdmin):
    list_display = ['id', 'letter_number']
    list_editable = ['letter_number']

    class Meta:
        model = Arabic_Letter


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'intervention', 'day', 'time']

    class Meta:
        model = Session


admin.site.register(Skill_Arabic)
admin.site.register(Test)
admin.site.register(Homeworks)
