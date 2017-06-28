#-*- coding: utf-8 -*-
from openerp import models, fields, api, tools,osv
from openerp.tools.translate import _
class meeting_minutes(models.Model):
	_name = 'meeting.information'	
	_rec_name = 'meeting_purpose'
	_description = 'Information'
	state = fields.Selection([('create', 'Create'),('meeting', 'Meeting'),('minutes', 'Minutes'),],default='create')
	_inherit = 'mail.thread'
	#_inherits = {'meeting.venue': 'mod_id'}
	
	#_inherits = {'meeting.participant': 'part_id' ,'meeting.agenda': 'agenda_id'}

        meeting_date= fields.Date('Date',required =True)
        #meeting_time=fields.Time('Meeting Time', required=True)
        meeting_purpose= fields.Char('Purpose', size=64, required = True)
	meeting_moderator = fields.Char(related='meeting_moderator1.participant_name', required =True, string = 'moderator')
	meeting_moderator1 = fields.Many2one('meeting.participant',string = "Moderator")
        participant_ids=fields.One2many('meeting.participant','participant_id2',string = 'participant')
        contact_ids=fields.One2many('meeting.external','participant_id2',string = 'External Participant')
	agenda_ids = fields.One2many('meeting.agenda', 'agenda_no', string= "Agenda")
	venue_fk = fields.Many2one('meeting.venue',string = "Venue")	
	
        meeting_type= fields.Many2one('meeting.types','Types', required =True)

	discussion_id1 = fields.One2many('meeting.discussion', 'meeting_no', string= "Discussion")	
        attendance_id= fields.One2many('meeting.attendance', 'attendance_id1', string= "Attendance")
	decision_id = fields.One2many('meeting.decision', 'meeting_id', string= "Decision")
	assign_id = fields.One2many('meeting.assign', 'meeting_id', string= "Asigned To")
	@api.multi
	def concept_progressbar(self):
		self.ensure_one()
		self.write({'state': 'create',})



    
    #This function is triggered when the user clicks on the button 'In progress'
	@api.multi
	def progress_progressbar(self):
		self.ensure_one()
		self.write({'state': 'meeting'})

    #This function is triggered when the user clicks on the button 'Done'
	@api.multi
	def done_progressbar(self):
		self.ensure_one()
		self.write({'state': 'minutes',})
		# post_vars = {'subject': "Message subject",'body': "Message body",'partner_ids': [(4, 3)],} # Where "4" adds the ID to the list
                                       # of followers and "3" is the partner ID 
		#thread_pool = self.pool.get('mail.thread')
		#thread_pool.message_post(cr, uid, False,type="notification",subtype="mt_comment",context=context,**post_vars)

	@api.multi
	def add_agenda(self):
		self.ensure_one()
		self.write({'state': 'agenda',})

	def generate_msg(self,cr,uid,ids,context=None):
		return {'value':{},'warning':{'title':'warning','message':'Your message'}}

class meeting_venue(models.Model):
	_name = 'meeting.venue'
	_rec_name = 'venue_name'
	_description = 'Meeting Venue'
	venue_fks = fields.One2many('meeting.information','venue_fk',string = "Venue ids")
	venue_id=fields.Integer('Venue ID')
        venue_name= fields.Char('Venue', size=64)
        venue_address= fields.Char('Address',size=64)
	venue_remarks = fields.Text('Remarks')
	
class metingTypes(models.Model):
	_name='meeting.types'
	_rec_name = 'meeting_type'	
	meeting_type = fields.One2many('meeting.information', 'meeting_type', string= "Meeting")
	meeting_type = fields.Char('Meeting Types')



class Participant(models.Model):
	_name = 'meeting.participant'
	_rec_name = 'participant_name'
	#_inherit = 'meeting.attendance'
        participant_id2= fields.Many2one('meeting.information','Meeting')
        participant_mod=fields.One2many('meeting.information','meeting_moderator1',string = 'Moderator')

	contact_id = fields.Many2one('hr.employee',string = "Participant")
	
	attendance_id = fields.One2many('meeting.attendance', 'attendance_id', string= "Attendance")
	participant_name= fields.Char(related='contact_id.name')
        email_id=fields.Char(related='contact_id.work_email')
        department= fields.Char(related='contact_id.department_id.name')
        phone_number= fields.Char(related='contact_id.mobile_phone')

