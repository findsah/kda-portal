from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('', views.empty, name='empty'),
    path('index/', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('language-select/', views.language_choose, name='language-choose'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register-centre/', views.register_centre, name='register-centre'),
    path('receptionist/', views.receptionist_dashboard, name='receptionist'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('success/', views.success, name='success'),
    path('search_psychologist/', views.search_psy, name='search_psy'),
    path('availability/<int:id>/', views.availability, name='availability'),
    path('availability/<int:id>/edit/', views.availability_edit, name='availability_edit'),
    path('slots/<int:id1>/<int:id2>/<str:date>/', views.check_slots, name='check_slots'),
    path('create-slots/<int:id>/<int:weekday>/', views.create_slots),
    path('slots/<int:id1>/<int:id2>/<str:date>/<str:time_s>/confirm-appointment/', views.confirm_appointment, name='confirm-appointment'),
    path('delete-appointment/<int:id>/', views.delete_appointment, name='delete-appointment'),
    path('reschedule/<int:id>/', views.rescheudle, name='reschedule'),
    path('child-case-form/<int:id>/', views.child_case, name='child-case'),#
    path('cc-child-history/<int:id>/', views.cc_child_history, name='cc_child_history'),#
    path('cc-condition/<int:id>/', views.cc_condition, name='cc_condition'),#
    path('cc-stages-of-growth/<int:id>/', views.cc_stages_of_growth, name='cc_stages_of_growth'),#
    path('cc-family-history/<int:id>/', views.cc_family_history, name='cc_family_history'),#
    path('cc-social-development/<int:id>/', views.cc_social_development, name='cc_social_development'),#
    path('cc-child-behaviour/<int:id>/', views.cc_child_beh, name='cc_child-behaviour'),#
    path('cc-school-history/<int:id>/', views.cc_school_history, name='cc_school_history'),#
    path('cc-difficulties/<int:id>/', views.cc_diff_info, name='cc_difficulties'),#
    path('cc-other-info/<int:id>/', views.cc_other_info, name='cc_other_info'),#
    path('send_link/<int:id>/<str:language>/', views.send_link_form, name='send_link'),
    path('add-intervention/<int:id>/', views.add_intervention, name='add_intervention'),###
    path('check-intervention/<str:student_id>/<str:teacher_id>/', views.check_intervention, name='check_intervention'),#
    path('reschedule-intervention/<int:id>/', views.reschedule_session, name='re-session'),
    path('search-teacher/', views.search_teacher, name='search_teacher'),
    path('weekly-schedule/<int:student_id>/<int:teacher_id>/', views.weekly_grid, name='weekly'),#
    path('confirm-slot/<int:student_id>/<int:teacher_id>/<str:slot>/', views.confirm_slot, name="confirm-slot"),#
    path('search-intervention/', views.search_intervention, name='search-intervention'),
    path('view-intervention/<int:id>/', views.detail_intervention, name='detail-intervention'),
    path('delete-intervention/<int:id>/', views.delete_intervention, name='delete-intervention'),
    path('status-intervention/<int:id>/', views.status_intervention, name='status-intervention'),
    path('search-assessment/', views.search_assessment, name='search-assessment'),
    path('assess_tests/<int:id1>/<int:id2>/', views.assess_tests, name='assess_tests'),
    path('assessment/<int:id1>/<int:id2>/<str:test>/<str:subtest>/', views.assessment, name='assessment'),
    path('pre-performance-search-teacher/', views.search_teacher_pre, name='pre-evaluation-teacher'),
    path('pre-performance-search/<int:teacher_id>/', views.pre_evaluation_search, name='pre-eva-search'),#
    path('pre-performance-a/<int:id>/', views.pre_evaluation, name='pre-eva1'),
    path('pre-performance-e/<int:id>/', views.pre_evaluation_arabic, name='pre-eva2'),
    path('teacher-search-performance/', views.select_teacher_assess, name='teacher-search-evaluation'),
    path('performance-search/<int:teacher_id>/', views.session_evaluation_search, name='eva-search'),#
    path('performance/<int:id>/', views.session_evaluation, name='eva'),
    path('registration/student/', views.registration_student, name='registration_student'),
    path('edit/student/<int:id>/', views.edit_student, name='edit_student'),#
    path('todays-appointment-list/', views.todays_appoint_list, name='todays-appointment-list'),
    path('todays-session-list/', views.todays_intervention, name='today-intervention'),
    path('todays-status/<int:id>/<str:reason>/', views.todays_status, name='todays-status'),
    path('search-student/', views.search_student, name='search-student'),
    path('report-all-appointments/', views.report_all_appointments, name='report-all-appointments'),
    path('report-all-sessions/', views.report_all_sessions, name='report-all-sessions'),
    path('assessment-graphs/<int:id>/', views.assessment_graph, name='assessment-graph'),
    path('report-session/<int:teacher_id>/<int:student_id>/', views.report_session, name='report-session'),#
    path('pdf/', views.GeneratePDF.as_view()),
    path('session-report-english/<int:id>/', views.english_session_report, name='english-session-report'),
    path('session-report-arabic/<int:id>/', views.arabic_session_report, name='arabic-session-report'),
    path('select-psy/', views.select_psy, name='select-psy'),
    path('dashboard-psychologist/<int:psy_id>/', views.dashboard_psy, name='dashboard-psy'),#
    path('select-teacher/', views.select_teacher, name='select-teacher'),
    path('dashboard-teacher/<int:teacher_id>/', views.dashboard_teacher, name='dashboard-teacher'),#
    path('select-student/<str:fromm>/', views.select_student, name='select-student'),
    path('dashboard-student/<int:student_id>/', views.dashboard_student, name='dashboard-student'),#
    path('monitor-student-performance/<int:student_id>/<str:subj>/', views.monitor_performance, name='monitor-performance'),#
    path('select-parent/<int:student_id>/', views.assign_parent, name='assign_parent'),#
    path('add-parent/<int:student_id>/', views.add_parent, name='add_parent'),#
    path('status/<int:id>/', views.change_status_student, name='change_status_student'),
    path('select-teacher-s/<int:id>/', views.select_teacher_status_change, name='select_teacher_status_change'),
    path('registration-psy/', views.registration_psy, name='registration-psy'),
    path('change-password/<int:id>/', views.change_password, name='change-password'),
    path('list-tests/<int:id>', views.test_lists, name='list-tests'),
    path('registration-teacher/', views.registration_teacher, name='registration-teacher'),

    # path('download-child-case/<str:username>/', views.download_child_case.as_view(), name='download-child-case'),
    path('pdfs/', views.test_pdf),

    path('download-child-case/<int:id>/', views.Child_Case_PDF, name='download-child-case'),#
    path('download-stanford/<int:id>/', views.Stanford_PDF, name='download-stanford'),#
    path('download-secondary/<int:id>/', views.Secondary_PDF, name='download-secondary'),#
    path('download-junior/<int:id>/', views.Junior_PDF, name='download-junior'),#
    path('download-acops/<int:id>/', views.ACOPS_PDF, name='download-acops'),#
    path('download-weksler/<int:id>/', views.Weksler_PDF, name='download-weksler'),#

    path('view_tests/<int:id>/', views.view_tests, name='view_tests'),
    path('rabbits/<int:id>/', views.rabbits, name='rabbits'),
    path('toybox/<int:id>/', views.toybox, name='rabbits'),
    path('races/<int:id>/', views.races, name='races'),
    path('rhymes/<int:id>/', views.rhymes, name='rhymes'),
    path('rhymes2/<int:id>/', views.rhymes_above7_part2, name='rhymes2'),
]
