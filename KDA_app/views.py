from wkhtmltopdf.views import PDFTemplateView

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.db.models import F

from .models import Person, Role, Hosted_Centres, Appointment, Availability, Slot, Child_Case_Data, \
    teacher_occupied_slots, Intervention, Assessment_psy, Pre_Evaluation, Skill_English_Pre, Skill_Arabic_Pre, \
    Evaluation_regular, Skill_English, Skill_Arabic, Arabic_Letter, Cognitive_assessment, Intervention_Cancelled, \
    All_Intervention, Test, Session, Homeworks
from django.contrib import messages
from .forms import login_form, register_form, register_centre_form, add_appointment_form, child_case_form, child_case_f
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.core import serializers

# Create your views here.
from .utils import render_to_pdf

current_time = timezone.now() + timezone.timedelta(hours=3)


# def home(request):
#     super = Person.objects.get(is_superuser=True)
#     if request.user.email != super.email:
#         return render(request, 'static_files/login.html')
#     else:
#         return render(request, 'static_files/index.html')
#
#
# def login(request):
#     email = request.POST.get('email')
#     password = request.POST.get('password')
#     super = Person.objects.get(is_superuser=True)
#     if email and password:
#         x = Person.objects.filter(email=email)
#         y = False
#         if x:
#             x = Person.objects.get(email=email)
#             y = x.check_password(password)
#         if y:
#             if x.email == super.email:
#                 return render(request, 'static_files/index.html')
#             else:
#                 messages.warning(request, 'Enter Correct Credentials')
#                 return redirect(login)
#         else:
#             messages.warning(request, 'Enter Correct Credentials')
#             return redirect(login)
#     return render(request, 'static_files/login.html')


def empty(request):
    return redirect(index)


