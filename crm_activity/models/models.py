from odoo import api, fields, models


class activity(models.Model):
    _inherit = 'crm.lead'

    state_sta = fields.Selection(string="State", selection=[('1', '1'), ('2', '2'), ], required=False, )
    submit_weekly_plan = fields.Boolean(string="Submit weekly plan", )
    customer_needs = fields.Text(string="Customer Needs", required=False, )
    meeting_type = fields.Selection(string="Meeting Type", selection=[('3', '3'), ('4', '4'), ], required=False, )
    competitors = fields.Text(string="Competitors", required=False, )
    does_the_client = fields.Boolean(string="Does the client hear about PrimeGear?", store=True)
    does_the_client_have = fields.Boolean(string="Does the client have Preventive maintenance devices?")
    primegear_courses = fields.Boolean(string="PrimeGear Courses", )
    stations = fields.Boolean(string="Stations / Equipment (Sales)", )
    conditional = fields.Boolean(string="Conditional Monitoring (ARMS)", )
    spareparts = fields.Boolean(string="Spareparts / Overhauls/Contract (After Market)", )
    company_profile = fields.Boolean(string="Show Company profile", )
    future_expansions = fields.Boolean(string="There are any future expansions ?", )
    problem_facing = fields.Text(string="Problems facing the customer", required=False, )
    machine_type = fields.Text(string="Machine Type", required=False, )
    machine_model = fields.Text(string="Machine Model", required=False, )
    manufacturer = fields.Text(string="Manufacturer", required=False, )
    production_year = fields.Text(string="Production Year", required=False, )
    Serial_Number = fields.Text(string="Serial Number", required=False, )
    notes_on_machine = fields.Text(string="Notes on Machine", required=False, )
