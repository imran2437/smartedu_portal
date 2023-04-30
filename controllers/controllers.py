# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
import logging
import json


class PartnerController(http.Controller):
    @http.route('/partner', type='http', auth='user')
    def partner_redirect(self, **kw):
        partner_type = request.env.user.partner_id.partner_type
        if partner_type == 'parent':
            return request.redirect('/my/admission/online/applications/parent')
        elif partner_type == 'student':
            return request.redirect('/my/admission/online/applications/student')
        else:
            return http.Response('Invalid partner type')


class MyPortalController(http.Controller):

    @http.route('/my/admission/online/applications/student', type='http', auth='user', website=True)
    def my_student_route(self, **kw):
        user = request.env.user
        information = http.request.env['se.student'].search(
            [('user_id', '=', user.id)], limit=1)
        return request.render("smartedu_portal.se_student_template", {
            'info': information,
        })

    @http.route('/my/admission/online/applications/list', type='http', auth='user', website=True)
    def my_student_admission_route(self, **kw):
        user = request.env.user
        applicant_info = http.request.env['se.application'].search(
            [('user_id', '=', user.id)], limit=1)
        return request.render("smartedu_portal.se_student_application_list", {
            'informations': applicant_info,

        })

    # @http.route('/my/admission/online/applications/list/form', type='http', auth='user', website=True)
    # def my_student_admission_form_route(self, **kw):
    #     user_id = request.env.context.get('uid')
    #     kw.update({"user_id": user_id})
    #     if request.httprequest.method == 'POST':

    #     # Handle update button click to update data
    #         student_id = int(kw.get('student_id'))
    #         student = request.env['se.application'].sudo().browse(
    #             student_id)
    #         student.update({
    #         'first_name': kw.get('first_name'),
    #         'email': kw.get('email'),
    #         'phone': kw.get('phone'),
    #     })
    #         return http.redirect_with_hash('/my/admission/online/applications/list/form')
    #     else:
    #     # Display form on initial GET request
    #        student_info = request.env['se.application'].search(
    #            [('user_id', '=', request.env.user.id)], limit=1)
    #        return request.render("smartedu_portal.se_student_admission_template", {
    #            'student_info': student_info,
    #        })

    @http.route('/my/admission/online/applications/list/form', auth='user', website=True)
    def update_form(self, **kw):
        user = request.env.user

        student_info = request.env['se.application'].sudo().search(
            [('user_id', '=', user.id)], limit=1)
        batch = request.env['se.batch'].sudo().search([])
        shift = request.env['se.education.shift'].sudo().search([])
        type = request.env['se.student.type'].sudo().search([])
        semester = request.env['se.semester'].sudo().search([])
        semester_type = request.env['se.semester.type'].sudo().search([])
        program = request.env['se.program'].sudo().search([])
        ssc = request.env['se.education.board'].sudo().search([])
        hsc = request.env['se.education.board'].sudo().search([])
        o_level = request.env['se.education.board'].sudo().search([])
        a_level = request.env['se.education.board'].sudo().search([])
        return request.render('smartedu_portal.se_student_admission_template', {
            # Relational Fields:

            "student_info": student_info,
            "batch": batch,
            "type": type,
            "shift": shift,
            "semester": semester,
            "semester_type": semester_type,
            "program": program,
            "ssc": ssc,
            "hsc": hsc,
            "o_level": o_level,
            "a_level": a_level,
        })

    @http.route('/my/admission/online/applications/update', auth='user', website=True)
    def update(self, **kw):
        user = request.env.user
        # get student info
        student_info = request.env['se.application'].sudo().search(
            [('user_id', '=', user.id)], limit=1)

        # update student info with new values
        student_info.first_name = kw["first_name"]
        student_info.middle_name = kw["middle_name"]
        student_info.last_name = kw["last_name"]
        student_info.student_id_text = kw["student_id_text"]

        # Update the many-to-one field (batch_id)
        batch_id = int(kw.get('batch_id', False))
        if batch_id:
            batch = request.env['se.batch'].sudo().browse(batch_id)
            student_info.batch_id = batch

        # Update the many-to-one field (student_type_id)
        student_type_id = int(kw.get('student_type_id', False))
        if student_type_id:
            student_type = request.env['se.student.type'].sudo().browse(
                student_type_id)
            student_info.student_type_id = student_type
    #  # Update the many-to-one field (semester_id)
        semester_id = int(kw.get('semester_id', False))
        if semester_id:
            semester_id = request.env['se.semester'].sudo().browse(
                semester_id)
            student_info.semester_id = semester_id

        # Update the many-to-one field (semester_type_id)
        semester_type_id = int(kw.get('semester_type_id', False))
        if semester_type_id:
            semester_type_id = request.env['se.semester.type'].sudo().browse(
                semester_type_id)
            student_info.semester_type_id = semester_type_id

        # Update the many-to-one field (education_shift_id)
        education_shift_id = int(kw.get('education_shift_id', False))
        if education_shift_id:
            education_shift_id = request.env['se.education.shift'].sudo().browse(
                education_shift_id)
            student_info.education_shift_id = education_shift_id

        # Update the many-to-one field (program_id)
        program_id = int(kw.get('program_id', False))
        if program_id:
            program_id = request.env['se.program'].sudo().browse(
                program_id)
            student_info.program_id = program_id

        student_info.application_serial_number = kw["application_serial_number"]
        student_info.application_number = kw["application_number"]
        student_info.application_date = kw["application_date"]
        student_info.admission_date = kw["admission_date"]
        student_info.admission_expire_date = kw["admission_expire_date"]
        student_info.curriculum_id = kw["curriculum_id"]
        student_info.fees = kw["fees"]
        student_info.admission_fee = kw["admission_fee"]
        # student_info.fees_term_id = kw["fees_term_id"]
        student_info.order_id = kw["order_id"]
        student_info.academic_faculty_id = kw["academic_faculty_id"]
        student_info.department_id = kw["department_id"]
        student_info.semester_year_string = kw["semester_year_string"]
        student_info.form_apply_type = kw["form_apply_type"]

        student_info.form_type = kw["form_type"]

        student_info.campus_type = kw["campus_type"]
        student_info.registration_number_ssc = kw["registration_number_ssc"]
        student_info.roll_number_ssc = kw["roll_number_ssc"]
        # student_info.education_board_ssc_id = kw["education_board_ssc_id"]

        # Update the many-to-one field (education_board_ssc_id)
        # education_board_ssc_id = int(kw.get('education_board_ssc_id', False))
        # if education_board_ssc_id:
        #     education_board_ssc_id = request.env['se.education.board'].sudo().browse(
        #     education_board_ssc_id)
        #     student_info.education_board_ssc_id = education_board_ssc_id

        student_info.year_ssc = kw["year_ssc"]
        student_info.ssc_gpa = kw["ssc_gpa"]
        student_info.ssc_certificate = kw["ssc_certificate"]
        student_info.registration_number_hsc = kw["registration_number_hsc"]
        student_info.roll_number_hsc = kw["roll_number_hsc"]
        # student_info.education_board_hsc_id = kw["education_board_hsc_id"]
        # Update the many-to-one field (education_board_hsc_id)
        # education_board_hsc_id = int(kw.get('education_board_hsc_id', False))
        # if education_board_hsc_id:
        #     education_board_hsc_id = request.env['se.education.board'].sudo().browse(
        #         education_board_hsc_id)
        #     student_info.education_board_hsc_id = education_board_hsc_id

        student_info.year_hsc = kw["year_hsc"]
        student_info.hsc_gpa = kw["hsc_gpa"]
        student_info.hsc_certificate = kw["hsc_certificate"]
        # student_info.education_board_o_level_id = kw["education_board_o_level_id"]
        # Update the many-to-one field (education_board_o_level_id)
        # education_board_o_level_id = int(kw.get('education_board_o_level_id', False))
        # if education_board_o_level_id:
        #     education_board_o_level_id = request.env['se.education.board'].sudo().browse(
        #         education_board_o_level_id)
        #     student_info.education_board_o_level_id = education_board_o_level_id

        student_info.a_level_certificate = kw["a_level_certificate"]
        student_info.o_level_certificate = kw["o_level_certificate"]
        student_info.passing_year_o_level = kw["passing_year_o_level"]
        # student_info.admission_board_result_o_level_ids = kw["admission_board_result_o_level_ids"]
        # student_info.education_board_a_level_id = kw["education_board_a_level_id"]
        # student_info.education_board_a_level_id = kw["education_board_a_level_id"]
        # Update the many-to-one field (education_board_a_level_id)
        # education_board_a_level_id = int(
        #     kw.get('education_board_a_level_id', False))
        # if education_board_a_level_id:
        #     education_board_a_level_id = request.env['se.education.board'].sudo().browse(
        #         education_board_a_level_id)
        #     student_info.education_board_a_level_id = education_board_a_level_id

        student_info.passing_year_a_level = kw["passing_year_a_level"]
        # student_info.admission_board_result_a_level_ids = kw["admission_board_result_a_level_ids"]
        student_info.gender = kw["gender"]
        student_info.marital_status = kw["marital_status"]
        student_info.religion = kw["religion"]
        student_info.blood_group = kw["blood_group"]
        student_info.email = kw["email"]
        student_info.phone = kw["phone"]
        student_info.emergency_contact_info = kw["emergency_contact_info"]
        student_info.street = kw["street"]
        student_info.zip = kw["zip"]
        student_info.permanent_district_id = kw["permanent_district_id"]
        student_info.country_id = kw["country_id"]
        student_info.present_street = kw["present_street"]
        student_info.present_zip = kw["present_zip"]
        student_info.present_district_id = kw["present_district_id"]
        student_info.present_country_id = kw["present_country_id"]
        # student_info.is_permanent_present_address_same = kw["is_permanent_present_address_same"]
        student_info.whatsapp_number = kw["whatsapp_number"]
        student_info.social_network = kw["social_network"]
        student_info.nationality = kw["nationality"]
        student_info.national_id_no = kw["national_id_no"]
        # student_info.passport_no = kw["passport_no"]
        student_info.visa_no = kw["visa_no"]

        student_info.visa_no = kw["visa_no"]
        student_info.visa_expire_date = kw["visa_expire_date"]
        student_info.father_name = kw["father_name"]
        student_info.father_contact_number = kw["father_contact_number"]
        student_info.father_email = kw["father_email"]
        student_info.father_national_id = kw["father_national_id"]
        student_info.father_passport = kw["father_passport"]
        student_info.father_birthday = kw["father_birthday"]
        student_info.father_age = kw["father_age"]
        student_info.father_occupation = kw["father_occupation"]
        student_info.father_designation = kw["father_designation"]
        student_info.father_annual_income = kw["father_annual_income"]
        student_info.mother_name = kw["mother_name"]
        student_info.mother_contact_number = kw["mother_contact_number"]
        student_info.mother_email = kw["mother_email"]
        student_info.mother_national_id = kw["mother_national_id"]
        student_info.mother_passport = kw["mother_passport"]
        student_info.mother_birthday = kw["mother_birthday"]
        student_info.mother_age = kw["mother_age"]
        student_info.mother_occupation = kw["mother_occupation"]
        student_info.mother_designation = kw["mother_designation"]
        student_info.local_guardian_name = kw["local_guardian_name"]
        student_info.local_guardian_email = kw["local_guardian_email"]
        student_info.local_guardian_contact_number = kw["local_guardian_contact_number"]
        student_info.local_guardian_national_id = kw["local_guardian_national_id"]
        student_info.local_guardian_passport = kw["local_guardian_passport"]
        student_info.local_guardian_relation = kw["local_guardian_relation"]
        student_info.local_guardian_street = kw["local_guardian_street"]
        student_info.local_guardian_zip = kw["local_guardian_zip"]
        student_info.local_guardian_state_id = kw["local_guardian_state_id"]
        student_info.local_guardian_country_id = kw["local_guardian_country_id"]

        # student_info.is_parents_freedom_fighter = kw["is_parents_freedom_fighter"]
        # student_info.is_tribal = kw["is_tribal"]
        # student_info.is_physical_disorder = kw["is_physical_disorder"]
        # student_info.is_first_division_player = kw["is_first_division_player"]
        student_info.write({
            'is_parents_freedom_fighter': kw.get('is_parents_freedom_fighter', False),
            'is_tribal': kw.get('is_tribal', False),
            'is_physical_disorder': kw.get('is_physical_disorder', False),
            'is_first_division_player': kw.get('is_first_division_player', False)
        })

        # student_info.know_the_diu_from_website = kw["know_the_diu_from_website"]
        # student_info.know_the_diu_from_newspaper = kw["know_the_diu_from_newspaper"]
        # student_info.know_the_diu_from_social_media = kw["know_the_diu_from_social_media"]
        # student_info.know_the_diu_from_sms = kw["know_the_diu_from_sms"]
        # student_info.know_the_diu_from_daffodil_family = kw["know_the_diu_from_daffodil_family"]
        # student_info.know_the_diu_from_diu_student = kw["know_the_diu_from_diu_student"]
        # student_info.know_the_diu_from_diu_employee = kw["know_the_diu_from_diu_employee"]
        # student_info.know_the_diu_from_others = kw["know_the_diu_from_others"]

        student_info.write({
            "is_parents_freedom_fighter": student_info.is_parents_freedom_fighter,
            "is_tribal": student_info.is_tribal,
            "is_physical_disorder": student_info.is_physical_disorder,
            "is_first_division_player": student_info.is_first_division_player,
            "know_the_diu_from_website": student_info.know_the_diu_from_website,
            "know_the_diu_from_newspaper": student_info.know_the_diu_from_newspaper,
            "know_the_diu_from_social_media": student_info.know_the_diu_from_social_media,
            "know_the_diu_from_sms": student_info.know_the_diu_from_sms,
            "know_the_diu_from_daffodil_family": student_info.know_the_diu_from_daffodil_family,
            "know_the_diu_from_diu_student": student_info.know_the_diu_from_diu_student,
            "know_the_diu_from_diu_employee": student_info.know_the_diu_from_diu_employee,
            "know_the_diu_from_others": student_info.know_the_diu_from_others,
        })

        return request.redirect('/my/admission/online/applications/list')


