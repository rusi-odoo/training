from odoo import models, fields

class Certification(models.Model):
    _name = 'certification'
    _description = 'Certification'

    name = fields.Char(string='Certification Name', required=True)

class GFSIScheme(models.Model):
    _name = 'gfsi.scheme'
    _description = 'GFSI Scheme'

    name = fields.Char(string='Scheme Name', required=True)

class GFSIGrade(models.Model):
    _name = 'gfsi.grade'
    _description = 'GFSI Grade'

    name = fields.Char(string='Grade', required=True)
