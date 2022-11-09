from odoo import api, fields, models


class activity(models.Model):
    _inherit = 'crm.lead'

    state_sta = fields.Selection(string="State",
                                 selection=[('planned', 'Planned'), ('held', 'Held'), ('not held', ' Not Held')],
                                 required=False, )
    submit_weekly_plan = fields.Boolean(string="Submit weekly plan", )
    customer_needs = fields.Text(string="Customer Needs", required=False, )
    meeting_type = fields.Selection(string="Meeting Type", selection=[('knocking door', 'Knocking Door'),
                                                                      ('company introduction ', 'Company Introduction '),
                                                                      ('tender (check, buy)', 'Tender (Check, Buy)'),
                                                                      ('tender attending (technical, financial)', 'Tender attending (Technical, Financial)'),
                                                                      ('Follow up', 'Follow Up'),
                                                                      ('offer delivery', 'Offer Delivery'),
                                                                      ('Equipment delivery', 'Equipment Delivery'),
                                                                      ('check visit (overview)', 'Check Visit (overview)'),
                                                                      ], required=False, )
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
    machine_type = fields.Selection(string="Machine Type", selection=[('compressor', 'Compressor'), ('generator', 'Generator'), ('dryer', 'Dryer')],required=False, )
    machine_model = fields.Text(string="Machine Model", required=False, )
    manufacturer = fields.Text(string="Manufacturer", required=False, )
    production_year = fields.Text(string="Production Year", required=False, )
    Serial_Number = fields.Text(string="Serial Number", required=False, )
    notes_on_machine = fields.Text(string="Notes on Machine", required=False, )
    client_interested_in = fields.Boolean(string="Client Interested In",)
    interested_in = fields.Selection(string="Interested In", selection=[('prime gear courses', 'Prime Gear Courses'),
                                                   ('stations / equipment', 'Stations / Equipment'),
                                                   ('conditional monitoring', 'Conditional Monitoring (ARM)'),
                                                   ('spare parts overhauls contract', 'Spare parts / Overhauls/Contract'),], required=False, )

    Short_results = fields.Selection(string="Short Results", selection=[('client interested', 'Client Interested'),('new opportunity', 'New Opportunity'),
                                                   ('lost opportunity', 'Lost Opportunity'),
                                                   ('out of our scope', 'Out Of Our Scope'),
                                                   ('tender attended', 'Tender Attended'),
                                                   ('postponed', 'Postponed'),
                                                   ('tender specs doc bought', 'Tender Specs Doc Bought'),
                                                   ('quote Under Technical Study', 'Quote Under Technical Study'),
                                                   ('quote under financial study', 'Quote Under Financial Study'),
                                                   ], required=False, )
