 
Field	Description	Typically Editable?
Phone Number	Personal mobile number	✅ Yes
Email Address	Personal or official email	❌ Usually No
Address	Residential or permanent address	✅ Yes
Emergency Contact	Name and phone of emergency contact	✅ Yes
Blood Group	For medical/emergency records	✅ Yes
Profile Photo	Employee profile picture	✅ Yes (via upload)
Gender	Male/Female/Other	✅ Yes
Date of Birth	For age verification	❌ Usually No
Marital Status	Single, Married, etc.	✅ Yes
Languages Known	Languages employee can speak/write	✅ Yes
Bank Details	For salary credit (bank name, account)	✅ Yes (often limited to HR/finance verification)
PAN / Aadhaar	Identity documents	❌ Usually No (managed by HR)
 
 
Swapnil Rathore
Field  Description  Typically Editable?          Phone Number  Personal mobile number  ✅ Yes      Email Address  Personal or official email  ❌ Usually No      Address  Residential or permanent address  ✅ Yes      Emergency Contact  Name and phone of emergency contact  ✅ Yes      Blood Group
Prem Sagar Meda sir these are the fields of changes that user can do in employe chat profile 
 
Flow chart for org structure
User Clicks                         	Backend Action	                           Next Step Key
"org_structure"	                      Show main org menu	                        "org_menu"
"view_departments"	                    GET /departments                    	"show_departments"
"view_teams"	                            GET /teams	                           "show_teams"
"view_teams_by_department"	            Ask department	                      "select_department"
"Engineering" (department)        	GET /teams?department=...                      	"show_filtered_teams"
"view_hierarchy_by_manager"         	Ask manager                                    	"select_manager"
"John Doe" (manager)	             GET /hierarchy?manager=...	                        "show_filtered_hierarchy"
 
 
Flowchart for Leaves module 
selected_option	                                Backend Action	                           next (to frontend)
"apply_leave"	                                 Start flow, collect 4 fields	              "ask_leave_type"
"leave_balance"	                                         GET /balance	                   "show_leave_balance"
"leave_status"	                                          GET /status	                      "show_leave_status"
"cancel_leave"	                                 Start flow, ask leave ID	                 "ask_leave_id"
leave_type/date/...	Store step-by-step in session	next step of apply flow
 
 
EMPLOYEE MODULE MENU:

1. View All Employees

2. View Employee by ID

3. View Archived Employees

4. Restore Employee by ID


TIMESHEET MENU:

1. View All Timesheets

2. View Timesheet by Date Range

3. View Approved Timesheets

4. View Rejected Timesheets

5. Submit New Timesheet


CLOCK MENU:

1. Clock In

2. Clock Out

3. View My Clock Logs

4. View Today's Clock Status

5. View Clock Logs by Date Range


PAYROLL MENU:

1. View My Payslips

2. Download Payslip for a Specific Month

3. View Salary Breakdown


EXPENSES MENU:

1. View My Expense Claims

2. Submit a New Expense

3. View Pending Expenses

4. View Approved Expenses

5. View Rejected Expenses

 INSURANCE MENU:
1. View My Insurance Details
2. View My Family Members Covered
3. View Claims History
4. Download Policy Document


CLIENTS MENU:
1. View All Clients
2. Filter Clients by Status (Active/Inactive)
3. View Client Contact Details


TASKS MENU:
1. View All My Tasks
2. Filter Tasks by Status (Pending / In Progress / Completed)
3. View Task Details



PROJECTS MENU:
1. View All Projects
2. Filter Projects by Status (Active / Completed / On Hold)
3. View Project Details