def login(request):
    if request.method == "POST":
        lf = login_form(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data["username"]
            password = lf.cleaned_data["password"]
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if user.role:
                    if user.role.name == "Receptionist":
                        return redirect(receptionist_dashboard)
                else:
                    return redirect(index)
            elif Person.objects.filter(username=username).count() == 0:
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
            elif not Person.objects.get(username=username).check_password(password):
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
            else:
                messages.warning(request, message="Wrong Credentials, Check again")
                return redirect(login)
    else:
        lf = login_form()
    return render(request, 'static_files/login.html', {'form': lf})


@login_required(login_url='login')
def language_choose(request):
    return render(request, 'registration/language.html')


@login_required(login_url='login')
def index(request):
    if request.user.role.name == "Teacher":
        return redirect(todays_intervention)
    elif request.user.role.name == "Parent":
        return redirect(select_student, 'recep')
    else:
        return redirect(todays_appoint_list)


def register(request):
    if request.method == "POST":
        rf = register_form(request.POST, request.FILES)
        if rf.is_valid():
            first_name = rf.cleaned_data['first_name']
            last_name = rf.cleaned_data['last_name']
            username = rf.cleaned_data['username']
            gender = rf.cleaned_data['gender']
            dob = rf.cleaned_data['dob']
            profile_picture = rf.cleaned_data['profile_picture']
            # profile_picture = request.FILES['profile_picture']
            street = rf.cleaned_data['street']
            block = rf.cleaned_data['block']
            city = rf.cleaned_data['city']
            state = rf.cleaned_data['state']
            country = rf.cleaned_data['country']
            postal_code = rf.cleaned_data['postalcode']
            qualification = rf.cleaned_data['qualification']
            institution = rf.cleaned_data['institution']
            mobile = rf.cleaned_data['mobile']
            email = rf.cleaned_data['email']

            Person.objects.create(first_name=first_name, last_name=last_name, gender=gender, dob=dob,
                                  profile_pic=profile_picture, username=username, country=country, state=state,
                                  city=city,
                                  street=street, block=block, postal_code=postal_code, qualification=qualification,
                                  institute=institution, mobile_number=mobile, email=email)
            messages.success(request, message="Individual Registered, Waiting for Approval From Admin")
            return redirect(register)
        else:
            print(rf.errors)
            return HttpResponse(rf.errors)
    else:
        rf = register_form()
    return render(request, 'static_files/register.html', {'form': rf})


def register_centre(request):
    rf = ''
    if request.method == "POST":
        rf = register_centre_form(request.POST, request.FILES)
        if rf.is_valid():
            centre_name = rf.cleaned_data['centre_name']
            hc_logo = rf.cleaned_data['hc_logo']
            hc_document = rf.cleaned_data['hc_document']
            qualification = rf.cleaned_data['qualification']
            institution = rf.cleaned_data['institution']
            first_name = rf.cleaned_data['first_name']
            last_name = rf.cleaned_data['last_name']
            profile_picture = rf.cleaned_data['profile_picture']
            # profile_picture = request.FILES['profile_picture']
            street = rf.cleaned_data['street']
            block = rf.cleaned_data['block']
            city = rf.cleaned_data['city']
            state = rf.cleaned_data['state']
            country = rf.cleaned_data['country']
            postal_code = rf.cleaned_data['postalcode']
            spoc_mobile_number = rf.cleaned_data['spoc_mobile_number']
            spoc_email = rf.cleaned_data['spoc_email']
            spoc_extension = rf.cleaned_data['spoc_extension']
            spoc_office_number = rf.cleaned_data['spoc_office_number']
            centre_mobile_number_1 = rf.cleaned_data['centre_mobile_number_1']
            centre_mobile_number_2 = rf.cleaned_data['centre_mobile_number_2']
            centre_office_number = rf.cleaned_data['centre_office_number']
            centre_extension_number = rf.cleaned_data['centre_extension_number']
            centre_email = rf.cleaned_data['centre_email']
            centre_web_address = rf.cleaned_data['centre_web_address']

            Hosted_Centres.objects.create(centre_name=centre_name, hc_logo=hc_logo, hc_document=hc_document,
                                          qualification=qualification, institute=institution, spoc_f_name=first_name,
                                          spoc_l_name=last_name, spoc_profile_pic=profile_picture, country=country,
                                          state=state, city=city, street=street, block=block, postal_code=postal_code,
                                          spoc_email=spoc_email, spoc_mobile_number=spoc_mobile_number,
                                          spoc_extension_number=spoc_extension, spoc_office_number=spoc_office_number,
                                          centre_mobile_number_1=centre_mobile_number_1,
                                          centre_mobile_number_2=centre_mobile_number_2,
                                          centre_office_number=centre_office_number,
                                          centre_extension_number=centre_extension_number, centre_email=centre_email,
                                          centre_web_address=centre_web_address)
            messages.success(request, message="Centre Registered. Waiting For Approval From Admin!")
            return redirect(register_centre)
        else:
            print(rf.errors)
            return HttpResponse(rf.errors)
    else:
        rf = register_centre_form()
    return render(request, 'static_files/register_centre.html', {'form': rf})


@login_required(login_url='login')
def receptionist_dashboard(request):
    user = request.user
    user = Person.objects.get(id=user.id)
    return render(request, 'static_files/dashboard_receptionist.html', {'user': user})


@login_required(login_url='login')
def appointment_list(request):
    appoin_list = ''
    children = set()
    psychologists = set()
    if request.user.role.name == "Physiologist":
        appoin_list = Appointment.objects.filter(psychologist=request.user).order_by('appointment_date')
    elif request.user.role.name == "Receptionist":
        appoin_list = Appointment.objects.filter().order_by('appointment_date')
    if request.method == "POST":
        s_by_name = request.POST['s_by_name']
        p_by_name = ''
        if request.user.role.name == "Receptionist":
            p_by_name = request.POST['p_by_name']
        if s_by_name:
            appoin_list = appoin_list.filter(child__username=s_by_name)
        if p_by_name:
            appoin_list = appoin_list.filter(psychologist__username=p_by_name)
    else:
        for appoint in appoin_list:
            children.add(appoint.child)
            psychologists.add(appoint.psychologist)
    return render(request, 'static_files/appointment_list.html', {'objs': appoin_list, 'children': children,
                                                                  'psychologists': psychologists})


weekdays = {'0': 'm', '1': 'tu', '2': 'w', '3': 'th', '4': 'f', '5': 'sa',
            '6': 'su'}


@login_required(login_url='login')
def add_appointment(request):
    if request.method == "POST":
        af = add_appointment_form(request.POST)
        if af.is_valid():
            appointment_date = af.cleaned_data['appointment_date']
            if request.user.role.name == "Receptionist":
                psychologist_id = request.POST['psy']
            else:
                psychologist_id = request.user.id
            child_id = request.POST['child']

            if not psychologist_id or not child_id:
                messages.warning(request, message="Fill All fields Please")
                return redirect(add_appointment)

            psy = Person.objects.get(id=psychologist_id)
            child = Person.objects.get(id=child_id)

            d = appointment_date.split('/')
            datee = datetime.datetime(int(d[2]), int(d[1]), int(d[0]))
            if datee.date() < datetime.datetime.now().date():
                messages.warning(request, message="Add date Ahead of today")
                return redirect(add_appointment)
            if datee.date().weekday() == 4:
                messages.warning(request, message="Friday is OFF")
                return redirect(add_appointment)
            return redirect(check_slots, psy.id, child.id, datee.date())
        else:
            messages.warning(request, message=af.errors)
            return redirect(add_appointment)
    af = add_appointment_form()
    p = Person.objects.filter(role__name="Physiologist")
    students = Person.objects.filter(role__name="Student")
    return render(request, 'static_files/add_appointment.html', {'form': af, 'psys': p, 'students': students})


time_slots_r_p = {'08:00:00': '0', '10:00:00': '1', '12:00:00': '2', '14:00:00': '3', '16:00:00': '4',
                  '18:00:00': '5'}

time_slots_p = {'0': '08:00:00', '1': '10:00:00', '2': '12:00:00', '3': '14:00:00', '4': '16:00:00',
                '5': '18:00:00'}


@login_required(login_url='login')
def check_slots(request, id1, id2, date):
    da = date.split('-')
    daat = datetime.datetime(int(da[0]), int(da[1]), int(da[2])).date()
    weekday = daat.weekday()
    # delete_old_slots(current_time.date())
    psy = Person.objects.get(id=id1)
    child = Person.objects.get(id=id2)
    content = []
    content2 = []
    ava = Availability.objects.filter(psychologist=psy).first()

    if request.method == "POST":
        for n in range(6):
            if str(n) in request.POST:
                if weekday == 0:
                    s_time = time_slots_p[str(n + int((int(str(ava.m_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
                elif weekday == 1:
                    s_time = time_slots_p[str(n + int((int(str(ava.tu_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
                elif weekday == 2:
                    s_time = time_slots_p[str(n + int((int(str(ava.w_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
                elif weekday == 3:
                    s_time = time_slots_p[str(n + int((int(str(ava.th_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
                elif weekday == 5:
                    s_time = time_slots_p[str(n + int((int(str(ava.sa_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
                elif weekday == 6:
                    s_time = time_slots_p[str(n + int((int(str(ava.su_available_time_from).split(':')[0]) - 8) / 2))]
                    return redirect(confirm_appointment, id1, id2, date, s_time)
    else:
        if ava:
            if weekday == 0:
                content = {'s': range(int((int(str(ava.m_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.m_available_time_to).split(':')[0]) -
                                           int(str(ava.m_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.m_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.m_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
            elif weekday == 1:
                content = {'s': range(int((int(str(ava.tu_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.tu_available_time_to).split(':')[0]) -
                                           int(str(ava.tu_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.tu_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.tu_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
            elif weekday == 2:
                content = {'s': range(int((int(str(ava.w_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.w_available_time_to).split(':')[0]) -
                                           int(str(ava.w_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.w_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.w_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
            elif weekday == 3:
                content = {'s': range(int((int(str(ava.th_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.th_available_time_to).split(':')[0]) -
                                           int(str(ava.th_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.th_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.th_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
            elif weekday == 5:
                content = {'s': range(int((int(str(ava.sa_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.sa_available_time_to).split(':')[0]) -
                                           int(str(ava.sa_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.sa_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.sa_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
            elif weekday == 6:
                content = {'s': range(int((int(str(ava.su_available_time_from).split(':')[0]) - 8) / 2)),
                           'd': range(int((int(str(ava.su_available_time_to).split(':')[0]) -
                                           int(str(ava.su_available_time_from).split(':')[0])) / 2)),
                           'e': range(int((20 - int(str(ava.su_available_time_to).split(':')[0])) / 2))
                           }
                content2 = [
                    int(time_slots_r_p[str(x.appointment_s_time)]) - int((int(str(ava.su_available_time_from).split(
                        ':')[0]) - 8) / 2) for x in
                    Appointment.objects.filter(psychologist=psy, child=child, appointment_date=daat)]
        else:
            messages.warning(request, message='Please Set Availability for the Psychologist')
            return redirect(add_appointment)

        # slotss = Slot.objects.filter(psychologist_id=id1, day=date)
        # x = current_time + timezone.timedelta(hours=2)
        # two_hours = int(str(x.time()).split(':')[0])
        # if slotss:
        # slotss = Slot.objects.filter(psychologist_id=id1, day=date, available=True)
        # if str(current_time.date()) == str(date):
        #     for slot in slotss:
        #         slot_time = int(str(slot.s_time).split(':')[0])
        #         print(slot_time, two_hours)
        #         if slot_time < two_hours or two_hours == 0 or two_hours == 1:
        #             slotss = slotss.exclude(id=slot.id)
        # else:
        #     d = date.split('-')
        #     datee = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
        #     weekday = datee.date().weekday()
        #     create_slots(id1, weekday=weekday, day=date)
        #     slotss = Slot.objects.filter(psychologist_id=id1, day=date, available=True)
        #     if current_time.date() == date:
        #         for slot in slotss:
        #             slot_time = int(str(slot.s_time).split(':')[0])
        #             if slot_time < two_hours:
        #                 slotss = slotss.exclude(id=slot.id)

        return render(request, 'static_files/check_slots.html', {'psy': psy, 'date': daat, 'child': child,
                                                                 'true_date': date, 'content': content,
                                                                 'content2': content2, 'weekday': weekday})


def success(request):
    return render(request, 'static_files/success.html')


@login_required(login_url='login')
def search_psy(request):
    psys = ''
    if request.method == "POST":
        id = request.POST['search_by_id']
        name = request.POST['search_by_name']
        if id:
            psys = Person.objects.filter(role__name="Physiologist", id=id)
        elif name:
            name = name.split(" ")
            for n in name:
                psys = Person.objects.filter(role__name="Physiologist", first_name__icontains=n)
                if not psys:
                    psys = Person.objects.filter(role__name="Physiologist", last_name__icontains=n)
    else:
        psys = Person.objects.filter(role__name="Physiologist")
    return render(request, 'static_files/search_psy.html', {'psys': psys})


@login_required(login_url='login')
def availability(request, id):
    p = Person.objects.get(id=id)
    ava, created = Availability.objects.get_or_create(psychologist=p)
    return render(request, 'static_files/availability_psy.html', {'ava': ava, 'psy': p})


@login_required(login_url='login')
def availability_edit(request, id):
    dic = {}
    p = Person.objects.get(id=id)
    ava = Availability.objects.get(psychologist=p)
    dic['m_from'] = str(ava.m_available_time_from)
    dic['m_to'] = str(ava.m_available_time_to)
    dic['tu_from'] = str(ava.tu_available_time_from)
    dic['tu_to'] = str(ava.tu_available_time_to)
    dic['w_from'] = str(ava.w_available_time_from)
    dic['w_to'] = str(ava.w_available_time_to)
    dic['th_from'] = str(ava.th_available_time_from)
    dic['th_to'] = str(ava.th_available_time_to)
    # dic['f_from'] = str(ava.f_available_time_from)
    # dic['f_to'] = str(ava.f_available_time_to)
    dic['sa_from'] = str(ava.sa_available_time_from)
    dic['sa_to'] = str(ava.sa_available_time_to)
    dic['su_from'] = str(ava.su_available_time_from)
    dic['su_to'] = str(ava.su_available_time_to)

    if request.method == "POST":
        m_from = request.POST['1-stime']
        m_to = request.POST['1-ftime']
        tu_from = request.POST['2-stime']
        tu_to = request.POST['2-ftime']
        w_from = request.POST['3-stime']
        w_to = request.POST['3-ftime']
        th_from = request.POST['4-stime']
        th_to = request.POST['4-ftime']
        # f_from = request.POST['5-stime']
        # f_to = request.POST['5-ftime']
        sa_from = request.POST['6-stime']
        sa_to = request.POST['6-ftime']
        su_from = request.POST['7-stime']
        su_to = request.POST['7-ftime']

        if m_from: ava.m_available_time_from = m_from
        if m_to: ava.m_available_time_to = m_to
        if tu_from: ava.tu_available_time_from = tu_from
        if tu_to: ava.tu_available_time_to = tu_to
        if w_from: ava.w_available_time_from = w_from
        if w_to: ava.w_available_time_to = w_to
        if th_from: ava.th_available_time_from = th_from
        if th_to: ava.th_available_time_to = th_to
        # if f_from: ava.f_available_time_from = f_from
        # if f_to: ava.f_available_time_to = f_to
        if sa_from: ava.sa_available_time_from = sa_from
        if sa_to: ava.sa_available_time_to = sa_to
        if su_from: ava.su_available_time_from = su_from
        if su_to: ava.su_available_time_to = su_to
        ava.save()

        return redirect(availability, id)
    return render(request, 'static_files/availability_psy_edit.html', {'dic': dic, 'psy': p})


def create_slots(id, weekday, day):
    slots = []
    ava = Availability.objects.get(psychologist_id=id)
    f = f'{weekdays[str(weekday)]}_available_time_from'
    t = f'{weekdays[str(weekday)]}_available_time_to'
    from_time = getattr(ava, f)
    to_time = getattr(ava, t)
    r = to_time.hour - from_time.hour
    y = from_time.hour
    for x in range(int(r / 2)):
        if y < 10:
            if y + 2 < 10:
                slots.append(f'0{y}:00-0{y + 2}:00')
            else:
                slots.append(f'0{y}:00-{y + 2}:00')
        else:
            slots.append(f'{y}:00-{y + 2}:00')
        y += 2
    for slot in slots:
        Slot.objects.create(psychologist_id=id, day=day, s_time=slot.split('-')[0], e_time=slot.split('-')[1],
                            available=True)
    return '0'


def delete_old_slots(date):
    slots = Slot.objects.filter(day__lt=date)
    for slot in slots:
        slot.delete()
    # appoints = Appointment.objects.filter(appointment_date__lt=date)
    # for appoint in appoints:
    #     appoint.delete()


@login_required(login_url='login')
def confirm_appointment(request, id1, id2, date, time_s):
    child = Person.objects.get(id=id2)
    # children = Person.objects.filter(role__name="Student").exclude(id=id2)
    psy = Person.objects.get(id=id1)
    da = date.split('-')
    daat = datetime.datetime(int(da[0]), int(da[1]), int(da[2])).date()
    e_hour = int(time_s.split(':')[0]) + 2
    time_e = f'{e_hour}:00:00'
    if request.method == "POST":
        appoint = Appointment.objects.filter(child_id=id2, psychologist_id=id1,
                                             appointment_date__gte=current_time.date()).first()
        if not appoint:
            Appointment.objects.create(psychologist_id=id1, child_id=id2, appointment_date=daat,
                                       appointment_s_time=time_s,
                                       appointment_e_time=time_e, status='true')
            return redirect(appointment_list)
        else:
            appoint.appointment_date = daat
            appoint.appointment_s_time = time_s
            appoint.appointment_e_time = time_e
            appoint.save()
            return redirect(appointment_list)

    return render(request, 'static_files/confirm_appointment.html', {'child': child, 'psy': psy,
                                                                     'date': daat, 'time_s': time_s, 'time_e': time_e})


@login_required(login_url='login')
def delete_appointment(request, id):
    appoin = Appointment.objects.get(id=id)
    appoin.delete()
    return redirect(appointment_list)


@login_required(login_url='login')
def rescheudle(request, id):
    appoin = Appointment.objects.get(id=id)
    psy = Person.objects.filter(role__name="Physiologist").exclude(id=appoin.psychologist_id)
    if request.method == "POST":
        appointment_date = request.POST['appointment_date']
        psy_name = request.POST['psy']
        full_name_psy = psy_name.split(' ')
        psy = Person.objects.get(first_name=full_name_psy[0])

        if not appointment_date:
            messages.warning(request, message="Kindly Select the date")
            return redirect(rescheudle, id)

        d = appointment_date.split('/')
        datee = datetime.datetime(int(d[2]), int(d[1]), int(d[0]))
        if datee.date() < datetime.datetime.now().date():
            messages.warning(request, message="Add date Ahead of today")
            return redirect(rescheudle, id)
        if datee.date().weekday() == 4:
            messages.warning(request, message="Friday is OFF")
            return redirect(rescheudle, id)
        return redirect(check_slots, psy.id, appoin.child.id, datee.date())

    return render(request, 'static_files/reshedule.html', {'appointment': appoin, 'psy': psy})


def is_none(field):
    if field is None:
        return True
    else:
        return False


def format_date_model(date):
    splitted = date.split('/')
    return f'{splitted[2]}-{splitted[1]}-{splitted[0]}'


def format_date_html(date):
    splitted = str(date).split('-')
    return f'{splitted[2]}/{splitted[1]}/{splitted[0]}'


def child_case(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    count = Child_Case_Data.objects.filter(child_id=id).count()
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            civil_number = child_form.cleaned_data['civil_number']
            school_name = child_form.cleaned_data['school_name']
            dob = child_form.cleaned_data['dob']
            place_of_birth = child_form.cleaned_data['place_of_birth']
            nationality = child_form.cleaned_data['nationality']
            grade = request.POST['grade']
            gender = request.POST['gender']

            father_name = child_form.cleaned_data['father_name']
            age_f = child_form.cleaned_data['age_f']
            nationality_f = child_form.cleaned_data['nationality_f']
            education_level_f = child_form.cleaned_data['education_level_f']
            phone_f = child_form.cleaned_data['phone_f']
            current_occupation_f = child_form.cleaned_data['current_occupation_f']
            residence_address_f = child_form.cleaned_data['residence_address_f']
            email_f = request.POST['email_f']

            mother_name = child_form.cleaned_data['mother_name']
            age_m = child_form.cleaned_data['age_m']
            nationality_m = child_form.cleaned_data['nationality_m']
            phone_m = child_form.cleaned_data['phone_m']
            education_level_m = child_form.cleaned_data['education_level_m']
            current_occupation_m = child_form.cleaned_data['current_occupation_m']
            residence_address_m = child_form.cleaned_data['residence_address_m']
            email_m = request.POST['email_m']

            guardian_name = child_form.cleaned_data['guardian_name']
            education_level_g = child_form.cleaned_data['education_level_g']
            relation_to_child = child_form.cleaned_data['relation_to_child']
            phone_g = child_form.cleaned_data['phone_g']
            current_occupation_g = child_form.cleaned_data['current_occupation_g']
            residence_address_g = child_form.cleaned_data['residence_address_g']
            email_g = request.POST['email_g']

            relation_btw_parents = request.POST['relation_btw_parents']
            martial_status_parents = request.POST['martial_status_parents']
            parent_passed_away = request.POST['parent_passed_away']
            child_living_with = child_form.cleaned_data['child_living_with']
            father_married_before = request.POST['father_married_before']
            mother_married_before = request.POST['mother_married_before']
            when_was_married = request.POST['when_was_married']
            second_marriage = request.POST['second_marriage']
            nationality_second_marriage = child_form.cleaned_data['nationality_second_marriage']
            number_of_family_members = child_form.cleaned_data['number_of_family_members']
            number_of_brothers = child_form.cleaned_data['number_of_brothers']
            number_of_sisters = child_form.cleaned_data['number_of_sisters']
            number_of_brothers_from_father = child_form.cleaned_data['number_of_brothers_from_father']
            number_of_sisters_from_father = child_form.cleaned_data['number_of_sisters_from_father']
            number_of_brothers_from_mother = child_form.cleaned_data['number_of_brothers_from_mother']
            number_of_sisters_from_mother = child_form.cleaned_data['number_of_sisters_from_mother']
            order_sibling = child_form.cleaned_data['order_sibling']
            others_living_in_house = child_form.cleaned_data['others_living_in_house']
            lives_with = child_form.cleaned_data['lives_with']

            if count == 0:
                child = Person.objects.get(id=id)
                Child_Case_Data.objects.create(child=child, civil_number=civil_number, school_name=school_name,
                                               dob=format_date_model(dob), place_of_birth=place_of_birth,
                                               nationality=nationality, grade=grade, gender=gender, f_name=father_name,
                                               f_age=age_f, f_nationality=nationality_f, f_phone=phone_f,
                                               f_education_level=education_level_f, f_occupation=current_occupation_f,
                                               f_address=residence_address_f, f_email=email_f, m_name=mother_name,
                                               m_age=age_m, m_nationality=nationality_m, m_phone=phone_m,
                                               m_education_level=education_level_m, m_occupation=current_occupation_m,
                                               m_address=residence_address_m, m_email=email_m, g_name=guardian_name,
                                               g_education_level=education_level_g, g_relation_child=relation_to_child,
                                               g_phone=phone_g, g_occupation=current_occupation_g,
                                               g_address=residence_address_g, g_email=email_g,
                                               relation_btw_parents=relation_btw_parents,
                                               martial_status=martial_status_parents, passed_away=parent_passed_away,
                                               living_in_case=child_living_with, father_married=father_married_before,
                                               mother_married=mother_married_before, married_when=when_was_married,
                                               second_marriage=second_marriage,
                                               nationality_sec_m=nationality_second_marriage,
                                               number_of_fam=number_of_family_members,
                                               number_of_bros=number_of_brothers,
                                               number_of_sis=number_of_sisters,
                                               number_of_bros_f=number_of_brothers_from_father,
                                               number_of_sis_f=number_of_sisters_from_father,
                                               number_of_bros_m=number_of_brothers_from_mother,
                                               number_of_sis_m=number_of_sisters_from_mother,
                                               order_sib=order_sibling, other_people_house=others_living_in_house,
                                               lives_current=lives_with
                                               )
            else:
                cc = Child_Case_Data.objects.get(child_id=id)
                cc.civil_number = civil_number
                cc.school_name = school_name
                cc.dob = format_date_model(dob)
                cc.place_of_birth = place_of_birth
                cc.nationality = nationality
                cc.grade = grade
                cc.gender = gender
                cc.f_name = father_name
                cc.f_age = age_f
                cc.f_nationality = nationality_f
                cc.f_phone = phone_f
                cc.f_education_level = education_level_f
                cc.f_occupation = current_occupation_f
                cc.f_address = residence_address_f
                cc.f_email = email_f
                cc.m_name = mother_name
                cc.m_age = age_m
                cc.m_nationality = nationality_m
                cc.m_phone = phone_m
                cc.m_education_level = education_level_m
                cc.m_occupation = current_occupation_m
                cc.m_address = residence_address_m
                cc.m_email = email_f
                cc.g_name = guardian_name
                cc.g_education_level = education_level_g
                cc.g_relation_child = relation_to_child
                cc.g_phone = phone_g
                cc.g_occupation = current_occupation_g
                cc.g_address = residence_address_g
                cc.g_email = email_g
                cc.relation_btw_parents = relation_btw_parents
                cc.martial_status = martial_status_parents
                cc.passed_away = parent_passed_away
                cc.living_in_case = child_living_with
                cc.father_married = father_married_before
                cc.mother_married = mother_married_before
                cc.second_marriage = second_marriage
                cc.nationality_sec_m = nationality_second_marriage
                cc.number_of_fam = number_of_family_members
                cc.number_of_bros = number_of_brothers
                cc.number_of_sis = number_of_sisters
                cc.number_of_bros_f = number_of_brothers_from_father
                cc.number_of_sis_f = number_of_sisters_from_father
                cc.number_of_bros_m = number_of_brothers_from_mother
                cc.number_of_sis_m = number_of_sisters_from_mother
                cc.order_sib = order_sibling
                cc.other_people_house = others_living_in_house
                cc.lives_current = lives_with

                cc.save()

            if 'next' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)

        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        if count != 0:
            cc = Child_Case_Data.objects.get(child_id=id)
            cc.dob = format_date_html(cc.dob)

    return render(request, 'static_files/child-case.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_child_history(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            state_of_mind_preg = child_form.cleaned_data['state_of_mind_preg']
            age_during_preg = child_form.cleaned_data['age_during_preg']
            health_psy_preg = child_form.cleaned_data['health_psy_preg']
            preg_bleeding = request.POST['preg_bleeding']
            preg_poisoning = request.POST['preg_poisoning']
            preg_infection = request.POST['preg_infection']
            preg_accident = request.POST['preg_accident']
            kind_of_accident_preg = child_form.cleaned_data['kind_of_accident_preg']
            medicines_drugs_preg = child_form.cleaned_data['medicines_drugs_preg']
            prob_disease_preg = child_form.cleaned_data['prob_disease_preg']
            duration_preg = request.POST['duration_preg']
            preg_month = request.POST['preg_month']
            birth_type = request.POST['birth_type']
            umbilical_cord_neck = request.POST['umbilical_cord_neck']
            skin_yellow = request.POST['skin_yellow']
            skin_blue = request.POST['skin_blue']
            twin_triplet = request.POST['twin_triplet']
            oxygen_deficiency = request.POST['oxygen_deficiency']
            colic_cramps = request.POST['colic_cramps']
            dropsy_edema_hydrops = request.POST['dropsy_edema_hydrops']

            baby_weight_birth = child_form.cleaned_data['baby_weight_birth']
            prob_birth = child_form.cleaned_data['prob_birth']
            complications_birth = child_form.cleaned_data['complications_birth']

            health_psy_post_b = child_form.cleaned_data['health_psy_post_b']
            baby_incubator = request.POST['baby_incubator']
            period_incubator = child_form.cleaned_data['period_incubator']
            surgery_baby = child_form.cleaned_data['surgery_baby']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.state_of_m = state_of_mind_preg
            cc.p_m_age = age_during_preg
            cc.m_health = health_psy_preg
            cc.p_bleeding = preg_bleeding
            cc.p_poisoning = preg_poisoning
            cc.p_infection = preg_infection
            cc.p_accident = preg_accident
            cc.p_accident_detail = kind_of_accident_preg
            cc.p_medicines = medicines_drugs_preg
            cc.p_problems = prob_disease_preg
            cc.p_duration = duration_preg
            cc.p_month = preg_month
            cc.type_birth = birth_type
            cc.umbilical_cord = umbilical_cord_neck
            cc.skin_yellow = skin_yellow
            cc.skin_blue = skin_blue
            cc.twin_trip = twin_triplet
            cc.needed_oxy = oxygen_deficiency
            cc.colic_cramps = colic_cramps
            cc.dropsy = dropsy_edema_hydrops
            cc.baby_weight = baby_weight_birth
            cc.b_problems = prob_birth
            cc.b_complications = complications_birth
            cc.health_m_pb = health_psy_post_b
            cc.incubator = baby_incubator
            cc.incubator_period = period_incubator
            cc.b_surgery = surgery_baby

            cc.save()

            if 'prev' in request.POST:
                return redirect(child_case, id)
            elif 'next' in request.POST:
                return redirect(cc_condition, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_development_of_child.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_condition(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            extremely_high_temp_age = child_form.cleaned_data['extremely_high_temp_age']
            extremely_high_temp_dur = child_form.cleaned_data['extremely_high_temp_dur']
            ear_problems_age = child_form.cleaned_data['ear_problems_age']
            ear_problems_dur = child_form.cleaned_data['ear_problems_dur']
            vision_problems_age = child_form.cleaned_data['vision_problems_age']
            vision_problems_dur = child_form.cleaned_data['vision_problems_dur']
            juandice_age = child_form.cleaned_data['juandice_age']
            juandice_dur = child_form.cleaned_data['juandice_dur']
            asthma_age = child_form.cleaned_data['asthma_age']
            asthma_dur = child_form.cleaned_data['asthma_dur']
            allergy_age = child_form.cleaned_data['allergy_age']
            allergy_dur = child_form.cleaned_data['allergy_dur']
            poisoning_age = child_form.cleaned_data['poisoning_age']
            poisoning_dur = child_form.cleaned_data['poisoning_dur']
            surgical_age = child_form.cleaned_data['surgical_age']
            surgical_dur = child_form.cleaned_data['surgical_dur']
            surgery = child_form.cleaned_data['surgery']
            accident_age = child_form.cleaned_data['accident_age']
            accident_dur = child_form.cleaned_data['accident_dur']
            accident = child_form.cleaned_data['accident']
            not_mentioned_disease = child_form.cleaned_data['not_mentioned_disease']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.extremely_high_temp_age = extremely_high_temp_age
            cc.extremely_high_temp_dur = extremely_high_temp_dur
            cc.ear_problems_age = ear_problems_age
            cc.ear_problems_dur = ear_problems_dur
            cc.vision_problems_age = vision_problems_age
            cc.vision_problems_dur = vision_problems_dur
            cc.juandice_age = juandice_age
            cc.juandice_dur = juandice_dur
            cc.asthma_age = asthma_age
            cc.asthma_dur = asthma_dur
            cc.allergy_age = allergy_age
            cc.allergy_dur = allergy_dur
            cc.poisoning_age = poisoning_age
            cc.poisoning_dur = poisoning_dur
            cc.surgical_age = surgical_age
            cc.surgical_dur = surgical_dur
            cc.surgery = surgery
            cc.accident_age = accident_age
            cc.accident_dur = accident_dur
            cc.accident = accident
            cc.not_mentioned_disease = not_mentioned_disease

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_child_history, id)
            elif 'next' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_condition.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_stages_of_growth(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            breastfeeding = request.POST['breastfeeding']
            weaning_age = child_form.cleaned_data['weaning_age']
            age_tooth_start = child_form.cleaned_data['age_tooth_start']
            age_commune = child_form.cleaned_data['age_commune']
            age_simple_words = child_form.cleaned_data['age_simple_words']
            age_speech = child_form.cleaned_data['age_speech']
            age_sentence = child_form.cleaned_data['age_sentence']
            age_bottle_carry = child_form.cleaned_data['age_bottle_carry']
            age_love = child_form.cleaned_data['age_love']
            age_sat = child_form.cleaned_data['age_sat']
            age_stop = child_form.cleaned_data['age_stop']
            age_walk = child_form.cleaned_data['age_walk']
            age_wore_help = child_form.cleaned_data['age_wore_help']
            age_wore_self = child_form.cleaned_data['age_wore_self']
            age_shoes = child_form.cleaned_data['age_shoes']
            age_feed = child_form.cleaned_data['age_feed']
            age_urination = child_form.cleaned_data['age_urination']
            age_bathroom_train = child_form.cleaned_data['age_bathroom_train']
            visual_probs = request.POST['visual_probs']
            use_glasses = request.POST['use_glasses']
            age_glasses = child_form.cleaned_data['age_glasses']
            hearing_probs = request.POST['hearing_probs']
            hearing_aid = request.POST['hearing_aid']
            age_hearing_aid = child_form.cleaned_data['age_hearing_aid']
            speaking_difficulty = request.POST['speaking_difficulty']
            treated_speech_centres = request.POST['treated_speech_centres']
            age_speech_centre = child_form.cleaned_data['age_speech_centre']
            hand = request.POST['hand']
            leg = request.POST['leg']
            both_hand = request.POST['both_hand']
            stop_left_hand = request.POST['stop_left_hand']
            age_stop_left_hand = child_form.cleaned_data['age_stop_left_hand']
            involuntary_urination = request.POST['involuntary_urination']
            cause_involuntary_urination = request.POST['cause_involuntary_urination']
            age_involutary_urination = child_form.cleaned_data['age_involutary_urination']
            medicines_bool = request.POST['medicines_bool']
            medicine_name = child_form.cleaned_data['medicine_name']
            medicine_reason = child_form.cleaned_data['medicine_reason']
            appetite = child_form.cleaned_data['appetite']
            fav_food = child_form.cleaned_data['fav_food']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.breastfeeding = breastfeeding
            cc.age_weaning = weaning_age
            cc.age_teething = age_tooth_start
            cc.age_commune = age_commune
            cc.age_pronouncing = age_simple_words
            cc.age_speech = age_speech
            cc.age_full_sentence = age_sentence
            cc.age_bottle_milk = age_bottle_carry
            cc.age_love = age_love
            cc.age_sat_self = age_sat
            cc.age_stop_self = age_stop
            cc.age_walking = age_walk
            cc.age_wearing_help = age_wore_help
            cc.age_wearing_self = age_wore_self
            cc.age_shoes = age_shoes
            cc.age_feeding = age_feed
            cc.age_urination = age_urination
            cc.age_bathroom = age_bathroom_train
            cc.visual_prob = visual_probs
            cc.use_glasses = use_glasses
            cc.age_glasses = age_glasses
            cc.hearing_prob = hearing_probs
            cc.use_hearing_aid = hearing_aid
            cc.age_hearing_aid = age_hearing_aid
            cc.diff_speaking = speaking_difficulty
            cc.treated_speech = treated_speech_centres
            cc.age_treated_speech = age_speech_centre
            cc.hand_writing = hand
            cc.leg_kicking = leg
            cc.both_hands = both_hand
            cc.stop_left_hand = stop_left_hand
            cc.age_stop_left_hand = age_stop_left_hand
            cc.involuntary_urination = involuntary_urination
            cc.cause_involuntary_urination = cause_involuntary_urination
            cc.age_involuntary_urination = age_involutary_urination
            cc.medicines_bool = medicines_bool
            cc.medicines_name = medicine_name
            cc.medicine_reason = medicine_reason
            cc.eating_habits = appetite
            cc.fav_food = fav_food

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_condition, id)
            elif 'next' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_stages_of_growth.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_family_history(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            hyperinactivity = child_form.cleaned_data['hyperinactivity']
            reading = child_form.cleaned_data['reading']
            writing_dictating = child_form.cleaned_data['writing_dictating']
            calculating = child_form.cleaned_data['calculating']
            concentration = child_form.cleaned_data['concentration']
            pronouncing = child_form.cleaned_data['pronouncing']
            hearing = child_form.cleaned_data['hearing']
            visual = child_form.cleaned_data['visual']
            mobility = child_form.cleaned_data['mobility']
            intellectual = child_form.cleaned_data['intellectual']
            down_syndrome = child_form.cleaned_data['down_syndrome']
            autism = child_form.cleaned_data['autism']
            other_problems = child_form.cleaned_data['other_problems']
            child_hereditary = request.POST['child_hereditary']
            age_discovered = child_form.cleaned_data['age_discovered']
            effecting_child = child_form.cleaned_data['effecting_child']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.hyperinactivity = hyperinactivity
            cc.reading_diff = reading
            cc.writing_dictating_diff = writing_dictating
            cc.calculating_diff = calculating
            cc.concentration_diff = concentration
            cc.pronouncing_diff = pronouncing
            cc.impaired_hearing = hearing
            cc.visual_impairment = visual
            cc.impaired_mobility = mobility
            cc.intellectual_disability = intellectual
            cc.down_syn = down_syndrome
            cc.autism = autism
            cc.other_prob = other_problems
            cc.child_hereditary = child_hereditary
            cc.age_problem = age_discovered
            cc.prob_effect = effecting_child

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'next' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_family_history.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_social_development(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            friends = child_form.cleaned_data['friends']
            siblings = child_form.cleaned_data['siblings']
            parents = child_form.cleaned_data['parents']
            adults = child_form.cleaned_data['adults']
            maid = child_form.cleaned_data['maid']
            maid_rel_age = child_form.cleaned_data['maid_rel_age']
            fam_auth = child_form.cleaned_data['fam_auth']
            link_fam = child_form.cleaned_data['link_fam']
            punishment_reward = request.POST['punishment_reward']
            punisher = child_form.cleaned_data['punisher']
            punishment = request.POST['punishment']
            spending_time = child_form.cleaned_data['spending_time']
            hobbies_child = child_form.cleaned_data['hobbies_child']
            m_lang = child_form.cleaned_data['m_lang']
            o_lang = child_form.cleaned_data['o_lang']
            dialects = request.POST['dialects']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.friends = friends
            cc.siblings = siblings
            cc.parents = parents
            cc.adults = adults
            cc.maid = maid
            cc.age_maid = maid_rel_age
            cc.fam_auth = fam_auth
            cc.fam_close = link_fam
            cc.punishment_sys = punishment_reward
            cc.punisher = punisher
            cc.punishment = punishment
            cc.spent_time_in = spending_time
            cc.fav_hobby = hobbies_child
            cc.main_lang = m_lang
            cc.other_lang = o_lang
            cc.dilects = dialects

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_family_history, id)
            elif 'next' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)
    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc-social-development.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_child_beh(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            mental_illness = request.POST['mental_illness']
            mental_illnesses = child_form.cleaned_data['mental_illnesses']
            time_alone = request.POST['time_alone']
            specific_friend = request.POST['specific_friend']
            diff_friend = request.POST['diff_friend']
            quarrel_friends = request.POST['quarrel_friends']
            o_like_play = request.POST['o_like_play']
            o_avoid_play = request.POST['o_avoid_play']
            f_older = request.POST['f_older']
            f_younger = request.POST['f_younger']
            attention_seeker = request.POST['attention_seeker']
            confi_ability = request.POST['confi_ability']
            quite = request.POST['quite']
            impulsive = request.POST['impulsive']
            activity_normal = request.POST['activity_normal']
            cooperative = request.POST['cooperative']
            lies = request.POST['lies']
            moody = request.POST['moody']
            bored = request.POST['bored']
            comp_tasks = request.POST['comp_tasks']
            sad = request.POST['sad']
            cheerful = request.POST['cheerful']
            aggressive = request.POST['aggressive']
            avoid_competition = request.POST['avoid_competition']
            compete_others = request.POST['compete_others']
            lazy = request.POST['lazy']
            leadership = request.POST['leadership']
            autonomy = request.POST['autonomy']
            time_task = request.POST['time_task']
            anxious = request.POST['anxious']
            feel_afraid = request.POST['feel_afraid']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.mental_illness_bool = mental_illness
            cc.mental_illness = mental_illnesses
            cc.spends_time_alone = time_alone
            cc.no_friend = specific_friend
            cc.diff_friend = diff_friend
            cc.quarrels_friend = quarrel_friends
            cc.like_to_play = o_like_play
            cc.avoid_to_play = o_avoid_play
            cc.older_friend = f_older
            cc.younger_friend = f_younger
            cc.seeker_attention = attention_seeker
            cc.confidence_ability = confi_ability
            cc.quite = quite
            cc.impulsive = impulsive
            cc.normal_activity = activity_normal
            cc.cooperative = cooperative
            cc.lies = lies
            cc.moody = moody
            cc.gets_bored = bored
            cc.completes_tasks = comp_tasks
            cc.sad = sad
            cc.cheerful = cheerful
            cc.aggressive = aggressive
            cc.avoid_competition = avoid_competition
            cc.compete_others = compete_others
            cc.lazy = lazy
            cc.leadership = leadership
            cc.self_reliance = autonomy
            cc.long_time_tasks = time_task
            cc.anxious = anxious
            cc.afraid = feel_afraid

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_social_development, id)
            elif 'next' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)


    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_child_beh.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_school_history(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            s_name_1 = child_form.cleaned_data['s_name_1']
            s_enroll_1 = child_form.cleaned_data['s_enroll_1']
            s_beh_1 = child_form.cleaned_data['s_beh_1']
            s_name_2 = child_form.cleaned_data['s_name_2']
            s_enroll_2 = child_form.cleaned_data['s_enroll_2']
            s_beh_2 = child_form.cleaned_data['s_beh_2']
            s_name_3 = child_form.cleaned_data['s_name_3']
            s_enroll_3 = child_form.cleaned_data['s_enroll_3']
            s_beh_3 = child_form.cleaned_data['s_beh_3']

            first_stage = child_form.cleaned_data['first_stage']
            stages_failed = request.POST['stages_failed']
            failure_class = child_form.cleaned_data['failure_class']
            failure_subjs = child_form.cleaned_data['failure_subjs']
            private_tutors = request.POST['private_tutors']
            advantage = child_form.cleaned_data['advantage']
            diff_teaching = request.POST['diff_teaching']
            teachers_note = child_form.cleaned_data['teachers_note']
            supervision_teaching = request.POST['supervision_teaching']
            achievement = child_form.cleaned_data['achievement']
            motivation = child_form.cleaned_data['motivation']
            enthusiasm = child_form.cleaned_data['enthusiasm']
            time_punctuality = child_form.cleaned_data['time_punctuality']
            fav_articles = child_form.cleaned_data['fav_articles']
            least_fav_material = child_form.cleaned_data['least_fav_material']
            rel_teachers = child_form.cleaned_data['rel_teachers']
            desire_school = child_form.cleaned_data['desire_school']
            absent_reasons = child_form.cleaned_data['absent_reasons']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.school_name_1 = s_name_1
            if s_enroll_1:
                cc.enroll_date_1 = format_date_model(s_enroll_1)
            else:
                cc.enroll_date_1 = None
            cc.attitude_school_1 = s_beh_1
            cc.school_name_2 = s_name_2
            if s_enroll_2:
                cc.enroll_date_2 = format_date_model(s_enroll_2)
            else:
                cc.enroll_date_2 = None
            cc.attitude_school_2 = s_beh_2
            cc.school_name_3 = s_name_3
            if s_enroll_3:
                cc.enroll_date_3 = format_date_model(s_enroll_3)
            else:
                cc.enroll_date_3 = None
            cc.attitude_school_3 = s_beh_3
            cc.first_stage = first_stage
            cc.failed = stages_failed
            cc.failed_class = failure_class
            cc.failed_subjs = failure_subjs
            cc.private_tutors = private_tutors
            cc.take_advantage = advantage
            cc.difficult_teaching = diff_teaching
            cc.teachers_note = teachers_note
            cc.supervision = supervision_teaching
            cc.academic_achievement = achievement
            cc.motivation = motivation
            cc.enthusiasm = enthusiasm
            cc.time_punctual = time_punctuality
            cc.fav_articles = fav_articles
            cc.least_fav_material = least_fav_material
            cc.rel_teachers = rel_teachers
            cc.desire_school = desire_school
            cc.reason_absent = absent_reasons

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'next' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
        if cc.enroll_date_1:
            cc.enroll_date_1 = format_date_html(cc.enroll_date_1)
        else:
            cc.enroll_date_1 = ''
        if cc.enroll_date_2:
            cc.enroll_date_2 = format_date_html(cc.enroll_date_2)
        else:
            cc.enroll_date_2 = ''
        if cc.enroll_date_3:
            cc.enroll_date_3 = format_date_html(cc.enroll_date_3)
        else:
            cc.enroll_date_3 = ''
    return render(request, 'static_files/cc_school_history.html', {'obj': appoin, 'child': child, 'form': child_form,
                                                                   'cc': cc})


def cc_diff_info(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            reading_d = request.POST['reading_d']
            dictating_d = request.POST['dictating_d']
            writing_d = request.POST['writing_d']
            remembering_nearby_d = request.POST['remembering_nearby_d']
            recog_time = request.POST['recog_time']
            recog_days = request.POST['recog_days']
            recog_dir = request.POST['recog_dir']
            work_on_time = request.POST['work_on_time']
            focus_attention = request.POST['focus_attention']
            understanding = request.POST['understanding']
            remembering_remote_d = request.POST['remembering_remote_d']
            relationships = request.POST['relationships']
            expressing = request.POST['expressing']
            remembering_d = request.POST['remembering_d']
            blackboard = request.POST['blackboard']
            printed = request.POST['printed']
            flip = request.POST['flip']
            numbers_letters = request.POST['numbers_letters']
            verbal_ins = request.POST['verbal_ins']
            listening = request.POST['listening']
            repeat = request.POST['repeat']
            dis_numbers = request.POST['dis_numbers']
            multiplication = request.POST['multiplication']
            phone_numbers_m = request.POST['phone_numbers_m']
            counting = request.POST['counting']
            add_subt = request.POST['add_subt']
            maths_sym = request.POST['maths_sym']
            size = request.POST['size']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.reading = reading_d
            cc.dictating = dictating_d
            cc.writing = writing_d
            cc.remembering_nearby = remembering_nearby_d
            cc.recog_time = recog_time
            cc.recog_days = recog_days
            cc.recog_directions = recog_dir
            cc.completing_work = work_on_time
            cc.focus_attention = focus_attention
            cc.understanding = understanding
            cc.remembering_remote = remembering_remote_d
            cc.relationships = relationships
            cc.expressing_ideas = expressing
            cc.remembering_skills = remembering_d
            cc.moving_blackboard = blackboard
            cc.copying_printed = printed
            cc.flip_words = flip
            cc.confuses_numbers = numbers_letters
            cc.understanding_verbal = verbal_ins
            cc.learning_listening = listening
            cc.repeat_instruction = repeat
            cc.distinguish_numbers = dis_numbers
            cc.memorizing_multiplication = multiplication
            cc.memorizing_phone = phone_numbers_m
            cc.counting_up = counting
            cc.performing_add_subt = add_subt
            cc.understanding_mathematical = maths_sym
            cc.distinguish_size = size

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_school_history, id)
            elif 'next' in request.POST:
                return redirect(cc_other_info, id)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step10' in request.POST:
                return redirect(cc_other_info, id)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
    return render(request, 'static_files/cc_diff_info.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


def cc_other_info(request, id):
    appoin = Appointment.objects.filter(child_id=id).last()
    child = Person.objects.get(id=id)
    cc = ''
    if request.method == "POST":
        child_form = child_case_form(request.POST)
        if child_form.is_valid():
            # Get data
            follow_up = request.POST['follow_up']
            reason_1 = request.POST['reason_1']
            reason_2 = request.POST['reason_2']
            reason_3 = request.POST['reason_3']
            reason_4 = request.POST['reason_4']
            reason_5 = request.POST['reason_5']
            iq_test = request.POST['iq_test']
            date_last_a = child_form.cleaned_data['date_last_a']
            place_last_a = child_form.cleaned_data['place_last_a']
            other_info = request.POST['other_info']

            cc = Child_Case_Data.objects.get(child_id=id)
            cc.parents_cooperation = follow_up
            cc.reason_1 = reason_1
            cc.reason_2 = reason_2
            cc.reason_3 = reason_3
            cc.reason_4 = reason_4
            cc.reason_5 = reason_5
            cc.prev_iq = iq_test
            if date_last_a:
                cc.date_last_assessment = format_date_model(date_last_a)
            else:
                cc.date_last_assessment = None
            cc.place_last_assessment = place_last_a
            cc.other_info = other_info

            cc.save()

            if 'prev' in request.POST:
                return redirect(cc_diff_info, id)
            elif 'next' in request.POST:
                return redirect(appointment_list)
            elif 'step1' in request.POST:
                return redirect(child_case, id)
            elif 'step2' in request.POST:
                return redirect(cc_child_history, id)
            elif 'step3' in request.POST:
                return redirect(cc_condition, id)
            elif 'step4' in request.POST:
                return redirect(cc_stages_of_growth, id)
            elif 'step5' in request.POST:
                return redirect(cc_family_history, id)
            elif 'step6' in request.POST:
                return redirect(cc_social_development, id)
            elif 'step7' in request.POST:
                return redirect(cc_child_beh, id)
            elif 'step8' in request.POST:
                return redirect(cc_school_history, id)
            elif 'step9' in request.POST:
                return redirect(cc_diff_info, id)
        else:
            print(child_form.errors)

    else:
        child_form = child_case_form()
        cc = Child_Case_Data.objects.get(child_id=id)
        if cc.date_last_assessment:
            cc.date_last_assessment = format_date_html(cc.date_last_assessment)
        else:
            cc.date_last_assessment = ''
    return render(request, 'static_files/cc_other_info.html',
                  {'obj': appoin, 'child': child, 'form': child_form, 'cc': cc})


@login_required(login_url='login')
def send_link_form(request, id, language):
    child = Appointment.objects.get(id=id).child
    if child.email:
        form_link = f'http://40.89.138.111/ar/child-case-form/{child.id}/'
        print(language)
        if language == 'en':
            message = f"Welcome,\n To enter the data for the case form of {child.first_name} {child.parent.first_name} {child.last_name}, Please Click the following link:\n" + form_link + \
                      '\n\n With Regards \n Kuwait Dyslexia Association.'
        elif language == 'ar':
            message = f' مرحبا بكم \n لادخال بيانات استمارة الحالة {child.first_name} {child.parent.first_name} {child.last_name}, يرجى الضغط على الرابط التالي :\n' + form_link + '\nمع تحيات\n الجمعية الكويتية للدسلكسيا\n'
        else:
            message = ''
        send_mail('From KDA', message, "info@q8da.com", [child.email, 'portal@q8da.com'], fail_silently=False)
        # send_mail('From KDA', message, "info@q8da.com", ['hamza.zaid29@yahoo.com'], fail_silently=False)
        messages.success(request, message="Email sent.")
    else:
        messages.success(request, message="No Email Found.")

    return redirect(appointment_list)


@login_required(login_url='login')
def add_intervention(request, id):
    if request.method == "POST":
        if 'sub' in request.POST:
            teacher_username = request.POST['teacher']
            teacher_id = Person.objects.get(username=teacher_username).id
            student_id = id
            if not teacher_username:
                messages.warning(request, message='Kindly Fill the Fields before Proceeding')
                return redirect(add_intervention, id)
            return redirect(check_intervention, student_id, teacher_id)
        # return redirect(weekly_grid, student_username, teacher_username)
    else:
        student = Person.objects.get(id=id)
        subjs = []
        teachers = []
        intvs = Intervention.objects.filter(student=student)
        for intv in intvs:
            subjs.append(intv.teacher.subject_teaching)
            if intv.teacher not in teachers:
                teachers.append(intv.teacher)
        all_teachers = Person.objects.filter(role__name='Teacher')
        for t in all_teachers:
            if t.subject_teaching not in subjs:
                teachers.append(t)
        return render(request, 'static_files/add_intervention.html', {'student': student, 'teachers': teachers})


@login_required(login_url='login')
def check_intervention(request, student_id, teacher_id):
    intervention = Intervention.objects.filter(teacher_id=teacher_id,
                                               student_id=student_id).first()
    if intervention:
        back = False
        sessions = Session.objects.filter(intervention=intervention, is_active=True)
        sessions_count = sessions.count()
        if sessions_count >= 6:
            back = True
        return render(request, 'static_files/check_intervention.html',
                      {'intervention': intervention, 'sessions': sessions,
                       'sessions_count': sessions_count, 'back': back})
    else:
        student = Person.objects.get(id=student_id)
        teacher = Person.objects.get(id=teacher_id)
        return render(request, 'static_files/check_intervention.html', {'student': student, 'teacher': teacher})


@login_required(login_url='login')
def reschedule_session(request, id):
    if request.method == "POST":
        teacher_username = request.POST['teacher']
        teacher_id = Person.objects.get(username=teacher_username).id
        # student_username = request.POST['student']
        return redirect(weekly_grid, id, teacher_id)
    else:
        session = Session.objects.get(id=id)
        teachers = Person.objects.filter(role__name='Teacher',
                                         subject_teaching=session.intervention.teacher.subject_teaching)
    return render(request, 'static_files/add_intervention.html',
                  {'teachers': teachers, 'student': session.intervention.student.full_name,
                   'session': session})


@login_required(login_url='login')
def search_teacher(request):
    teachers = ''
    subjects = []
    if request.method == "POST":
        teachers = Person.objects.filter(role__name='Teacher')
        for teacher in teachers:
            subjects.append(teacher.subject_teaching)
        subj = request.POST['subject']
        name = request.POST['search_by_name']
        if subj:
            teachers = Person.objects.filter(role__name="Teacher", subject_teaching__iexact=subj)
        elif name:
            name = name.split(" ")
            for n in name:
                teachers = Person.objects.filter(role__name="Teacher", first_name__icontains=n)
                if not teachers:
                    teachers = Person.objects.filter(role__name="Teacher", last_name__icontains=n)
    else:
        teachers = Person.objects.filter(role__name='Teacher')
        for teacher in teachers:
            if teacher.subject_teaching not in subjects:
                subjects.append(teacher.subject_teaching)

    return render(request, 'static_files/search_teacher.html', {'teachers': teachers, 'subjects': subjects})


time_slots_r = {'0800-0830': '0', '0830-0900': '1', '0900-0930': '2', '0930-1000': '3', '1000-1030': '4',
                '1030-1100': '5', '1100-1130': '6', '1130-1200': '7', '1200-1230': '8', '1230-1300': '9',
                '1300-1330': '10', '1330-1400': '11', '1400-1430': '12', '1430-1500': '13', '1500-1530': '14',
                '1530-1600': '15', '1600-1630': '16', '1630-1700': '17', '1700-1730': '18', '1730-1800': '19',
                '1800-1830': '20', '1830-1900': '21', '1900-1930': '22', '1930-2000': '23'}


@login_required(login_url='login')
def weekly_grid(request, student_id, teacher_id):
    ava = Availability.objects.get(psychologist_id=teacher_id)
    if request.method == "POST":
        for x in range(24):
            if f'{x}-mon' in request.POST:
                a = (int(str(ava.m_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.m_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-m')
            elif f'{x}-tue' in request.POST:
                a = (int(str(ava.tu_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.tu_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-tu')
            elif f'{x}-wed' in request.POST:
                a = (int(str(ava.w_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.w_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-w')
            elif f'{x}-th' in request.POST:
                a = (int(str(ava.th_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.th_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-th')
            elif f'{x}-sat' in request.POST:
                a = (int(str(ava.sa_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.sa_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-sa')
            elif f'{x}-sun' in request.POST:
                a = (int(str(ava.su_available_time_from).split(':')[0]) - 8) * 2
                b = int((int(str(ava.su_available_time_from).split(':')[1])) / 30)
                start_time = a + b
                return redirect(confirm_slot, student_id, teacher_id, f'{x + start_time}-su')
    else:
        content = {'s_mon': range(((int(str(ava.m_available_time_from).split(':')[0]) - 8) * 2) +
                                  int((int(str(ava.m_available_time_from).split(':')[1])) / 30)),
                   'mon': range(((int(str(ava.m_available_time_to).split(':')[0]) -
                                  int(str(ava.m_available_time_from).split(':')[0])) * 2) +
                                int((int(str(ava.m_available_time_to).split(':')[1])) / 30) -
                                int((int(str(ava.m_available_time_from).split(':')[1])) / 30)),
                   'e_mon': range(((20 - int(str(ava.m_available_time_to).split(':')[0])) * 2) -
                                  int((int(str(ava.m_available_time_to).split(':')[1])) / 30)),
                   's_tue': range(((int(str(ava.tu_available_time_from).split(':')[0]) - 8) * 2) +
                                  int((int(str(ava.tu_available_time_from).split(':')[1])) / 30)),
                   'tue': range(((int(str(ava.tu_available_time_to).split(':')[0]) -
                                  int(str(ava.tu_available_time_from).split(':')[0])) * 2) +
                                int((int(str(ava.tu_available_time_to).split(':')[1])) / 30) -
                                int((int(str(ava.tu_available_time_from).split(':')[1])) / 30)),
                   'e_tue': range(((20 - int(str(ava.tu_available_time_to).split(':')[0])) * 2) -
                                  int((int(str(ava.tu_available_time_to).split(':')[1])) / 30)),
                   's_wed': range(((int(str(ava.w_available_time_from).split(':')[0]) - 8) * 2) +
                                  int((int(str(ava.w_available_time_from).split(':')[1])) / 30)),
                   'wed': range(((int(str(ava.w_available_time_to).split(':')[0]) -
                                  int(str(ava.w_available_time_from).split(':')[0])) * 2) +
                                int((int(str(ava.w_available_time_to).split(':')[1])) / 30) -
                                int((int(str(ava.w_available_time_from).split(':')[1])) / 30)),
                   'e_wed': range(((20 - int(str(ava.w_available_time_to).split(':')[0])) * 2) -
                                  int((int(str(ava.w_available_time_to).split(':')[1])) / 30)),
                   's_th': range(((int(str(ava.th_available_time_from).split(':')[0]) - 8) * 2) +
                                 int((int(str(ava.th_available_time_from).split(':')[1])) / 30)),
                   'th': range(((int(str(ava.th_available_time_to).split(':')[0]) -
                                 int(str(ava.th_available_time_from).split(':')[0])) * 2) +
                               int((int(str(ava.th_available_time_to).split(':')[1])) / 30) -
                               int((int(str(ava.th_available_time_from).split(':')[1])) / 30)),
                   'e_th': range(((20 - int(str(ava.th_available_time_to).split(':')[0])) * 2) -
                                 int((int(str(ava.th_available_time_to).split(':')[1])) / 30)),
                   's_sat': range(((int(str(ava.sa_available_time_from).split(':')[0]) - 8) * 2) +
                                  int((int(str(ava.sa_available_time_from).split(':')[1])) / 30)),
                   'sat': range(((int(str(ava.sa_available_time_to).split(':')[0]) -
                                  int(str(ava.sa_available_time_from).split(':')[0])) * 2) +
                                int((int(str(ava.sa_available_time_to).split(':')[1])) / 30) -
                                int((int(str(ava.sa_available_time_from).split(':')[1])) / 30)),
                   'e_sat': range(((20 - int(str(ava.sa_available_time_to).split(':')[0])) * 2) -
                                  int((int(str(ava.sa_available_time_to).split(':')[1])) / 30)),
                   's_sun': range(((int(str(ava.su_available_time_from).split(':')[0]) - 8) * 2) +
                                  int((int(str(ava.su_available_time_from).split(':')[1])) / 30)),
                   'sun': range(((int(str(ava.su_available_time_to).split(':')[0]) -
                                  int(str(ava.su_available_time_from).split(':')[0])) * 2) +
                                int((int(str(ava.su_available_time_to).split(':')[1])) / 30) -
                                int((int(str(ava.su_available_time_from).split(':')[1])) / 30)),
                   'e_sun': range(((20 - int(str(ava.su_available_time_to).split(':')[0])) * 2) -
                                  int((int(str(ava.su_available_time_to).split(':')[1])) / 30))}

        intv_m = [int(time_slots_r[x.time]) - (((int(str(ava.m_available_time_from).split(':')[0]) - 8) * 2) +
                                               int((int(str(ava.m_available_time_from).split(':')[1])) / 30)) for x in
                  Session.objects.filter(intervention__teacher_id=teacher_id, day="Monday",
                                         intervention__status="Active", is_active=True)]
        intv_tu = [int(time_slots_r[x.time]) - (((int(str(ava.tu_available_time_from).split(':')[0]) - 8) * 2) +
                                                int((int(str(ava.tu_available_time_from).split(':')[1])) / 30)) for x in
                   Session.objects.filter(intervention__teacher_id=teacher_id, day="Tuesday",
                                          intervention__status="Active", is_active=True)]
        intv_w = [int(time_slots_r[x.time]) - (((int(str(ava.w_available_time_from).split(':')[0]) - 8) * 2) +
                                               int((int(str(ava.w_available_time_from).split(':')[1])) / 30)) for x in
                  Session.objects.filter(intervention__teacher_id=teacher_id, day="Wednesday",
                                         intervention__status="Active", is_active=True)]
        intv_th = [int(time_slots_r[x.time]) - (((int(str(ava.th_available_time_from).split(':')[0]) - 8) * 2) +
                                                int((int(str(ava.th_available_time_from).split(':')[1])) / 30)) for x in
                   Session.objects.filter(intervention__teacher_id=teacher_id, day="Thursday",
                                          intervention__status="Active", is_active=True)]
        intv_sa = [int(time_slots_r[x.time]) - (((int(str(ava.sa_available_time_from).split(':')[0]) - 8) * 2) +
                                                int((int(str(ava.sa_available_time_from).split(':')[1])) / 30)) for x in
                   Session.objects.filter(intervention__teacher_id=teacher_id, day="Saturday",
                                          intervention__status="Active", is_active=True)]
        intv_su = [int(time_slots_r[x.time]) - (((int(str(ava.su_available_time_from).split(':')[0]) - 8) * 2) +
                                                int((int(str(ava.su_available_time_from).split(':')[1])) / 30)) for x in
                   Session.objects.filter(intervention__teacher_id=teacher_id, day="Sunday",
                                          intervention__status="Active", is_active=True)]

        content2 = {'mon': intv_m, 'tue': intv_tu, 'wed': intv_w,
                    'th': intv_th, 'sat': intv_sa, 'sun': intv_su, 'ava': ava}
        return render(request, 'static_files/weekly_grid.html', {'content': content, 'content2': content2})


week = {'m': 'Monday', 'tu': 'Tuesday', 'w': 'Wednesday', 'th': 'Thursday', 'sa': 'Saturday',
        'su': 'Sunday'}
time_slots = {'0': '0800-0830', '1': '0830-0900', '2': '0900-0930', '3': '0930-1000', '4': '1000-1030',
              '5': '1030-1100', '6': '1100-1130', '7': '1130-1200', '8': '1200-1230', '9': '1230-1300',
              '10': '1300-1330', '11': '1330-1400', '12': '1400-1430', '13': '1430-1500', '14': '1500-1530',
              '15': '1530-1600', '16': '1600-1630', '17': '1630-1700', '18': '1700-1730', '19': '1730-1800',
              '20': '1800-1830', '21': '1830-1900', '22': '1900-1930', '23': '1930-2000'}


@login_required(login_url='login')
def confirm_slot(request, student_id, teacher_id, slot):
    teacher = Person.objects.get(id=teacher_id)
    stu = Person.objects.filter(id=student_id).first()
    session = None
    if not stu:
        session = Session.objects.get(id=student_id)
        stu = session.intervention.student
    slot1 = slot.split('-')
    start_date = ''
    if request.method == "POST":
        total_sessions = request.POST['total_sessions']
        intervention = Intervention.objects.filter(teacher=teacher, student=stu).first()
        if intervention:
            if not session:
                Session.objects.create(intervention=intervention, day=week[slot1[1]],
                                       time=f'{time_slots[slot1[0]]}')
            else:
                session.day = week[slot1[1]]
                session.time = f'{time_slots[slot1[0]]}'
                session.save()
            intervention.total_sessions = total_sessions
            intervention.save()
        else:
            # if Intervention.objects.filter(student=student, teacher=teacher).count() == 0:
            start_date = request.POST['start_date']
            s = start_date.split('/')
            st = datetime.date(int(s[2]), int(s[1]), int(s[0]))
            if daysname[str(st.weekday())] != week[slot1[1]] or st < current_time.date():
                messages.warning(request, message=f"Enter Any Future date of {week[slot1[1]]}")
                return redirect(confirm_slot, student_id, teacher_id, slot)
            # diff = current_time.date() - st
            # c_weeks = int(int(diff.days) / 7) + 1
            intervention = Intervention.objects.create(teacher=teacher, student=stu,
                                                       status="Active", start_date=st, total_sessions=total_sessions)
            session = Session.objects.create(intervention=intervention, day=week[slot1[1]],
                                             time=f'{time_slots[slot1[0]]}')
        # x = st
        # for c in range(c_weeks):
        #     All_Intervention.objects.create(intervention=intervention, date=x)
        #     x = x + datetime.timedelta(days=7)
        return redirect(search_intervention)
        # else:
        #     intervention = Intervention.objects.get(student=student, teacher=teacher)
        #     intervention.teacher = teacher
        #     intervention.day = week[slot1[1]]
        #     intervention.time = f'{time_slots[slot1[0]]}'
        #     intervention.save()
        #     return redirect(search_intervention)
        # return redirect(confirm_slot, student.username, username, slot)
    else:
        already = False
        total_sessions = None
        weekday = week[slot1[1]]
        timeslot = f'{time_slots[slot1[0]]}'
        students = Person.objects.filter(role__name="Student")
        intervention = Intervention.objects.filter(teacher=teacher, student=stu).first()
        if intervention:
            already = True
            start_date = intervention.start_date
            total_sessions = intervention.total_sessions
        return render(request, 'static_files/confirm_slot_teacher.html', {'weekday': weekday, 'time_slot': timeslot,
                                                                          'students': students, 'teacher': teacher,
                                                                          'stu': stu, 'start_date': start_date,
                                                                          'already': already,
                                                                          'total_sessions': total_sessions})


@login_required(login_url='login')
def search_intervention(request):
    if request.user.role.name == 'Receptionist':
        interventions = Intervention.objects.filter(status='Active').order_by('start_date')
    else:
        interventions = Intervention.objects.filter(teacher=request.user, status="Active").order_by('start_date')
    if request.method == "POST":
        sname = request.POST['search_by_sname']
        if request.user.role.name == 'Receptionist':
            tname = request.POST['search_by_tname']
            subj = request.POST['search_by_s']
        else:
            tname = ''
            subj = ''
        if subj:
            interventions = interventions.filter(teacher__subject_teaching=subj)
        if sname:
            interventions = interventions.filter(student__username=sname)
        if tname:
            interventions = interventions.filter(teacher__username=sname)

    all = []
    teachers = set()
    students = set()
    for intv in interventions:
        teachers.add(intv.teacher)
        students.add(intv.student)
        all.append(
            {'teacher': intv.teacher, 'student': intv.student, 'total_sessions': intv.total_sessions, 'id': intv.id,
             'start_date': intv.start_date,
             'sessions': [x for x in Session.objects.filter(intervention=intv, is_active=True)],
             'count': Session.objects.filter(intervention=intv, is_active=True).count(),
             'conducted': All_Intervention.objects.filter(session__intervention=intv,
                                                          status='attended').count()})
    subjs = {x.subject_teaching for x in teachers}
    return render(request, 'static_files/search_intervention.html', {'interventions': all, 'teachers': teachers,
                                                                     'students': students, 'subjs': subjs})


daysname_reverse = {'Monday': '0', 'Tuesday': '1', 'Wednesday': '2', 'Thursday': '3', 'Friday': '4', 'Saturday': '5',
                    'Sunday': '6'}


@login_required(login_url='login')
def detail_intervention(request, id):
    intv = Intervention.objects.get(id=id)
    start_date = intv.start_date
    week_day_number_s = intv.start_date.weekday()
    difference_week_number = max(int(week_day_number_s) - int(daysname_reverse[intv.day]),
                                 int(daysname_reverse[intv.day]) - int(week_day_number_s))
    start_date = start_date + timezone.timedelta(difference_week_number)
    dates = [format_date_html(start_date)]
    difference_weeks = int((int((timezone.now().date() - intv.start_date).days)) / 7)
    for x in range(difference_weeks):
        start_date = start_date + timezone.timedelta(days=7)
        dates.append(format_date_html(start_date))
    return render(request, 'static_files/detail_intervention.html', {'intervention': intv, 'dates': dates})


@login_required(login_url='login')
def delete_intervention(request, id):
    intv = Intervention.objects.get(id=id)
    intv.delete()

    return redirect(search_intervention)


@login_required(login_url='login')
def status_intervention(request, id):
    intv = Intervention.objects.get(id=id)
    intv.status = "Closed"
    intv.save()

    return redirect(search_intervention)


@login_required(login_url='login')
def search_assessment(request):
    if request.method == "POST":
        child_id = Person.objects.get(id=request.POST['child']).id
        if request.user.role.name == 'Receptionist':
            psy_id = Person.objects.get(username=request.POST['psy']).id
        else:
            psy_id = request.user.id
        return redirect(assess_tests, child_id, psy_id)
    else:
        children = Person.objects.filter(role__name="Student")
        psys = Person.objects.filter(role__name="Physiologist")
        return render(request, 'static_files/assessment_search.html', {'children': children, 'psys': psys})


@login_required(login_url='login')
def assess_tests(request, id1, id2):
    child = Person.objects.get(id=id1)
    psy = Person.objects.get(id=id2)
    appointment = Appointment.objects.filter(child=child, psychologist=psy).last()
    if not appointment:
        messages.warning(request, message='There is no such appointment for the given child and psychologist!')
        return redirect(search_assessment)
    content = ''
    cog = ''
    if request.method == "POST":
        test = request.POST['test']
        if test == 'iq':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='iq').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='iq')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test, 'subtests': ['IQ'], 'list_subs': list_subs}
        elif test == 'acops':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='acops').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='acops')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test,
                       'subtests': ['Rabbits', 'Zoid Friends', 'Zoid Letter Names', 'Zoid Letters',
                                    'Wock', 'Ryhms', 'Races', 'Toybox'], 'list_subs': list_subs}
        elif test == 'junior':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='junior').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='junior')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test, 'subtests': ['Spelling', 'Reading', 'Single Word Reading', 'Mobile',
                                                  'Funny Words', 'Segment', 'Cave'], 'list_subs': list_subs}
        elif test == 'secondary':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='secondary').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='secondary')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test, 'subtests': ['Spelling', 'Reading', 'Single Word Reading', 'Mobile',
                                                  'Funny Words', 'Segment', 'Cave'], 'list_subs': list_subs}
        elif test == 'standford':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='standford').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='standford')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test, 'subtests': ['Stanford'], 'list_subs': list_subs}
        elif test == 'weksler':
            count = Assessment_psy.objects.filter(appointment=appointment, test_name='weksler').count()
            list_subs = ''
            if count != 0:
                assess = Assessment_psy.objects.filter(appointment=appointment, test_name='weksler')
                list_subs = [x.sub_test_name for x in assess]
            content = {'test': test, 'subtests': ['Vocabulary IQ', 'Practical IQ', 'Total IQ'],
                       'list_subs': list_subs}
        count = Cognitive_assessment.objects.filter(appointment=appointment, test_name=test).count()
        if count != 0:
            cog = Cognitive_assessment.objects.get(appointment=appointment, test_name=test)
            cog.cognitive_date = format_date_html(cog.cognitive_date)
        if 'cognitive' in request.POST:
            if request.POST['cognitive_date']:
                if count == 0:
                    cog = Cognitive_assessment.objects.create(appointment=appointment, test_name=test,
                                                              cognitive_date=format_date_model(
                                                                  request.POST['cognitive_date']),
                                                              cognitive_result=request.POST['cognitive_result'],
                                                              recommendations=request.POST['recommendations'],
                                                              notice=request.POST['notice'])
                    cog.cognitive_date = format_date_html(cog.cognitive_date)
                else:
                    cog = Cognitive_assessment.objects.get(appointment=appointment, test_name=test)
                    cog.cognitive_date = format_date_model(request.POST['cognitive_date'])
                    cog.cognitive_result = request.POST['cognitive_result']
                    cog.recommendations = request.POST['recommendations']
                    cog.notice = request.POST['notice']
                    cog.save()
                    cog.cognitive_date = format_date_html(cog.cognitive_date)
        # appoints = Appointment.objects.filter(child=child, psychologist=psy, appointment_date__=)
    appoints = ''
    return render(request, 'static_files/assess_tests.html',
                  {'child': child, 'content': content, 'cog': cog, 'psy': psy, 'appoints': appoints})


test_dict = {'iq': 'IQ', 'acops': 'ACOPS', 'junior': 'Junior', 'secondary': 'Secondary', 'standford': 'Standford',
             'weksler': 'Weksler'}


@login_required(login_url='login')
def assessment(request, id1, id2, test, subtest):
    appointment = Appointment.objects.filter(child_id=id1, psychologist_id=id2).last()
    assess = ''
    count = Assessment_psy.objects.filter(appointment=appointment, test_name=test,
                                          sub_test_name=subtest).count()
    if Cognitive_assessment.objects.filter(appointment=appointment, test_name=test).count() != 0:
        cog = Cognitive_assessment.objects.get(appointment=appointment, test_name=test)
    else:
        cog = ''
    if request.method == "POST":
        if count == 0:
            if test == "weksler":
                assess = Assessment_psy.objects.create(appointment=appointment, test_name=test,
                                                       sub_test_name=subtest, sub_score_float=request.POST['sub_score'],
                                                       sub_percentage=request.POST['sub_percent'],
                                                       test_date=format_date_model(request.POST['test_date']))
            elif test == 'junior' or test == 'secondary' or test == 'acops':
                assess = Assessment_psy.objects.create(appointment=appointment, test_name=test,
                                                       sub_test_name=subtest, sub_score=request.POST['sub_score'],
                                                       sub_time=request.POST['sub_time'],
                                                       sub_grade=request.POST['sub_grade'],
                                                       test_date=format_date_model(request.POST['test_date']))
            else:
                assess = Assessment_psy.objects.create(appointment=appointment, test_name=test,
                                                       sub_test_name=subtest, sub_score=request.POST['sub_score'],
                                                       sub_time=request.POST['sub_time'],
                                                       sub_grade=request.POST['sub_grade'],
                                                       test_date=format_date_model(request.POST['test_date']), )
            if cog:
                assess.cognitive = cog
        else:
            assess = Assessment_psy.objects.get(appointment=appointment, test_name=test,
                                                sub_test_name=subtest)
            if test == "weksler":
                assess.sub_score_float = request.POST['sub_score']
                assess.sub_percentage = request.POST['sub_percent']
                assess.test_date = format_date_model(request.POST['test_date'])
            elif test == 'junior' or test == 'secondary' or test == 'acops':
                assess.sub_score = request.POST['sub_score']
                assess.sub_time = request.POST['sub_time']
                assess.sub_grade = request.POST['sub_grade']
                assess.test_date = format_date_model(request.POST['test_date'])
            else:
                assess.sub_score = request.POST['sub_score']
                assess.sub_time = request.POST['sub_time']
                assess.sub_grade = request.POST['sub_grade']
                assess.test_date = format_date_model(request.POST['test_date'])
            if cog:
                assess.cognitive = cog
            assess.save()
        return redirect(assess_tests, id1, id2)
    else:
        child = Person.objects.get(id=id1)
        if count != 0:
            assess = Assessment_psy.objects.get(appointment=appointment, test_name=test,
                                                sub_test_name=subtest)
            assess.test_date = format_date_html(assess.test_date)
            assess.sub_time = str(assess.sub_time)
            assess.sub_score = str(assess.sub_score)
            # assess.cognitive_date = format_date_html(assess.cognitive_date)
    return render(request, 'static_files/assessment.html', {'child': child, 'assess': assess,
                                                            'Test': test_dict[test], 'subtest': subtest,
                                                            'number': range(21)})


@login_required(login_url='login')
def search_teacher_pre(request):
    if request.method == "POST":
        t_username = request.POST['teacher']
        teacher_id = Person.objects.get(username=t_username).id
        return redirect(pre_evaluation_search, teacher_id)
    teachers = Person.objects.filter(role__name="Teacher")
    return render(request, 'static_files/select_teacher_assess.html', {'teachers': teachers})


@login_required(login_url='login')
def pre_evaluation_search(request, teacher_id):
    teacher = Person.objects.get(id=teacher_id)
    # if request.method == "POST":
    #     # student = Person.objects.get(username=request.POST['student'])
    #     for stu in Person.objects.filter(role__name="Student"):
    #         if stu.username in request.POST:
    #             if teacher.subject_teaching == "English":
    #                 return redirect(pre_evaluation, t_username, stu.id)
    #             elif teacher.subject_teaching == "Arabic":
    #                 return redirect(pre_evaluation_arabic, t_username, stu.id)
    intvs = Intervention.objects.filter(teacher_id=teacher_id)
    students = []
    pre_eva_counts = []
    for intv in intvs:
        students.append(Person.objects.get(id=intv.student.id))
        # pre_eva_counts.update({f'{intv.student.id}': Pre_Evaluation.objects.filter(teacher_id=7, student_id=intv.student.id).count()})
        if Pre_Evaluation.objects.filter(intervention=intv).count() != 0:
            pre_eva_counts.append(intv.student.id)
    return render(request, 'static_files/pre_eva_search.html', {'students': students, 'pre_eva_counts': pre_eva_counts,
                                                                'teacher': teacher, 'intvs': intvs})


@login_required(login_url='login')
def pre_evaluation(request, id):
    intervention = Intervention.objects.get(id=id)
    skill_english = ''
    count = Pre_Evaluation.objects.filter(intervention=intervention).count()
    if request.method == "POST":
        reading = request.POST['reading']
        writing = request.POST['writing']
        if count == 0:
            obj = Pre_Evaluation.objects.create(intervention=intervention)
            Skill_English_Pre.objects.create(pre_eva=obj, one=reading, two=writing)
        else:
            pre_eva = Pre_Evaluation.objects.get(intervention=intervention)
            skill_english = Skill_English_Pre.objects.get(pre_eva=pre_eva)
            skill_english.one = reading
            skill_english.two = writing
            skill_english.save()

        return redirect(pre_evaluation_search, intervention.teacher.id)
    else:
        if count != 0:
            pre_eva = Pre_Evaluation.objects.get(intervention=intervention)
            skill_english = Skill_English_Pre.objects.get(pre_eva=pre_eva)
        return render(request, 'static_files/pre_evaluation.html',
                      {'intervention': intervention, 'skill_english': skill_english,
                       'subj': 'English'})


@login_required(login_url='login')
def pre_evaluation_arabic(request, id):
    intervention = Intervention.objects.get(id=id)
    skill_arabic = ''
    count = Pre_Evaluation.objects.filter(intervention=intervention).count()
    if request.method == "POST":
        one = request.POST['one']
        two = request.POST['two']
        three = request.POST['three']
        four = request.POST['four']
        five = request.POST['five']
        six = request.POST['six']
        seven = request.POST['seven']
        eight = request.POST['eight']
        if count == 0:
            obj = Pre_Evaluation.objects.create(intervention=intervention)
            Skill_Arabic_Pre.objects.create(pre_eva=obj, one=one, two=two, three=three, four=four, five=five, six=six,
                                            seven=seven, eight=eight)
        else:
            pre_eva = Pre_Evaluation.objects.get(intervention=intervention)
            skill_arabic = Skill_Arabic_Pre.objects.get(pre_eva=pre_eva)
            skill_arabic.one = one
            skill_arabic.two = two
            skill_arabic.three = three
            skill_arabic.four = four
            skill_arabic.five = five
            skill_arabic.six = six
            skill_arabic.seven = seven
            skill_arabic.eight = eight
            skill_arabic.save()

        return redirect(pre_evaluation_search, intervention.teacher.id)
    else:
        if count != 0:
            pre_eva = Pre_Evaluation.objects.get(intervention=intervention)
            skill_arabic = Skill_Arabic_Pre.objects.get(pre_eva=pre_eva)
        return render(request, 'static_files/pre_evaluation.html',
                      {'intervention': intervention, 'skill_arabic': skill_arabic,
                       'subj': 'Arabic'})


daysname = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday', '4': 'Friday', '5': 'Saturday',
            '6': 'Sunday'}


@login_required(login_url='login')
def select_teacher_assess(request):
    if request.method == "POST":
        teacher = request.POST['teacher']
        teacher_id = Person.objects.get(username=teacher).id
        # teacher = Person.objects.get(username=teacher)
        return redirect(session_evaluation_search, teacher_id)
    else:
        teachers = Person.objects.filter(role__name="Teacher")
        return render(request, 'static_files/select_teacher_assess.html', {'teachers': teachers})


@login_required(login_url='login')
def session_evaluation_search(request, teacher_id):
    intvs = Intervention.objects.filter(teacher_id=teacher_id, status='Active')
    students = []
    for intv in intvs:
        students.append(Person.objects.get(id=intv.student.id))
    if request.method == "POST":
        student = int(request.POST['student'])
        intv = intvs.get(student_id=student)
        all_intv = All_Intervention.objects.filter(session__intervention=intv, status='attended')
        if 'next' in request.POST:
            return redirect(session_evaluation, request.POST['date'])
        return render(request, 'static_files/session_evaluation_search.html', {'students': students, 'stu': student,
                                                                               'all_intvs': all_intv, 'display': True})
    else:
        return render(request, 'static_files/session_evaluation_search.html', {'students': students})


@login_required(login_url='login')
def session_evaluation(request, id):
    a_intervention = All_Intervention.objects.get(id=id)
    intervention = Intervention.objects.get(session__all_intv=a_intervention)

    if a_intervention.session.intervention.teacher.subject_teaching == "English":
        skills_english_objs = Skill_English.objects.filter(a_intervention__session__intervention=intervention)

        skills_english = {'cvc2': '', 'letter': '', 'cvc4': '', 'syllable': '', 'spelling': '', 'cvcd': '', 'vccv': '',
                          'iblends': '', 'fblends': '', 'review92': '', 'vcccv': '', 'ngnk': '', 'suffix': '',
                          'magic': '', 'magic_e': '', 'cvce_test': '', 'magic2e': '', 'smagice': '', 'vcv': '',
                          'ph': '', 'ck': '', 'vowel': '', 'kkck': '', 'erir': '', 'owou': '', 'igh': '', 'ble': '',
                          'le': '', 'yvy': '', 'ild': '', 'aror': '', 'oo': '', 'y_vowel': '', 'soft_c': '',
                          'soft_g': '', 'gedge': '', 'gc': '', 'auaw': '', 'tch': '', 'ing': '', 'vcv_spelling': '',
                          'three_s': '', 'schwa': ''}

        if request.method == "POST":

            for skill in skills_english.keys():
                v = skills_english_objs.filter(skill_name=skill).first()
                if v:
                    skills_english[skill] = v.grade
                if skill in request.POST:
                    s = Skill_English.objects.create(skill_name=skill, grade=request.POST[skill],
                                                     a_intervention=a_intervention)

                    skills_english[skill] = s.grade
                    return render(request, 'static_files/session_evaluation.html',
                                  {'a_intv': a_intervention, 'skills': skills_english})

        else:
            for skill in skills_english.keys():
                v = skills_english_objs.filter(skill_name=skill).first()
                if v:
                    skills_english[skill] = v.grade
            print(skills_english)
            return render(request, 'static_files/session_evaluation.html',
                          {'a_intv': a_intervention, 'skills': skills_english})
    else:
        skills_arabic_objs = Skill_Arabic.objects.filter(a_intervention__session__intervention=intervention)
        general = ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20',
                   '21', '29', '30', '31', '32', '33', '34', '35', '36', '37']

        if request.method == "POST":
            letter_number = request.POST.get('letter_number', '')
            letter = Arabic_Letter.objects.get(letter_number=letter_number)
            skills_arabic = []
            if letter_number in general:
                skills_arabic = ['f%one', 'f%two', 'f%three', 'f%four', 'f%five', 'f%six', 'f%seven', 'l%eight']
            elif letter_number == '8':
                skills_arabic = ['f%a_one', 'l%a_two']
            elif letter_number == '14':
                skills_arabic = ['l%b_one']
            elif letter_number == '22':
                skills_arabic = ['f%c_one', 'l%c_two']
            elif letter_number == '23':
                skills_arabic = ['f%d_one', 'f%d_two', 'f%d_three', 'l%d_four']
            elif letter_number == '24':
                skills_arabic = ['l%e_one']
            elif letter_number == '25':
                skills_arabic = ['l%f_one']
            elif letter_number == '26':
                skills_arabic = ['f%g_one', 'l%g_two']
            elif letter_number == '27':
                skills_arabic = ['f%h_one', 'l%h_two']
            elif letter_number == '28':
                skills_arabic = ['l%i_one']

            for skill in skills_arabic:
                if skill in request.POST:
                    skil = skill.split('%')
                    n_of_letters = skills_arabic_objs.count()
                    if not skills_arabic_objs.filter(letter=letter).first():
                        skills = Skill_Arabic.objects.create(a_intervention=a_intervention, letter=letter)
                        x = skills._meta.get_field(skil[1])
                        y = (str(x).split('.'))[2]
                        setattr(skills, y, request.POST[skill])
                        skills.save()
                    else:
                        skills = skills_arabic_objs.filter(letter=letter).first()
                        skills.a_intervention = a_intervention
                        x = skills._meta.get_field(skil[1])
                        y = (str(x).split('.'))[2]
                        setattr(skills, y, request.POST[skill])
                        skills.save()
                    if skil[0] == 'l':
                        if int(letter_number) == 37:
                            messages.success(request, message='All Letters Finished')
                            return redirect(search_assessment)
                        else:
                            letter = Arabic_Letter.objects.get(letter_number=int(letter_number) + 1)
                        Skill_Arabic.objects.create(a_intervention=a_intervention, letter=letter)
                        return redirect(session_evaluation, id)

                    return render(request, 'static_files/session_evaluation_arabic.html', {'a_intv': a_intervention,
                                                                                           'letter_number': letter_number,
                                                                                           'skills': skills,
                                                                                           'n_of_letters': n_of_letters,
                                                                                           'general': general})

            n_of_letters = skills_arabic_objs.count()
            if not skills_arabic_objs.filter(letter=letter).first():
                skills = Skill_Arabic.objects.create(a_intervention=a_intervention, letter=letter)
            else:
                skills = Skill_Arabic.objects.filter(a_intervention__session__intervention=intervention)
            return render(request, 'static_files/session_evaluation_arabic.html', {'a_intv': a_intervention,
                                                                                   'skills': skills,
                                                                                   'letter_number': letter_number,
                                                                                   'n_of_letters': n_of_letters,
                                                                                   'general': general})

        else:
            n_of_letters = skills_arabic_objs.count()
            if n_of_letters == 0:
                n_of_letters = 1
            # if count != 0:
            #     reg_eva = Evaluation_regular.objects.get(intervention=a_intervention)
            #     n_of_letters = Skill_Arabic.objects.filter(evaluation_regular=reg_eva).count()
            return render(request, 'static_files/session_evaluation_arabic.html', {'a_intv': a_intervention,
                                                                                   'letter_number': 0,
                                                                                   'n_of_letters': n_of_letters,
                                                                                   'general': general})


@login_required(login_url='login')
def registration_student(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        nationality = request.POST['nationality']
        language = request.POST['language']
        profile_pic = request.FILES.get('profile_pic', None)
        id_pic = request.FILES.get('id_pic', None)
        g_f_name = request.POST['g_f_name']
        g_l_name = request.POST['g_l_name']
        country_code = request.POST['country_code']
        mobile_number = request.POST['mobile']
        email = request.POST['email']
        school_name = request.POST['school_name']
        class_name = request.POST['class_name']
        s_language = request.POST['s_language']

        parent = Person.objects.filter(first_name=g_f_name, last_name=g_l_name, country_code=country_code,
                                       mobile_number=mobile_number).first()
        if not parent:
            role = Role.objects.get(name='Parent')
            parent = Person.objects.create(first_name=g_f_name, last_name=g_l_name, country_code=country_code,
                                           mobile_number=mobile_number)
            # g_f_name = ''.join(parent.first_name.split(' '))
            # g_l_name = ''.join(parent.last_name.split(' '))
            parent.username = f'{parent.mobile_number}'
            parent.role = role
            parent.save()
        student = Person(email=email, first_name=f_name, last_name=l_name, gender=gender,
                         dob=format_date_model(dob), profile_pic=profile_pic, register_id=id_pic,
                         mobile_number=mobile_number,
                         country_code=country_code,
                         school=school_name, class_name=class_name, nationality=nationality, language=language,
                         s_language=s_language)
        f_name = ''.join(student.first_name.split(' '))
        l_name = ''.join(student.last_name.split(' '))
        # student.username = f'{f_name}{l_name}{student.id}'
        # student.username = ''.join(student.username.split(' '))
        role = Role.objects.get(name="Student")
        student.role = role
        student.approved = True
        student.parent = parent
        student.save()
        student.username = f'{student.id}'
        student.save()

        return redirect(search_student)
    return render(request, 'static_files/registration_student.html')


@login_required(login_url='login')
def edit_student(request, id):
    student = Person.objects.get(id=id)

    if request.method == "POST":
        student.nationality = request.POST['nationality']
        student.language = request.POST['language']
        student.country_code = request.POST['country_code']
        student.mobile_number = request.POST['mobile']
        student.school = request.POST['school_name']
        student.class_name = request.POST['class_name']
        student.s_language = request.POST['s_language']

        g_f_name = request.POST['g_f_name']
        g_l_name = request.POST['g_l_name']
        parent = Person.objects.filter(first_name__icontains=g_f_name, last_name__icontains=g_l_name,
                                       country_code=request.POST['country_code'],
                                       mobile_number=request.POST['mobile']).first()
        if not parent and g_f_name:
            role = Role.objects.get(name='Parent')
            parent = Person.objects.create(first_name=g_f_name, last_name=g_l_name,
                                           country_code=request.POST['country_code'],
                                           mobile_number=request.POST['mobile'])
            # g_f_name = ''.join(parent.first_name.split(' '))
            # g_l_name = ''.join(parent.last_name.split(' '))
            parent.username = f'{parent.mobile_number}'
            parent.role = role
            parent.save()

        student.email = request.POST['email']
        student.save()

        return redirect(search_student)

    return render(request, 'static_files/registration_student.html', {'student': student, 'edit': True})


@login_required(login_url='login')
def todays_appoint_list(request):
    children = set()
    psychologists = set()
    if request.user.role.name == 'Receptionist':
        appoin_list = Appointment.objects.filter(appointment_date=datetime.datetime.now().date())
    else:
        appoin_list = Appointment.objects.filter(psychologist=request.user,
                                                 appointment_date=datetime.datetime.now().date())
    if request.method == "POST":
        s_by_name = request.POST['s_by_name']
        p_by_name = ''
        if request.user.role.name == "Receptionist":
            p_by_name = request.POST['p_by_name']
        if s_by_name:
            appoin_list = appoin_list.filter(child__username=s_by_name)
        if p_by_name:
            appoin_list = appoin_list.filter(psychologist__username=p_by_name)
    else:
        for appoint in appoin_list:
            children.add(appoint.child)
            psychologists.add(appoint.psychologist)
    return render(request, 'static_files/appointment_list.html', {'objs': appoin_list, 'today': True,
                                                                  'children': children, 'psychologists': psychologists})


@login_required(login_url='login')
def todays_intervention(request):
    status = ''
    students = set()
    teachers = set()
    subjs = set()
    if request.user.role.name == 'Receptionist':
        sessions = Session.objects.filter(day=daysname[str(datetime.datetime.now().weekday())],
                                          intervention__status='Active', is_active=True)
    else:
        sessions = Session.objects.filter(intervention__teacher=request.user,
                                          day=daysname[str(datetime.datetime.now().weekday())],
                                          intervention__status='Active', is_active=True)
    if request.method == "POST":
        sname = request.POST['search_by_sname']
        if request.user.role.name == 'Receptionist':
            tname = request.POST['search_by_tname']
            subj = request.POST['search_by_s']
        else:
            tname = ''
            subj = ''
        if subj:
            sessions = sessions.filter(intervention__teacher__subject_teaching=subj)
        if sname:
            sessions = sessions.filter(intervention__student__username=sname)
        if tname:
            sessions = sessions.filter(intervention__teacher__username=sname)

        cancelled_ids = {}
        f_reason = {'attended': 'Attended', 's_absent': 'Student Absent', 't_absent': 'Teacher Absent',
                    'cancelled': 'Cancelled'}
        for i in sessions:
            reason = All_Intervention.objects.get(session=i, date=current_time.date()).status
            cancelled_ids.update({i.id: f_reason[reason]})
    else:
        for session in sessions:
            students.add(session.intervention.student)
            teachers.add(session.intervention.teacher)
            subjs.add(session.intervention.teacher.subject_teaching)
            if All_Intervention.objects.filter(session=session, date=current_time.date()).count() == 0:
                All_Intervention.objects.create(session=session, date=current_time.date())
        cancelled_ids = {}
        f_reason = {'attended': 'Attended', 's_absent': 'Student Absent', 't_absent': 'Teacher Absent',
                    'cancelled': 'Cancelled'}
        for i in sessions:
            reason = All_Intervention.objects.get(session=i, date=current_time.date()).status
            cancelled_ids.update({i.id: f_reason[reason]})
    return render(request, 'static_files/todays_intervention.html', {'interventions': sessions, 'today': True,
                                                                     'status': status, 'c_ids': cancelled_ids,
                                                                     'students': students, 'teachers': teachers,
                                                                     'subjs': subjs})


@login_required(login_url='login')
def todays_status(request, id, reason):
    count = All_Intervention.objects.filter(session_id=id, date=current_time.date()).count()
    if count == 0:
        if Intervention.objects.get(id=id).status == 'Active':
            All_Intervention.objects.create(session_id=id, date=current_time.date(), reason=reason)
    else:
        obj = All_Intervention.objects.get(session_id=id, date=current_time.date())
        obj.status = reason
        obj.save()

    return redirect(todays_intervention)


@login_required(login_url='login')
def search_student(request):
    students = ''
    if request.method == "POST":
        students = Person.objects.filter(role__name='Student')
        name = request.POST['search_by_name']
        if name:
            name = name.split(" ")
            for n in name:
                students = Person.objects.filter(role__name="Student", first_name__icontains=n)
                if not students:
                    students = Person.objects.filter(role__name="Student", last_name__icontains=n)
    else:
        students = Person.objects.filter(role__name='Student')

    return render(request, 'static_files/search_student.html', {'students': students})


@login_required(login_url='login')
def report_all_appointments(request):
    appointments = Appointment.objects.all()
    psys = []
    children = []
    for appointment in appointments:
        if appointment.psychologist not in psys:
            psys.append(appointment.psychologist)
        if appointment.child not in children:
            children.append(appointment.child)
    if request.method == "POST":
        if 'range' in request.POST:
            fromm = request.POST['fromm']
            too = request.POST['to']
            if fromm and too:
                fromm = fromm.split('/')
                too = too.split('/')
                fromm = datetime.date(int(fromm[2]), int(fromm[1]), int(fromm[0]))
                too = datetime.date(int(too[2]), int(too[1]), int(too[0]))
                appoints = Appointment.objects.filter(appointment_date__gte=fromm, appointment_date__lte=too)
                assessments = []
                for p in appoints:
                    if Assessment_psy.objects.filter(appointment=p).count() != 0:
                        assessments.append(p)
                return render(request, 'static_files/report_all_appointments.html', {'psys': psys, 'display': 'dates',
                                                                                     'appoints': appoints,
                                                                                     'fromm': format_date_html(fromm),
                                                                                     'too': format_date_html(too),
                                                                                     'assessments': assessments})
            else:
                messages.warning(request, message="Kindly fill the range of dates")
                return redirect(report_all_appointments)

        if 'psy_btn' in request.POST:
            psy = request.POST['psy']
            p = Person.objects.get(username=psy)
            assessments = []
            past_appoints = Appointment.objects.filter(psychologist__username=psy,
                                                       appointment_date__lt=current_time.date())
            for pp in past_appoints:
                if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                    assessments.append(pp)
            current_appoints = Appointment.objects.filter(psychologist__username=psy,
                                                          appointment_date__gte=current_time.date())
            return render(request, 'static_files/report_all_appointments.html', {'psys': psys, 'display': 'psy',
                                                                                 'psyy': p, 'p_appoints': past_appoints,
                                                                                 'c_appoints': current_appoints,
                                                                                 'assessments': assessments})
        if 'child_btn' in request.POST:
            child = request.POST['child']
            p = Person.objects.get(username=child)
            assessments = []
            past_appoints = Appointment.objects.filter(child__username=child,
                                                       appointment_date__lt=current_time.date())
            for pp in past_appoints:
                if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                    assessments.append(pp)
            current_appoints = Appointment.objects.filter(child__username=child,
                                                          appointment_date__gte=current_time.date())
            return render(request, 'static_files/report_all_appointments.html',
                          {'children': children, 'display': 'child',
                           'ch': p, 'p_appoints': past_appoints,
                           'c_appoints': current_appoints,
                           'assessments': assessments})
    else:
        return render(request, 'static_files/report_all_appointments.html', {'psys': psys, 'children': children,
                                                                             'display': 'all'})


@login_required(login_url='login')
def report_all_sessions(request):
    intvs = Intervention.objects.all()
    teachers = []
    students = []
    for intv in intvs:
        if intv.teacher not in teachers:
            teachers.append(intv.teacher)
        if intv.student not in students:
            students.append(intv.student)
    student = ''
    if request.method == "POST":
        if 'range' in request.POST:
            fromm = (request.POST['fromm']).split('/')
            too = (request.POST['to']).split('/')
            fromm = datetime.date(int(fromm[2]), int(fromm[1]), int(fromm[0]))
            too = datetime.date(int(too[2]), int(too[1]), int(too[0]))
            sessions = All_Intervention.objects.filter(date__gte=fromm, date__lte=too)
            return render(request, 'static_files/report_all_sessions.html', {'teachers': teachers, 'display': 'dates',
                                                                             'sessions': sessions,
                                                                             'fromm': format_date_html(fromm),
                                                                             'too': format_date_html(too)})
        past_sessions = ''
        t = ''
        p_sessions_dict = {}
        if 'teach' in request.POST:
            teacher = request.POST['teacher']
            t = Person.objects.get(username=teacher)
            past_sessions = All_Intervention.objects.filter(date__lte=current_time.date(),
                                                            session__intervention__teacher=t)
            students = []
            for p in past_sessions:
                if p.session.intervention.student not in students:
                    students.append(p.session.intervention.student)

        if 'stud_btn' in request.POST:
            stu_username = request.POST['student']
            s = Person.objects.get(username=stu_username)
            past_sessions = All_Intervention.objects.filter(date__lte=current_time.date(),
                                                            session__intervention__student=s)

            return render(request, 'static_files/report_all_sessions.html', {'display': 'student',
                                                                             'stud': s, 'p_sessions': past_sessions,
                                                                             'students': students})

        if 'search' in request.POST:
            student = request.POST['student']
            teacher = request.POST['teacher']
            t = Person.objects.get(username=teacher)
            past_sessions = All_Intervention.objects.filter(date__lte=current_time.date(),
                                                            session__intervention__teacher__username=teacher,
                                                            session__intervention__student__username=student)
        if 'report' in request.POST:
            student = request.POST['student']
            teacher = request.POST['teacher']
            student_id = Person.objects.get(username=student).id
            teacher_id = Person.objects.get(username=teacher).id
            return redirect(report_session, teacher_id, student_id)
        return render(request, 'static_files/report_all_sessions.html', {'teachers': teachers, 'display': 'teacher',
                                                                         'teacherr': t, 'p_sessions': past_sessions,
                                                                         'students': students, 'stu': student, })
    else:
        sessions = Session.objects.filter(day=daysname[str(datetime.datetime.now().weekday())],
                                          intervention__status='Active', is_active=True)
        for session in sessions:
            if All_Intervention.objects.filter(session=session, date=current_time.date()).count() == 0:
                if session.intervention.status == 'Active':
                    All_Intervention.objects.create(session=session, date=current_time.date())
        return render(request, 'static_files/report_all_sessions.html', {'teachers': teachers, 'display': 'all',
                                                                         'students': students})


@login_required(login_url='login')
def assessment_graph(request, id):
    objs = Assessment_psy.objects.filter(appointment_id=id)
    print(objs)
    appointment = objs.first().appointment
    child = appointment.child
    psy = appointment.psychologist

    singles = [0, 0, 0]
    singles_t = [0, 0, 0]
    acops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    acops_t = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    junior = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    junior_t = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondary = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondary_t = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for obj in objs:
        if obj.test_name == "iq":
            singles[0] = obj.sub_score
            singles_t[0] = obj.sub_time
        if obj.test_name == "standford":
            singles[1] = obj.sub_score
            singles_t[1] = obj.sub_time
        if obj.test_name == "weksler":
            if obj.sub_test_name == "Total IQ":
                singles[2] = float(obj.sub_score_float)
        if obj.test_name == "acops":
            if obj.sub_test_name == "Rabbits":
                acops[1] = obj.sub_score
                acops_t[1] = obj.sub_time
            if obj.sub_test_name == "Zoid Friends":
                acops[2] = obj.sub_score
                acops_t[2] = obj.sub_time
            if obj.sub_test_name == "Zoid Letter Names":
                acops[3] = obj.sub_score
                acops_t[3] = obj.sub_time
            if obj.sub_test_name == "Zoid Letters":
                acops[4] = obj.sub_score
                acops_t[4] = obj.sub_time
            if obj.sub_test_name == "Wock":
                acops[5] = obj.sub_score
                acops_t[5] = obj.sub_time
            if obj.sub_test_name == "Ryhms":
                acops[6] = obj.sub_score
                acops_t[6] = obj.sub_time
            if obj.sub_test_name == "Races":
                acops[7] = obj.sub_score
                acops_t[7] = obj.sub_time
            if obj.sub_test_name == "Toybox":
                acops[8] = obj.sub_score
                acops_t[8] = obj.sub_time
        if obj.test_name == "junior":
            if obj.sub_test_name == "Spelling":
                junior[1] = obj.sub_score
                junior_t[1] = obj.sub_time
            if obj.sub_test_name == "Reading":
                junior[2] = obj.sub_score
                junior_t[2] = obj.sub_time
            if obj.sub_test_name == "Single Word Reading":
                junior[3] = obj.sub_score
                junior_t[3] = obj.sub_time
            if obj.sub_test_name == "Mobile":
                junior[4] = obj.sub_score
                junior_t[4] = obj.sub_time
            if obj.sub_test_name == "Funny Words":
                junior[5] = obj.sub_score
                junior_t[5] = obj.sub_time
            if obj.sub_test_name == "Segment":
                junior[6] = obj.sub_score
                junior_t[6] = obj.sub_time
            if obj.sub_test_name == "Cave":
                junior[7] = obj.sub_score
                junior_t[7] = obj.sub_time
        if obj.test_name == "secondary":
            if obj.sub_test_name == "Spelling":
                secondary[1] = obj.sub_score
                secondary_t[1] = obj.sub_time
            if obj.sub_test_name == "Reading":
                secondary[2] = obj.sub_score
                secondary_t[2] = obj.sub_time
            if obj.sub_test_name == "Single Word Reading":
                secondary[3] = obj.sub_score
                secondary_t[3] = obj.sub_time
            if obj.sub_test_name == "Mobile":
                secondary[4] = obj.sub_score
                secondary_t[4] = obj.sub_time
            if obj.sub_test_name == "Funny Words":
                secondary[5] = obj.sub_score
                secondary_t[5] = obj.sub_time
            if obj.sub_test_name == "Segment":
                secondary[6] = obj.sub_score
                secondary_t[6] = obj.sub_time
            if obj.sub_test_name == "Cave":
                secondary[7] = obj.sub_score
                secondary_t[7] = obj.sub_time
        print(acops)
    return render(request, 'static_files/assessments_graph.html', {'singles': singles, 'singles_t': singles_t,
                                                                   'child': child, 'psy': psy,
                                                                   'acops': acops, 'acops_t': acops_t,
                                                                   'junior': junior, 'junior_t': junior_t,
                                                                   'secondary': secondary, 'secondary_t': secondary_t})


@login_required(login_url='login')
def report_session(request, teacher_id, student_id):
    teacher = Person.objects.get(id=teacher_id)
    student = Person.objects.get(id=student_id)
    intervention = Intervention.objects.filter(student=student, teacher=teacher, status='Active').last()
    intv = All_Intervention.objects.filter(session__intervention=intervention)
    t_count = intv.count()
    attended = intv.filter(status='attended').count()
    cancelled = intv.filter(status='cancelled').count()
    s_absent = intv.filter(status='s_absent').count()
    t_absent = intv.filter(status='t_absent').count()
    counts = [t_count, attended, cancelled, s_absent, t_absent]

    percent_complete = ((attended) / (intervention.total_sessions)) * 100
    return render(request, 'static_files/report_session.html',
                  {'intervention': intervention, 'teacher': teacher, 'student': student, 'counts': counts,
                   'percent_complete': percent_complete})


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        # template = get_template('static_files/pdf.html')
        cc = Child_Case_Data.objects.get(child__username='student1')
        form = child_case_f(instance=cc)
        ss = serializers.serialize('json', [cc, ])
        pp = json.loads(ss)
        x = pp[0]['fields']
        context = {
            'form': form.fields,
            'obj': x
        }
        # html = template.render(context)
        pdf = render_to_pdf('pdfs/file1/page1.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % "12341231"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url='login')
def english_session_report(request, id):
    a_intervention = All_Intervention.objects.get(id=id)
    intervention = Intervention.objects.get(session__all_intv=a_intervention)
    marks = {'mastery': 4, 'n_mastery': 2}
    eng = Skill_English.objects.filter(a_intervention__session__intervention=intervention).order_by('id')
    # eng = Skill_English.objects.filter(a_intervention=a_intervention).order_by('id')
    result = [0] * 45
    if eng:
        # z = 0
        # for x in eng._meta.get_fields():
        #     y = (str(x).split('.'))[2]
        #     if getattr(eng, y):
        #         if getattr(eng, y) in marks.keys():
        #             result[z] = marks[getattr(eng, y)]
        #     z += 1
        z = 0
        for i in eng:
            result[z] = marks[i.grade]
            z += 1
    # result = result[2:]
    result1 = [0] + result[0:9]
    result2 = [0] + result[9:18]
    result3 = [0] + result[18:27]
    result4 = [0] + result[27:36]
    result5 = [0] + result[36:45]

    return render(request, 'static_files/english_session_report.html', {'a_intervention': a_intervention,
                                                                        'result1': result1, 'result2': result2,
                                                                        'result3': result3, 'result4': result4,
                                                                        'result5': result5})


@login_required(login_url='login')
def arabic_session_report(request, id):
    a_intervention = All_Intervention.objects.get(id=id)
    student = a_intervention.session.intervention.student
    teacher = a_intervention.session.intervention.teacher
    intervention = Intervention.objects.get(session__all_intv=a_intervention)
    n_of_letters = Skill_Arabic.objects.filter(a_intervention__session__intervention=intervention).count()
    if request.method == "POST":
        letter_number = request.POST['letter']
        letter = Arabic_Letter.objects.get(letter_number=letter_number)
        marks = {'acceptable': 2, 'good': 4, 'vgood': 6, 'excellent': 8}
        # eva_regular = Evaluation_regular.objects.filter(intervention=a_intervention).first()
        arabic = Skill_Arabic.objects.get(a_intervention__session__intervention=intervention,
                                          letter=letter)
        result = [0]
        general = ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11', '12', '13', '15', '16', '17', '18', '19', '20',
                   '21', '29', '30', '31', '32', '33', '34', '35', '36', '37']
        skills_arabic = []
        labels = []
        if letter_number in general:
            skills_arabic = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
            labels = ["", "يميز الصوت المكرر في الجملة العلاجية شفهياً", "يحدد مكان الحرف كتابياً.",
                      "يميز بين صوت الحرف المعالج القصير والطويل", "يكتب الحرف المعالج بصوتيه الطويل والقصير.",
                      "يحدد المقطع الساكن", "يقرأ جمل مكونة من كلمات مكونة من أصوات سبق دراستها.",
                      "يميز بين الكلمات المتشابهة بوضع دائرة حول الكلمة التي توافق",
                      "يكتب ما يملى عليه من كلمات مكونة من حروف سبق دراستها"]
        elif letter_number == '8':
            skills_arabic = ['a_one', 'a_two']
            labels = ["", "يميز بين أنواع التنوين الثلاثة", "يقرأ جمل محتوية على كلمات منونة"]
        elif letter_number == '14':
            skills_arabic = ['b_one']
            labels = ["", "يميز بين التاء المربوطة والمفتوحة"]
        elif letter_number == '22':
            skills_arabic = ['c_one', 'c_two']
            labels = ["", "يميز بين همزتي الوصل والقطع قراءةً", "يميز بين همزتي الوصل والقطع كتابةً"]
        elif letter_number == '23':
            skills_arabic = ['d_one', 'd_two', 'd_three', 'd_four']
            labels = ["", "يكتب كلمات محتوية على همزة متوسطة على ألف", "يكتب كلمات محتوية على همزة متوسطة على واو",
                      "يكتب كلمات محتوية على همزة متوسطة على ياء", "يكتب كلمات محتوية على همزة متوسطة على السطر"]
        elif letter_number == '24':
            skills_arabic = ['e_one']
            labels = ["", "يميز بين اشكال الهمزة آخر الكلمة المسبوقة بفتحة وضمة وكسرة"]
        elif letter_number == '25':
            skills_arabic = ['f_one']
            labels = ["", "يميز بين الألف المتطرفة الممدودة والتي تكتب على شكل الياء المقصورة"]
        elif letter_number == '26':
            skills_arabic = ['g_one', 'g_two']
            labels = ["", "يميز  المقطع المشددة قراءةً", "يميز المقطع المشدد كتابةً"]
        elif letter_number == '27':
            skills_arabic = ['h_one', 'h_two']
            labels = ["", "يميز بين اللام القمرية واللام الشمسية قراءةً",
                      "يميز بين اللام القمرية واللام الشمسية كتابةً"]
        elif letter_number == '28':
            skills_arabic = ['i_one']
            labels = ["",
                      "يجيد كتابة كلمات محتوية على ال التعريف دخل عليها حرف من حروف الجر ( بـ  , كـ  , لـ ) او حرف الفاء"]

        for skill in skills_arabic:
            a = getattr(arabic, skill)
            if a:
                result.append(marks[a])
            else:
                result.append(0)

        return render(request, 'static_files/arabic_session_report.html', {'student': student, 'teacher': teacher,
                                                                           'letter_number': letter_number,
                                                                           'result': result, 'intv': a_intervention,
                                                                           'n_of_letters': n_of_letters,
                                                                           'labels': labels})
    return render(request, 'static_files/arabic_session_report.html', {'student': student, 'teacher': teacher,
                                                                       'intv': a_intervention,
                                                                       'n_of_letters': n_of_letters})


@login_required(login_url='login')
def select_psy(request):
    if request.method == "POST":
        psy = request.POST['psy']
        psy_id = Person.objects.get(username=psy).id
        return redirect(dashboard_psy, psy_id)
    else:
        psys = Person.objects.filter(role__name='Physiologist')
        return render(request, 'static_files/select_psy.html', {'psys': psys})


@login_required(login_url='login')
def dashboard_psy(request, psy_id):
    psy = Person.objects.get(id=psy_id)
    if request.method == "POST":
        if 's_child_btn' in request.POST:
            child_username = request.POST['s_child']
            if child_username:
                child = Person.objects.get(username=child_username)
                assessments = []
                past_appoints = Appointment.objects.filter(psychologist_id=psy_id,
                                                           child__username=child_username,
                                                           appointment_date__lt=current_time.date())
                for pp in past_appoints:
                    if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                        assessments.append(pp)
                current_appoints = Appointment.objects.filter(psychologist_id=psy_id,
                                                              child__username=child_username,
                                                              appointment_date__gte=current_time.date())
                return render(request, 'static_files/dashboard_psy.html',
                              {'psy': psy, 'display': 's_name', 'p_appoints': past_appoints,
                               'c_appoints': current_appoints, 'assessments': assessments, 'child': child})
            else:
                messages.warning(request, message="Kindly select a child before applying filter")
                return redirect(dashboard_psy, psy.id)

        if 's_date_btn' in request.POST:
            selected_date = request.POST['s_date']
            if selected_date:
                selected_date = format_date_model(selected_date)
                assessments = []
                all_appointments = Appointment.objects.filter(psychologist_id=psy_id,
                                                              appointment_date=selected_date)
                for pp in all_appointments:
                    if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                        assessments.append(pp)
                return render(request, 'static_files/dashboard_psy.html',
                              {'psy': psy, 'display': 's_date', 'appoints': all_appointments,
                               'assessments': assessments,
                               'ss_date': format_date_html(selected_date)})
            else:
                messages.warning(request, message="Kindly select a date before applying filter")
                return redirect(dashboard_psy, psy.id)
        if 'range' in request.POST:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            if from_date and to_date:
                from_date = format_date_model(from_date)
                to_date = format_date_model(to_date)
                assessments = []
                all_appointments = Appointment.objects.filter(psychologist_id=psy_id,
                                                              appointment_date__gte=from_date,
                                                              appointment_date__lte=to_date)
                for pp in all_appointments:
                    if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                        assessments.append(pp)
                return render(request, 'static_files/dashboard_psy.html',
                              {'psy': psy, 'display': 'r_dates', 'appoints': all_appointments,
                               'assessments': assessments,
                               'f_date': format_date_html(from_date),
                               't_date': format_date_html(to_date)})
            else:
                messages.warning(request, message="Kindly select a date before applying filter")
                return redirect(dashboard_psy, psy.id)
    else:
        all_appoints = Appointment.objects.filter(psychologist=psy)
        children = []
        for a in all_appoints:
            if a.child not in children:
                children.append(a.child)
        assessments = []
        past_appoints = Appointment.objects.filter(psychologist=psy, appointment_date__lt=current_time.date())
        pa_count = past_appoints.count()
        for pp in past_appoints:
            if Assessment_psy.objects.filter(appointment=pp).count() != 0:
                assessments.append(pp)
        current_appoints = Appointment.objects.filter(psychologist=psy,
                                                      appointment_date__gte=current_time.date())
        ca_count = current_appoints.count()
        return render(request, 'static_files/dashboard_psy.html',
                      {'psy': psy, 'display': 'all', 'p_appoints': past_appoints,
                       'c_appoints': current_appoints, 'assessments': assessments,
                       'children': children, 'pa_count': pa_count,
                       'ca_count': ca_count})


@login_required(login_url='login')
def select_teacher(request):
    if request.method == "POST":
        teacher = request.POST['teacher']
        teacher_id = Person.objects.get(username=teacher).id
        return redirect(dashboard_teacher, teacher_id)
    else:
        teachers = Person.objects.filter(role__name='Teacher')
        return render(request, 'static_files/select_teacher.html', {'teachers': teachers})


@login_required(login_url='login')
def dashboard_teacher(request, teacher_id):
    teacher = Person.objects.get(id=teacher_id)
    intvs = Session.objects.filter(intervention__teacher=teacher, intervention__status='Active', is_active=True)
    monday = {}
    tuesday = {}
    wednesday = {}
    thursday = {}
    saturday = {}
    sunday = {}
    for x in range(24):
        monday.update({x: ''})
        tuesday.update({x: ''})
        wednesday.update({x: ''})
        thursday.update({x: ''})
        saturday.update({x: ''})
        sunday.update({x: ''})

    for intv in intvs:
        if intv.day == 'Monday':
            monday.update({int(time_slots_r[intv.time]): intv})
        if intv.day == 'Tuesday':
            tuesday.update({int(time_slots_r[intv.time]): intv})
        if intv.day == 'Wednesday':
            wednesday.update({int(time_slots_r[intv.time]): intv})
        if intv.day == 'Thursday':
            thursday.update({int(time_slots_r[intv.time]): intv})
        if intv.day == 'Saturday':
            saturday.update({int(time_slots_r[intv.time]): intv})
        if intv.day == 'Sunday':
            sunday.update({int(time_slots_r[intv.time]): intv})

    from_date = ''
    to_date = ''
    if request.method == 'POST':
        from_date = format_date_model(request.POST['from_date'])
        to_date = format_date_model(request.POST['to_date'])

        all_intvs = All_Intervention.objects.filter(session__intervention__teacher=teacher, status='attended',
                                                    date__gte=from_date, date__lte=to_date)
    else:
        all_intvs = All_Intervention.objects.filter(session__intervention__teacher=teacher)
        for all_intv in all_intvs:
            if all_intv.session.intervention.teacher_change_date:
                if all_intv.session.intervention.teacher_change_date >= all_intv.date:
                    all_intvs.exclude(id=all_intv.id)

    on_going = Intervention.objects.filter(teacher=teacher, status='Active').count()
    concluded = all_intvs.count()
    attended = all_intvs.filter(status='attended').count()
    stu_absents = all_intvs.filter(status='s_absent').count()
    teacher_absents = all_intvs.filter(status='t_absent').count()
    cancelled = all_intvs.filter(status='cancelled').count()

    return render(request, 'static_files/dashboard_teacher.html', {'teacher': teacher, 'monday': monday,
                                                                   'tuesday': tuesday, 'wednesday': wednesday,
                                                                   'thursday': thursday, 'saturday': saturday,
                                                                   'sunday': sunday, 'all_intvs': all_intvs,
                                                                   'on_going': on_going, 'concluded': concluded,
                                                                   'attended': attended, 'stu_absents': stu_absents,
                                                                   'teacher_absents': teacher_absents,
                                                                   'cancelled': cancelled, 'loop': range(24),
                                                                   'from_date': '' if from_date == '' else format_date_html(
                                                                       from_date),
                                                                   'to_date': '' if to_date == '' else format_date_html(
                                                                       to_date)})


@login_required(login_url='login')
def select_student(request, fromm):
    if request.method == "POST":
        student_id = request.POST['student']
        # student_id = Person.objects.get(id=student).id
        if fromm == 'recep':
            return redirect(dashboard_student, student_id)
        elif fromm == 'intervention':
            return redirect(add_intervention, student_id)
    else:
        if request.user.role.name == "Parent":
            students = Person.objects.filter(parent=request.user, role__name='Student')
        else:
            students = Person.objects.filter(role__name='Student')
        return render(request, 'static_files/select_student.html', {'students': students, 'fromm': fromm})


@login_required(login_url='login')
def dashboard_student(request, student_id):
    if request.method == "POST":
        if 'English' in request.POST:
            intervention = Intervention.objects.filter(student_id=student_id,
                                                       teacher__subject_teaching='English').last()
            if request.FILES.get('homework_file'):
                Homeworks.objects.create(file=request.FILES.get('homework_file'), intervention=intervention)
                messages.success(request, message='Uploaded Successfully')
        elif 'Arabic' in request.POST:
            intervention = Intervention.objects.filter(student_id=student_id,
                                                       teacher__subject_teaching='Arabic').last()
            if request.FILES.get('homework_file'):
                Homeworks.objects.create(file=request.FILES.get('homework_file'), intervention=intervention)
                messages.success(request, message='Uploaded Successfully')
    student = Person.objects.get(id=student_id)
    sessions = Intervention.objects.filter(student=student)
    subjs = {}
    all_interventions = []
    for s in sessions:
        subjs.update({s.teacher.subject_teaching: s})
        if s.pending_s_date:
            f_date = s.pending_s_date + datetime.timedelta(days=14)
            print(f_date)
            if current_time.date() > f_date:
                s.status = 'Not_Active'
                s.pending_s_date = None
                s.save()
        all_interventions.append({'teacher': s.teacher, 'student': s.student, 'total_sessions': s.total_sessions,
                                  'start_date': s.start_date, 'status': s.status, 'id': s.id,
                                  'sessions': [x for x in Session.objects.filter(intervention=s, is_active=True)],
                                  'count': Session.objects.filter(intervention=s, is_active=True).count(),
                                  'conducted': All_Intervention.objects.filter(session__intervention=s,
                                                                               status='attended').count()})
    assessment = Assessment_psy.objects.filter(appointment__child=student).first()
    all_intvs = All_Intervention.objects.filter(session__intervention__student=student)
    on_going = Intervention.objects.filter(student=student, status='Active').count()
    concluded = all_intvs.count()
    attended = all_intvs.filter(status='attended').count()
    stu_absents = all_intvs.filter(status='s_absent').count()
    teacher_absents = all_intvs.filter(status='t_absent').count()
    cancelled = all_intvs.filter(status='cancelled').count()
    child_case = Child_Case_Data.objects.filter(child_id=student_id).first()
    stanford = Assessment_psy.objects.filter(appointment__child=student, test_name='standford')
    secondary = Assessment_psy.objects.filter(appointment__child=student, test_name='secondary')
    junior = Assessment_psy.objects.filter(appointment__child=student, test_name='junior')
    acops = Assessment_psy.objects.filter(appointment__child=student, test_name='acops')
    parent = Person.objects.filter(children__id=student_id).first()
    if concluded > 0:
        attendance = 100 - ((stu_absents / (concluded - teacher_absents - cancelled)) * 100)
    else:
        attendance = 0
    return render(request, 'static_files/dashboard_student.html', {'student': student, 'subjs': subjs,
                                                                   'assessment': assessment, 'all_intvs': all_intvs,
                                                                   'all_interventions': all_interventions,
                                                                   'on_going': on_going, 'concluded': concluded,
                                                                   'attended': attended, 'stu_absents': stu_absents,
                                                                   'teacher_absents': teacher_absents,
                                                                   'cancelled': cancelled, 'attendance': attendance,
                                                                   'child_case': child_case, 'stanford': stanford,
                                                                   'secondary': secondary, 'junior': junior,
                                                                   'parent': parent, 'acops': acops
                                                                   })


skill_name = {'cvc2': 'Reviewing CVC words (2-3 letters)', 'letter': 'The letter sound',
              'cvc4': 'Review Test CVC Words (2-4 letters)', 'syllable': 'Two-Syllable Compound Words',
              'spelling': 'Spelling Rule –ff-ll-ss-zz ', 'cvcd': 'Spelling Rule –ff-ll-ss-zz ',
              'vccv': 'Syllabication –Method VC/CV', 'iblends': 'Initial Blends', 'fblends': 'Final Consonant Blends',
              'review92': 'Page 92 Review Test', 'vcccv': 'Multisyllabic words with Blends (VC/CV, VCCCV)',
              'ngnk': 'ng and nk Endings ', 'suffix': 'Suffix: ed as /id/ ;/d/; /t/', 'magic': 'Magic E',
              'magic_e': 'Review Test for Magic e Words', 'cvce_test': 'Review Test- CVC and CVCe Contrasts',
              'magic2e': 'Review Test- CVC and CVCe Contrasts', 'smagice': 'Syllable Magic e',
              'vcv': 'Syllable Magic e', 'ph': 'ph Digraph', 'ck': '-ck',
              'vowel': 'Pre test Vowel Digraphs ea, oa, ai, ee, ay, oe Introduce Vowel Digraphs not mastered',
              'kkck': 'Spellings for /k/: k, ck, or ke', 'erir': 'r-Controlled Vowels – er, ir, ,ur',
              'owou': 'Dipthongs ow; ou', 'igh': '-igh',
              'ble': 'Consonant le Endings (-ble; -fle; -tle; -dle; -gle; -kle; -ple; -zle)',
              'le': 'Doubling Rule Consonant-le',
              'yvy': 'Consonant-y Endings (y, vy, by, dy, ty, ry, ny, py, sy, my; -l y)',
              'ild': 'Word endings in –ild; -old; -ind-; olt, ost', 'aror': 'r-Controlled Vowels – ar, or,',
              'oo': 'Oo', 'y_vowel': 'y as a vowel', 'soft_c': 'Hard and Soft c', 'soft_g': 'Hard and Soft g',
              'gedge': 'Hard and Soft g', 'gc': 'Hard and Soft g', 'auaw': 'The Three (au)s - aw -au -a',
              'tch': 'Oi and oy, tch', 'ing': 'ing as an Ending',
              'vcv_spelling': 'VCV Spelling Rule ( Alternative Spelling and Pronunciation)',
              'three_s': 'Three Syllable Words', 'schwa': 'Schwa Sound'}

letter_name = {1: 'الراء', 2: 'الباء', 3: 'العين', 4: 'الدال', 5: 'السين', 6: 'الميم', 7: 'النون', 8: 'التنوين',
               9: 'الصاد', 10: 'الزاي', 11: 'الكاف', 12: 'الهاء', 13: 'النون', 14: 'التاء المربوطة', 15: 'الحاء',
               16: 'الواو', 17: 'الفاء', 18: 'الياء', 19: 'الضاد', 20: 'اللام', 21: 'الألف', 22: 'همزتا الوصل والقطع',
               23: 'الهمزة المتوسطة', 24: 'الهمزة آخر الكلمة', 25: 'الألف المتطرفة', 26: 'الشدة', 27: 'الـ التعريف',
               28: 'مهارة دخول حرف على الكلمة المبدوءة بـ ال', 29: 'القاف', 30: 'الجيم', 31: 'التاء', 32: 'الطاء',
               33: 'الغين', 34: 'الشين', 35: 'الذال', 36: 'الخاء', 37: 'الطاء'}

skills_arabic = {'one': 'يميز الصوت المكرر في الجملة العلاجية', 'two': 'يضع دائة حول الحرف المعالج',
                 'three': 'يميز بين صوت الحرف المعالج القصير والطويل',
                 'four': 'يكتب الحرف المعالج بأشكاله بحسب موقعه بالجملة', 'five': 'يحدد المقطع الساكن',
                 'six': 'يركب كلمات من مقاطع مد', 'seven': 'يقرأ جمل مكونة من  كلمات محتوية على أصوات سبق دراستها',
                 'eight': 'يكتب ما يملى عليه'}

grade = {'mastery': 4, 'n_mastery': 2}
grade_arabic = {'acceptable': 1, 'good': 2, 'vgood': 3, 'excellent': 4}
months = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June',
          '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


@login_required(login_url='login')
def monitor_performance(request, student_id, subj):
    student = Person.objects.get(id=student_id)
    intv = Intervention.objects.get(student=student, teacher__subject_teaching=subj)
    if subj == "English":
        skill_objs = Skill_English.objects.filter(a_intervention__session__intervention=intv).order_by('id')
        percent_complete = ((skill_objs.count()) / 43) * 100
        skills = []
        sum_of_marks = 0
        # skill_names = []        # For Graph
        skill_month = []  # For Graph
        n = 1
        for skill in skill_objs:
            skill_month.append({'x': skill.a_intervention.date, 'y': n})
            n = n + 1
            skills.append({'skill_name': skill_name[skill.skill_name], 'date': skill.a_intervention.date,
                           'percentage': ((grade[skill.grade]) / 4) * 100})
            sum_of_marks = sum_of_marks + grade[skill.grade]
        # skill_month1 = [0] + skill_month[0:9]
        # skill_month2 = [0] + skill_month[9:18]
        # skill_month3 = [0] + skill_month[18:27]
        # skill_month4 = [0] + skill_month[27:36]
        # skill_month5 = [0] + skill_month[36:45]

        if skill_objs.count() != 0:
            overall_percentage = (sum_of_marks / (skill_objs.count() * 4)) * 100
        else:
            overall_percentage = 0
        return render(request, 'static_files/monitor_performance.html', {'student': student, 'subj': subj,
                                                                         'percent_complete': percent_complete,
                                                                         'skills': skills,
                                                                         'skill_months': skill_month,
                                                                         'overall': overall_percentage,
                                                                         })
    else:
        letter_objs = Skill_Arabic.objects.filter(a_intervention__session__intervention=intv)
        percent_complete = ((letter_objs.count()) / 37) * 100
        letters = []
        tt_count = 0
        tt_marks = 0
        letters_months = []
        grouped_skills = {'one': [0, 0], 'two': [0, 0], 'three': [0, 0], 'four': [0, 0], 'five': [0, 0], 'six': [0, 0],
                          'seven': [0, 0], 'eight': [0, 0]}
        n = 1
        for letter in letter_objs:
            t_count = 0
            t_marks = 0
            for field in letter._meta.get_fields():
                y = (str(field).split('.'))[2]
                if y != 'id' and y != 'a_intervention' and y != 'letter':
                    if getattr(letter, y):
                        if y in grouped_skills.keys():
                            grouped_skills[y][0] = grouped_skills[y][0] + grade_arabic[getattr(letter, y)]
                            grouped_skills[y][1] = grouped_skills[y][1] + 1
                        t_marks = t_marks + grade_arabic[getattr(letter, y)]
                        t_count = t_count + 1
            letters_months.append({'x': letter.a_intervention.date, 'y': n})
            n = n + 1
            letters.append({'letter_name': letter_name[letter.letter.letter_number], 'date': letter.a_intervention.date,
                            'percentage': 0 if t_count == 0 else (t_marks / (t_count * 4)) * 100})
            tt_marks = tt_marks + (0 if t_count == 0 else (t_marks / (t_count * 4)) * 100)
            tt_count = tt_count + 1

        # letters_month.pop()
        # letters_month1 = [0] + letters_month[0:9]
        # letters_month2 = [0] + letters_month[9:18]
        # letters_month3 = [0] + letters_month[18:27]
        # letters_month4 = [0] + letters_month[27:37]

        if tt_count != 0:
            overall_percentage = (tt_marks / tt_count)
        else:
            overall_percentage = 0
        skills = {}
        # if letters_month1 == [0]:
        #     letters_month1 = [0]*10
        # if letters_month2 == [0]:
        #     letters_month2 = [0]*10
        # if letters_month3 == [0]:
        #     letters_month3 = [0]*10
        # if letters_month4 == [0]:
        #     letters_month4 = [0]*11
        for skill, value in grouped_skills.items():
            if value[1] != 0:
                skills.update({skills_arabic[skill]: ((value[0]) / (value[1] * 4)) * 100})
        return render(request, 'static_files/monitor_performance.html', {'student': student, 'subj': subj,
                                                                         'percent_complete': percent_complete,
                                                                         'letters': letters,
                                                                         'overall': overall_percentage,
                                                                         'grouped_skills': skills,
                                                                         'letters_months': letters_months,
                                                                         })


@login_required(login_url='login')
def assign_parent(request, student_id):
    student = Person.objects.get(id=student_id)
    parents = Person.objects.filter(role__name='Parent')
    parent = Person.objects.filter(children__id=student_id).first()
    if request.method == "POST":
        parent_username = request.POST['parent']
        parent = Person.objects.get(username=parent_username)

        student.parent = parent
        student.save()

        return redirect(dashboard_student, student_id)
    return render(request, 'static_files/choose_parent.html', {'student': student, 'parents': parents,
                                                               'par': parent})


@login_required(login_url='login')
def add_parent(request, student_id):
    student = Person.objects.get(id=student_id)
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        country_code = request.POST['country_code']
        mobile = request.POST['mobile']
        role = Role.objects.get(name='Parent')
        parent = Person.objects.create(first_name=f_name, last_name=l_name, username='aa', role=role,
                                       country_code=country_code, mobile_number=mobile)

        uf_name = ''.join(f_name.split(' '))
        ul_name = ''.join(l_name.split(' '))
        # username = f'{uf_name}{ul_name}{parent.id}'
        parent.username = f'{parent.mobile_number}'
        student.parent = parent

        student.save()
        parent.save()

        return redirect(dashboard_student, student_id)

    return render(request, 'static_files/add_parent.html', {'student': student})


def str_to_date(date_string):
    date_array = date_string.split('/')
    date = int(date_array[0])
    month = int(date_array[1])
    year = int(date_array[2])

    new_date = datetime.date(year, month, date)

    return new_date


@login_required(login_url='login')
def change_status_student(request, id):
    intervention = Intervention.objects.get(id=id)
    current_status = intervention.status
    if request.method == 'POST':
        status = request.POST['status']
        intervention.status = status
        if status == 'Pending' or status == 'Not_Active':
            if status == 'Pending':
                intervention.pending_s_date = current_time.date()
            else:
                intervention.pending_s_date = None
            sessions = Session.objects.filter(intervention=intervention, is_active=True)
            for session in sessions:
                session.is_active = False
                session.save()
            intervention.save()
        else:
            intervention.pending_s_date = None
            intervention.save()
            if current_status == 'Pending':
                return redirect(check_intervention, intervention.student.id, intervention.teacher.id)
            elif current_status == 'Not_Active':
                return redirect(select_teacher_status_change, intervention.id)

        return redirect(dashboard_student, intervention.student.id)
    return render(request, 'static_files/change_status_student.html', {'intervention': intervention})


@login_required(login_url='login')
def select_teacher_status_change(request, id):
    intervention = Intervention.objects.get(id=id)
    teachers = Person.objects.filter(role__name='Teacher',
                                     subject_teaching=intervention.teacher.subject_teaching).exclude(
        id=intervention.teacher.id)
    if request.method == 'POST':
        teacher_username = request.POST['teacher']
        teacher = Person.objects.get(username=teacher_username)
        intervention.teacher = teacher
        intervention.teacher_change_date = current_time.date()
        intervention.save()

        sessions = Session.objects.filter(intervention=intervention, is_active=True)
        for session in sessions:
            session.is_active = False
            session.save()

        return redirect(check_intervention, intervention.student.id, intervention.teacher.id)
    return render(request, 'static_files/select_teacher.html', {'teachers': teachers, 'status_change': True})


@login_required(login_url='login')
def registration_psy(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        language = request.POST['language']
        country_code = request.POST['country_code']
        mobile_number = request.POST['mobile']
        id_pic = request.FILES.get('id_pic')
        username = request.POST['username']
        password = request.POST['password']

        person = Person.objects.filter(email=email).first()
        if person:
            messages.warning(request, message="Email Already Registered")
            return redirect(registration_psy)
        person = Person.objects.filter(username=username).first()
        if person:
            messages.warning(request, message="Username Already in use. Try another!")
            return redirect(registration_psy)

        psy = Person(first_name=f_name, last_name=l_name, register_id=id_pic, mobile_number=mobile_number,
                     country_code=country_code,
                     email=email, username=username, language=language, )
        role = Role.objects.get(name="Physiologist")
        psy.role = role
        psy.approved = True
        psy.set_password(password)
        psy.save()

        for x in request.POST.getlist('checks'):
            Test.objects.get(test_name=x).psychologist.add(psy)

        return redirect(search_psy)
    return render(request, 'static_files/registration_psy.html')


@login_required(login_url='login')
def change_password(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        password = request.POST['password']
        person.set_password(password)
        person.save()

        messages.success(request, message="Password Changed")
        if person.role.name == "Teacher":
            return redirect(search_teacher)
        elif person.role.name == "Physiologist":
            return redirect(search_psy)
        else:
            return redirect(search_student)
    return render(request, 'static_files/change_password.html', {'person': person})


@login_required(login_url='login')
def test_lists(request, id):
    psy = Person.objects.get(id=id)
    tests = Test.objects.filter(psychologist=psy)

    return render(request, 'static_files/test_list.html', {'psy': psy, 'tests': tests})


@login_required(login_url='login')
def registration_teacher(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        language = request.POST['language']
        country_code = request.POST['country_code']
        mobile_number = request.POST['mobile']
        id_pic = request.FILES.get('id_pic')
        qualification = request.POST['qualification']
        course = request.POST['course']
        certificate = request.FILES.get('certificate')
        username = request.POST['username']
        password = request.POST['password']

        person = Person.objects.filter(email=email).first()
        if person:
            messages.warning(request, message="Email Already Registered")
            return redirect(registration_psy)
        person = Person.objects.filter(username=username).first()
        if person:
            messages.warning(request, message="Username Already in use. Try another!")
            return redirect(registration_psy)

        teacher = Person(first_name=f_name, last_name=l_name, register_id=id_pic, mobile_number=mobile_number,
                         country_code=country_code,
                         email=email, username=username, language=language, qualification=qualification,
                         subject_teaching=course, certificate=certificate)
        role = Role.objects.get(name="Teacher")
        teacher.role = role
        teacher.approved = True
        teacher.set_password(password)
        teacher.save()

        return redirect(search_teacher)
    return render(request, 'static_files/registration_teacher.html')


import convertapi

convertapi.api_secret = 'IqqTZPI6mCvzto4E'


def test_pdf(request):
    # page1
    child = Person.objects.get(id=5)
    cc = Child_Case_Data.objects.get(child=child)
    appoint = Appointment.objects.filter(child=child).last()
    a = Assessment_psy.objects.filter(appointment__child=child, test_name='standford').first()

    reading = Assessment_psy.objects.filter(appointment__child_id=5, test_name='secondary',
                                            sub_test_name='Reading').last()
    spelling = Assessment_psy.objects.filter(appointment__child_id=5, test_name='junior',
                                             sub_test_name='Spelling').last()
    mobile = Assessment_psy.objects.filter(appointment__child_id=5, test_name='junior', sub_test_name='Mobile').last()
    funny = Assessment_psy.objects.filter(appointment__child_id=5, test_name='junior',
                                          sub_test_name='Funny Words').last()
    segment = Assessment_psy.objects.filter(appointment__child_id=5, test_name='junior', sub_test_name='Segment').last()
    cave = Assessment_psy.objects.filter(appointment__child_id=5, test_name='junior', sub_test_name='Cave').last()

    # acops
    rabbits = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Rabbits').last()
    zoid_friends = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                 sub_test_name='Zoid Friends').last()
    zoid_letter_names = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                      sub_test_name='Zoid Letter Names').last()
    zoid_letters = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                 sub_test_name='Zoid Letters').last()
    ryhms = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Ryhms').last()
    races = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Races').last()
    wock = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Wock').last()
    toybox = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Toybox').last()

    cognitive = Cognitive_assessment.objects.filter(appointment__child_id=5, test_name='acops').last()

    history = 'تبلغ ' + child.full_name + 'من العمر' + str(child.age_in_years) + 'سنة و' + str(child.age_in_months) + \
              'شهراً , وهي الإبنة '

    return render(request, 'pdfs/file1/acops.html', {'reading': reading, 'spelling': spelling, 'mobile': mobile,
                                                     'funny': funny, 'segment': segment,
                                                     'cave': cave, 'cognitive': cognitive, 'child': child,
                                                     'c': cc, 'appoint': appoint, 'a': a,
                                                     'rabbits': rabbits, 'zoid_friends': zoid_friends,
                                                     'zoid_letter_names': zoid_letter_names,
                                                     'zoid_letters': zoid_letters, 'ryhms': ryhms,
                                                     'races': races, 'wock': wock, 'toybox': toybox,
                                                     'history': history
                                                     })


def Child_Case_PDF(request, id):
    cc = Child_Case_Data.objects.get(child_id=id)
    appoint = Appointment.objects.filter(child_id=id).first()

    return render(request, 'pdfs/file1/page1.html', {'c': cc, 'appoint': appoint})


def Stanford_PDF(request, id):
    child = Person.objects.get(id=id)
    cc = Child_Case_Data.objects.get(child=child)
    a = Assessment_psy.objects.filter(appointment__child=child, test_name='standford').last()
    cognitive = Cognitive_assessment.objects.filter(appointment__child=child).last()
    return render(request, 'pdfs/file1/stanford.html', {'a': a, 'child': child, 'cognitive': cognitive, 'c': cc})


def Weksler_PDF(request, id):
    child = Person.objects.get(id=id)
    cc = Child_Case_Data.objects.get(child=child)
    a = Assessment_psy.objects.filter(appointment__child=child, test_name='weksler').last()
    cognitive = Cognitive_assessment.objects.filter(appointment__child=child).last()
    return render(request, 'pdfs/file1/weksler.html', {'a': a, 'child': child, 'cognitive': cognitive, 'c': cc})


def Secondary_PDF(request, id):
    child = Person.objects.get(id=id)
    cc = Child_Case_Data.objects.get(child=child)
    reading = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                            sub_test_name='Reading').last()
    spelling = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                             sub_test_name='Spelling').last()
    mobile = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                           sub_test_name='Mobile').last()
    single = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                           sub_test_name='Single Word Reading').last()
    funny = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                          sub_test_name='Funny Words').last()
    segment = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary',
                                            sub_test_name='Segment').last()
    cave = Assessment_psy.objects.filter(appointment__child=child, test_name='secondary', sub_test_name='Cave').last()
    cognitive = Cognitive_assessment.objects.filter(appointment__child=child, test_name='secondary').last()

    return render(request, 'pdfs/file1/secondary.html', {'reading': reading, 'spelling': spelling, 'mobile': mobile
        , 'single': single, 'funny': funny, 'segment': segment,
                                                         'cave': cave, 'cognitive': cognitive, 'child': child, 'c': cc})


def Junior_PDF(request, id):
    child = Person.objects.get(id=id)
    cc = Child_Case_Data.objects.get(child=child)
    reading = Assessment_psy.objects.filter(appointment__child=child, test_name='junior',
                                            sub_test_name='Reading').last()
    spelling = Assessment_psy.objects.filter(appointment__child=child, test_name='junior',
                                             sub_test_name='Spelling').last()
    mobile = Assessment_psy.objects.filter(appointment__child=child, test_name='junior', sub_test_name='Mobile').last()
    funny = Assessment_psy.objects.filter(appointment__child=child, test_name='junior',
                                          sub_test_name='Funny Words').last()
    segment = Assessment_psy.objects.filter(appointment__child=child, test_name='junior',
                                            sub_test_name='Segment').last()
    cave = Assessment_psy.objects.filter(appointment__child=child, test_name='junior', sub_test_name='Cave').last()

    cognitive = Cognitive_assessment.objects.filter(appointment__child=child, test_name='junior').last()

    return render(request, 'pdfs/file1/junior.html', {'reading': reading, 'spelling': spelling, 'mobile': mobile,
                                                      'funny': funny, 'segment': segment,
                                                      'cave': cave, 'cognitive': cognitive, 'child': child, 'c': cc})


def ACOPS_PDF(request, id):
    child = Person.objects.get(id=id)
    cc = Child_Case_Data.objects.get(child=child)
    rabbits = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Rabbits').last()
    zoid_friends = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                 sub_test_name='Zoid Friends').last()
    zoid_letter_names = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                      sub_test_name='Zoid Letter Names').last()
    zoid_letters = Assessment_psy.objects.filter(appointment__child=child, test_name='acops',
                                                 sub_test_name='Zoid Letters').last()
    ryhms = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Ryhms').last()
    races = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Races').last()
    wock = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Wock').last()
    toybox = Assessment_psy.objects.filter(appointment__child=child, test_name='acops', sub_test_name='Toybox').last()

    cognitive = Cognitive_assessment.objects.filter(appointment__child=child, test_name='acops').last()

    return render(request, 'pdfs/file1/acops.html', {'rabbits': rabbits, 'zoid_friends': zoid_friends,
                                                     'zoid_letter_names': zoid_letter_names,
                                                     'zoid_letters': zoid_letters, 'ryhms': ryhms,
                                                     'races': races, 'wock': wock, 'toybox': toybox,
                                                     'cognitive': cognitive, 'child': child, 'c': cc})


@login_required(login_url='login')
def view_tests(request, id):
    appointment = Appointment.objects.get(id=id)
    return render(request, 'tests/view_tests.html', {'appointment': appointment})


@login_required(login_url='login')
def rabbits(request, id):
    appointment = Appointment.objects.get(id=id)
    assessment = Assessment_psy.objects.filter(appointment_id=id, sub_test_name='Rabbits').last()
    if appointment.child.age_in_number < 7:
        below_age = True
    else:
        below_age = False

    if request.method == 'POST':
        comp_order1 = request.POST['comp_order1']
        player_order1 = request.POST['player_order1']
        start_time1 = request.POST['start_time1']
        end_time1 = request.POST['end_time1']

        # print(comp_order)
        # print(player_order)
        # diff = int(end_time) - int(start_time)

        # diff = diff / 1000
        #
        # print(f'{diff} seconds')
        # messages.success(request, message=request.POST)
        # print(request.POST)

        return redirect(rabbits, id)

    return render(request, 'tests/rabbits.html', {'appointment': appointment, 'assessment': assessment,
                                                  'below_age': below_age})


@login_required(login_url='login')
def toybox(request, id):
    appointment = Appointment.objects.get(id=id)
    assessment = Assessment_psy.objects.filter(appointment_id=id, sub_test_name='Rabbits').last()

    if appointment.child.age_in_number < 7:
        below_age = 1
    else:
        below_age = 0

    return render(request, 'tests/toybox.html', {'appointment': appointment, 'assessment': assessment,
                                                 'below_age': below_age})


@login_required(login_url='login')
def races(request, id):
    appointment = Appointment.objects.get(id=id)
    assessment = Assessment_psy.objects.filter(appointment_id=id, sub_test_name='Races').last()

    if appointment.child.age_in_number < 7:
        return render(request, 'tests/race(below7years).html', {'appointment': appointment, 'assessment': assessment})
    else:
        return render(request, 'tests/race(above7years).html', {'appointment': appointment, 'assessment': assessment})


@login_required(login_url='login')
def rhymes(request, id):
    appointment = Appointment.objects.get(id=id)
    assessment = Assessment_psy.objects.filter(appointment_id=id, sub_test_name='Rhymes').last()

    if appointment.child.age_in_number < 7:
        return render(request, 'tests/rhymes(below7years).html', {'appointment': appointment, 'assessment': assessment})
    else:
        return render(request, 'tests/rhymes(above7yearsTest1).html',
                      {'appointment': appointment, 'assessment': assessment})


@login_required(login_url='login')
def rhymes_above7_part2(request, id):
    appointment = Appointment.objects.get(id=id)
    assessment = Assessment_psy.objects.filter(appointment_id=id, sub_test_name='Rhymes').last()

    return render(request, 'tests/rhymes(above7yearsTest2).html', {'appointment': appointment, 'assessment': assessment})
