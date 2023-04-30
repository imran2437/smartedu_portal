# -*- coding: utf-8 -*-

from odoo import models, fields, api


class smartedu_portal(models.Model):
        _inherit = 'res.partner'
        
        
        partner_type = fields.Selection(
            string='Partner Type',
            selection=[('student', 'Student'), ('parent', 'Parent')]
        )
        


