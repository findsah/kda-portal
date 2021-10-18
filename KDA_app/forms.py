from django import forms
from .models import Person, Child_Case_Data
from django.core.exceptions import ValidationError


ROLES = [('Admin', 'Admin'), ('Trainer', 'Trainer'), ('Centre', 'Centre'), ('Individual', 'Individual'),
         ('Secretary', 'Secretary'),
         ('Physiologist', 'Physiologist'), ('Student', 'Student'), ('Receptionist', 'Receptionist')]
Gender = [('Male', 'Male'), ('Female', 'Female')]


# class login_form(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     # rolee = forms.ChoiceField(choices=ROLES, widget=forms.Select, initial='')
#
#     class Meta:
#         model = Person
#         fields = ['username', 'password']


class login_form(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())


class register_form(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=Gender, required=True)
    dob = forms.DateField(widget=forms.DateInput, required=True)
    profile_picture = forms.ImageField(required=True)
    street = forms.CharField(required=True)
    block = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    country = forms.CharField(required=True)
    postalcode = forms.CharField(required=True)
    qualification = forms.CharField(required=True)
    institution = forms.CharField(required=True)
    mobile = forms.IntegerField(min_value=0, required=True)
    email = forms.EmailField(required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        a = Person.objects.filter(username=username)
        if a:
            raise ValidationError("username is taken")
        return username


class register_centre_form(forms.Form):
    centre_name = forms.CharField(required=True)
    hc_logo = forms.ImageField(required=True)
    hc_document = forms.FileField(required=False)

    qualification = forms.CharField(required=False)
    institution = forms.CharField(required=False)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    street = forms.CharField(required=True)
    block = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    country = forms.CharField(required=True)
    postalcode = forms.CharField(required=False)

    spoc_mobile_number = forms.IntegerField(min_value=0, required=True)
    spoc_email = forms.EmailField(required=True)
    spoc_extension = forms.IntegerField(min_value=0, required=False)
    spoc_office_number = forms.IntegerField(min_value=0, required=False)

    centre_mobile_number_1 = forms.IntegerField(min_value=0, required=True)
    centre_mobile_number_2 = forms.IntegerField(min_value=0, required=False)
    centre_office_number = forms.IntegerField(min_value=0, required=False)
    centre_extension_number = forms.IntegerField(min_value=0, required=False)
    centre_email = forms.EmailField(required=True)
    centre_web_address = forms.CharField(required=False)


class add_appointment_form(forms.Form):
    appointment_date = forms.CharField(required=True)


Relationship_btw_parents = [('Close', 'Close'), ('Far', 'Far'), ('There is none', 'There is none')]
Martial_status_parents = [('Still exists', 'Still exists'), ('Does not exist', 'Does not exist')]
Parent_passed = [('Father', 'Father'), ('Mother', 'Mother'), ('Both of Them', 'Both of Them')]
If_married = [('Before Marriage Of Parents', 'Before Marriage Of Parents'), ('After Marriage Of Parents', 'Before Marriage Of Parents')]


class child_case_form(forms.Form):
    # Initial Data
    # Child Data
    civil_number = forms.IntegerField(min_value=0, required=False)
    school_name = forms.CharField(required=False)
    # dob = forms.DateField(widget=forms.DateInput, required=True)
    dob = forms.CharField(required=False)
    place_of_birth = forms.CharField(required=False)
    nationality = forms.CharField(required=False)
    grade = forms.CharField(required=False)

    # Father Data
    father_name = forms.CharField(required=False)
    age_f = forms.IntegerField(min_value=0, required=False)
    nationality_f = forms.CharField(required=False)
    education_level_f = forms.CharField(required=False)
    phone_f = forms.IntegerField(min_value=0, required=False)
    current_occupation_f = forms.CharField(required=False)
    residence_address_f = forms.CharField(required=False)
    email_f = forms.EmailField(required=False, empty_value='portal@q8da.com')

    # Mother Data
    mother_name = forms.CharField(required=False)
    age_m = forms.IntegerField(min_value=0, required=False)
    nationality_m = forms.CharField(required=False)
    phone_m = forms.IntegerField(min_value=0, required=False)
    education_level_m = forms.CharField(required=False)
    current_occupation_m = forms.CharField(required=False)
    residence_address_m = forms.CharField(required=False)
    email_m = forms.EmailField(required=False, empty_value='portal@q8da.com')

    # Guardian Data
    guardian_name = forms.CharField(required=False)
    education_level_g = forms.CharField(required=False)
    relation_to_child = forms.CharField(required=False)
    phone_g = forms.IntegerField(min_value=0, required=False)
    current_occupation_g = forms.CharField(required=False)
    residence_address_g = forms.CharField(required=False)
    email_g = forms.EmailField(required=False, empty_value='portal@q8da.com')

    # Family
    child_living_with = forms.CharField(required=False)
    nationality_second_marriage = forms.CharField(required=False)
    number_of_family_members = forms.IntegerField(min_value=0, required=False)
    number_of_brothers = forms.IntegerField(min_value=0, required=False)
    number_of_sisters = forms.IntegerField(min_value=0, required=False)
    number_of_brothers_from_father = forms.IntegerField(min_value=0, required=False)
    number_of_sisters_from_father = forms.IntegerField(min_value=0, required=False)
    number_of_brothers_from_mother = forms.IntegerField(min_value=0, required=False)
    number_of_sisters_from_mother = forms.IntegerField(min_value=0, required=False)
    order_sibling = forms.IntegerField(min_value=0, required=False)
    others_living_in_house = forms.CharField(required=False)
    lives_with = forms.CharField(required=False)

    # during pregnancy
    state_of_mind_preg = forms.CharField(required=False)
    age_during_preg = forms.CharField(required=False)
    health_psy_preg = forms.CharField(required=False)
    kind_of_accident_preg = forms.CharField(required=False)
    medicines_drugs_preg = forms.CharField(required=False)
    prob_disease_preg = forms.CharField(required=False)

    # delivery period
    baby_weight_birth = forms.IntegerField(min_value=0, required=False)
    prob_birth = forms.CharField(required=False)
    complications_birth = forms.CharField(required=False)

    # post birth period
    health_psy_post_b = forms.CharField(required=False)
    period_incubator = forms.CharField(required=False)
    surgery_baby = forms.CharField(required=False)

    # problems faced by case
    extremely_high_temp_age = forms.IntegerField(min_value=0, required=False)
    extremely_high_temp_dur = forms.CharField(required=False)
    ear_problems_age = forms.IntegerField(min_value=0, required=False)
    ear_problems_dur = forms.CharField(required=False)
    vision_problems_age = forms.IntegerField(min_value=0, required=False)
    vision_problems_dur = forms.CharField(required=False)
    juandice_age = forms.IntegerField(min_value=0, required=False)
    juandice_dur = forms.CharField(required=False)
    asthma_age = forms.IntegerField(min_value=0, required=False)
    asthma_dur = forms.CharField(required=False)
    allergy_age = forms.IntegerField(min_value=0, required=False)
    allergy_dur = forms.CharField(required=False)
    poisoning_age = forms.IntegerField(min_value=0, required=False)
    poisoning_dur = forms.CharField(required=False)
    surgical_age = forms.IntegerField(min_value=0, required=False)
    surgical_dur = forms.CharField(required=False)
    surgery = forms.CharField(required=False)
    accident_age = forms.IntegerField(min_value=0, required=False)
    accident_dur = forms.CharField(required=False)
    accident = forms.CharField(required=False)
    not_mentioned_disease = forms.CharField(required=False)

    # stages of growth
    weaning_age = forms.IntegerField(min_value=0, required=False)
    age_tooth_start = forms.IntegerField(min_value=0, required=False)
    age_commune = forms.IntegerField(min_value=0, required=False)
    age_simple_words = forms.IntegerField(min_value=0, required=False)
    age_speech = forms.IntegerField(min_value=0, required=False)
    age_sentence = forms.IntegerField(min_value=0, required=False)
    age_bottle_carry = forms.IntegerField(min_value=0, required=False)
    age_love = forms.IntegerField(min_value=0, required=False)
    age_sat = forms.IntegerField(min_value=0, required=False)
    age_stop = forms.IntegerField(min_value=0, required=False)
    age_walk = forms.IntegerField(min_value=0, required=False)
    age_wore_help = forms.IntegerField(min_value=0, required=False)
    age_wore_self = forms.IntegerField(min_value=0, required=False)
    age_shoes = forms.IntegerField(min_value=0, required=False)
    age_feed = forms.IntegerField(min_value=0, required=False)
    age_urination = forms.IntegerField(min_value=0, required=False)
    age_bathroom_train = forms.IntegerField(min_value=0, required=False)
    age_glasses = forms.IntegerField(min_value=0, required=False)
    age_hearing_aid = forms.IntegerField(min_value=0, required=False)
    age_speech_centre = forms.IntegerField(min_value=0, required=False)
    age_stop_left_hand = forms.IntegerField(min_value=0, required=False)
    age_involutary_urination = forms.IntegerField(min_value=0, required=False)
    medicine_name = forms.CharField(required=False)
    medicine_reason = forms.CharField(required=False)
    appetite = forms.CharField(required=False)
    fav_food = forms.CharField(required=False)

    # family history
    hyperinactivity = forms.CharField(widget=forms.Textarea, required=False)
    reading = forms.CharField(widget=forms.Textarea, required=False)
    writing_dictating = forms.CharField(widget=forms.Textarea, required=False)
    reading_inactivity = forms.CharField(widget=forms.Textarea, required=False)
    calculating = forms.CharField(widget=forms.Textarea, required=False)
    concentration = forms.CharField(widget=forms.Textarea, required=False)
    pronouncing = forms.CharField(widget=forms.Textarea, required=False)
    hearing = forms.CharField(widget=forms.Textarea, required=False)
    visual = forms.CharField(widget=forms.Textarea, required=False)
    mobility = forms.CharField(widget=forms.Textarea, required=False)
    intellectual = forms.CharField(widget=forms.Textarea, required=False)
    down_syndrome = forms.CharField(widget=forms.Textarea, required=False)
    autism = forms.CharField(widget=forms.Textarea, required=False)
    other_problems = forms.CharField(widget=forms.Textarea, required=False)
    age_discovered = forms.IntegerField(required=False)
    effecting_child = forms.CharField(required=False)

    # Social Relations
    friends = forms.CharField(required=False)
    siblings = forms.CharField(required=False)
    parents = forms.CharField(required=False)
    adults = forms.CharField(required=False)
    maid = forms.CharField(required=False)
    maid_rel_age = forms.IntegerField(min_value=0, required=False)
    fam_auth = forms.CharField(required=False)
    link_fam = forms.CharField(required=False)
    punisher = forms.CharField(required=False)
    spending_time = forms.CharField(required=False)
    hobbies_child = forms.CharField(required=False)
    m_lang = forms.CharField(required=False)
    o_lang = forms.CharField(required=False)

    # Behaviour
    mental_illnesses = forms.CharField(required=False)

    # school
    s_name_1 = forms.CharField(required=False)
    s_enroll_1 = forms.CharField(required=False)
    s_beh_1 = forms.CharField(required=False)

    s_name_2 = forms.CharField(required=False)
    s_enroll_2 = forms.CharField(required=False)
    s_beh_2 = forms.CharField(required=False)

    s_name_3 = forms.CharField(required=False)
    s_enroll_3 = forms.CharField(required=False)
    s_beh_3 = forms.CharField(required=False)

    first_stage = forms.CharField(required=False)
    failure_class = forms.CharField(required=False)
    failure_subjs = forms.CharField(required=False)
    advantage = forms.CharField(required=False)
    teachers_note = forms.CharField(required=False)
    achievement = forms.CharField(required=False)

    motivation = forms.CharField(required=False)
    enthusiasm = forms.CharField(required=False)
    time_punctuality = forms.CharField(required=False)
    fav_articles = forms.CharField(required=False)
    least_fav_material = forms.CharField(required=False)
    rel_teachers = forms.CharField(required=False)
    desire_school = forms.CharField(required=False)
    absent_reasons = forms.CharField(required=False)

    # Other Info
    follow_up = forms.CharField(widget=forms.Textarea, required=False)
    # reason_for_transferring
    reason_1 = forms.CharField(widget=forms.Textarea, required=False)
    reason_2 = forms.CharField(widget=forms.Textarea, required=False)
    reason_3 = forms.CharField(widget=forms.Textarea, required=False)
    reason_4 = forms.CharField(widget=forms.Textarea, required=False)
    reason_5 = forms.CharField(widget=forms.Textarea, required=False)
    date_last_a = forms.CharField(required=False)
    place_last_a = forms.CharField(required=False)
    other_info = forms.CharField(widget=forms.Textarea, required=False)


class child_case_f(forms.ModelForm):
    class Meta:
        model = Child_Case_Data
        exclude = ('child',)