# Update

# @http.route('/my/admission/online/applications/update', auth='public', website=True)
# def update(self, **kw):
#     # Get the ID of the student application to be updated
#     student_id = int(kw.get('student_id'))

#     # Retrieve the student application record and update the fields
#     student = request.env['se.application'].sudo().browse(student_id)
#     student.first_name = kw.get('first_name', False)
#     student.middle_name = kw.get('middle_name', False)
#     student.last_name = kw.get('last_name', False)

#     # Update the many-to-one field (batch_id)
#     batch_id = int(kw.get('batch_id', False))
#     if batch_id:
#         batch = request.env['se.batch'].sudo().browse(batch_id)
#         student.batch_id = batch

#     # Update the selection field (student_type_id)
#     student_type_id = int(kw.get('student_type_id', False))
#     if student_type_id:
#         student_type = request.env['se.student.type'].sudo().browse(
#             student_type_id)
#         student.student_type_id = student_type

#     # Redirect to the updated student application record
#     return http.redirect_with_hash('/my/admission/online/applications/list/form#student_id=%d' % student_id)

# Create Data From Portal to Backend

    # @http.route('/create/applicant', type='http', auth='user', website=True)
    # def create_applicant(self, **kw):

    #     # set current user
    #     user_id = request.env.context.get('uid')
    #     kw.update({"user_id": user_id})

    #     # set student  id
    #     request.env['se.application'].sudo().search(
    #         [('user_id', '=', user_id)], limit=1)

    #     request.env['se.application'].sudo().create(kw)
    #     return request.render("smartedu_portal.applicant_thanks", {})

# class MyPortalControllerParent(http.Controller):

#     @http.route('/my/admission/online/applications/parent', type='http', auth='user', website=True)
#     def parent(self, **kw):
#         return request.render("smartedu_portal.se_parent_template", {})


class MyPortalControllerParent(http.Controller):

    @http.route('/my/admission/online/applications/parent', type='http', auth='user', website=True)
    def my_student_route(self, **kw):
        user = request.env.user
        information = http.request.env['se.student'].search(
            [('user_id', '=', user.id)], limit=1)
        return request.render("smartedu_portal.se_parent_template", {
            'info': information,
        })