class ExternalParticipant(models.Model):
	_name = 'meeting.external'
	_rec_name = 'participant_name'
	# _inherit = 'meeting.attendance'
	participant_id2 = fields.Many2one('meeting.information', 'Meeting')

	# contact_id = fields.Many2one('res.partner',string = "Contacts")

	# attendance_id = fields.One2many('meeting.attendance', 'attendance_id2', string= "Attendance")
	# company_name =fields.Char(string = 'Company',related='contact_id.parent_name')
	# participant_name= fields.Char(related='contact_id.name')
	#    email_id=fields.Char(related='contact_id.email')
	#    phone_number= fields.Char(related='contact_id.mobile')
	# participant_name = fields.Char("Participant Name")
	designation = fields.Char(string="Designation",related='participant_name.function')
	company_name = fields.Char("Company Name")
	participant_name = fields.Many2one('res.partner',string="Participant Name", required=True)
	email_id = fields.Char("Email Address",related='participant_name.email')
	phone_number = fields.Char("Phone Number",related='participant_name.mobile')
	
class Agenda(models.Model):
	_name = 'meeting.agenda'
	_rec_name = 'agenda_name'
	agenda_no = fields.Many2one('meeting.information','Meeting')
        agenda_name= fields.Char('Agenda', size=64)
        agenda_owner= fields.Char('Owner', size=64)
	remarks= fields.Char('Remarks')
	discussion_id3 = fields.One2many('meeting.discussion', 'discussion_id1', string= "Discussion")
	decision_id = fields.One2many('meeting.decision', 'agenda_id', string= "Decision")


        
	
class Discussion(models.Model):
	_name = 'meeting.discussion'
	_rec_name = 'discussion_content'	
	discussion_id1 = fields.Many2one('meeting.agenda','Agenda')
	meeting_no = fields.Many2one('meeting.information','Meeting')
        discussion_content= fields.Char('Discussion')
        participant_id= fields.Char("Partcipant")

class attendance(models.Model):
	_name ='meeting.attendance'
        attendance_id= fields.Many2one('meeting.participant',string='Participant')
	part=fields.Many2one('meeting.participant',string='Participants',related='attendance_id.contact_id')
        attendance_id1= fields.Many2one('meeting.information','Meeting')
        attendance_id2= fields.Many2one('meeting.external','External Participant')
        attendance=fields.Boolean('Present/Absent',default = "True")

    #
    # @api.onchange('attendance_id1')
    # 	def onchange_attendance_id1(self):
    #     	self.part = False
    #
    # @api.model
    # 	def create(self, vals):
    #     	if vals.get('attendance_id1'):
    #        	 	project = self.env['meeting.information'].browse(vals.get('attendance_id1'))
    #         	vals['account_id'] = project.analytic_account_id.id
    #     		return super(attendance, self).create(vals)
    #
    # @api.multi
    # def write(self, vals):
    #     if vals.get('project_id'):
    #         project = self.env['meeting.information'].browse(vals.get('attendance_id1'))
    #         vals['account_id'] = project.analytic_account_id.id
    #     return super(attendance, self).write(vals)

class Decision(models.Model):
	_name='meeting.decision'
	_rec_name='decision_name'
	meeting_id = fields.Many2one('meeting.information','Meeting')
	agenda_id = fields.Many2one('meeting.agenda','Agenda')
	decision_name= fields.Char('Decision')
	decision_remarks=fields.Char('Remarks')
	asignee_id = fields.One2many('meeting.assign', 'decision_id', string= "Asigned To")

class AsignedTo(models.Model):
	_name= 'meeting.assign'
	_rec_name = 'name'
	decision_id = fields.Many2one('meeting.decision','Decision')
	meeting_id = fields.Many2one('meeting.information','Meeting')
	asigned_id = fields.Many2one('hr.employee', string = "Asigned to")
	name= fields.Char(related='asigned_id.name')
	email_id=fields.Char(related='asigned_id.work_email')
        department= fields.Char(related='asigned_id.department_id.name')
        phone_number= fields.Char(related='asigned_id.mobile_phone')

	


