import json
import os

intent_data = [
    # ─── Leave Policy (65 queries) ──────────────────────────────────
    {"id": "lp_001", "query": "How many days of Earned Leave do I receive per financial year?", "category": "Leave Policy"},
    {"id": "lp_002", "query": "What is the maximum limit of earned leave that can be carried forward?", "category": "Leave Policy"},
    {"id": "lp_003", "query": "How many casual and sick leaves are granted to employees each year?", "category": "Leave Policy"},
    {"id": "lp_004", "query": "What happens if my accumulated earned leave exceeds 45 days cap?", "category": "Leave Policy"},
    {"id": "lp_005", "query": "Is leave encashment permitted for unutilized earned leave?", "category": "Leave Policy"},
    {"id": "lp_006", "query": "How many weeks of paid maternity leave are female staff entitled to?", "category": "Leave Policy"},
    {"id": "lp_007", "query": "What is the paternity leave entitlement for new fathers at DSPAMC?", "category": "Leave Policy"},
    {"id": "lp_008", "query": "Can paternity leave be taken in multiple tranches within 6 months?", "category": "Leave Policy"},
    {"id": "lp_009", "query": "How many days of bereavement leave are provided in case of family loss?", "category": "Leave Policy"},
    {"id": "lp_010", "query": "What is the adoption leave policy for adopting a child?", "category": "Leave Policy"},
    {"id": "lp_011", "query": "How are earned leaves credited across the quarters in a financial year?", "category": "Leave Policy"},
    {"id": "lp_012", "query": "Can I apply for casual leave on PeoplePulse for half a day?", "category": "Leave Policy"},
    {"id": "lp_013", "query": "What notice period is required for taking more than 3 consecutive days of leave?", "category": "Leave Policy"},
    {"id": "lp_014", "query": "Where in the PeoplePulse HRMS portal do I submit my leave request?", "category": "Leave Policy"},
    {"id": "lp_015", "query": "Do I need to nominate a handover delegate when taking annual leave?", "category": "Leave Policy"},
    {"id": "lp_016", "query": "Are public holidays counted as part of earned leave duration?", "category": "Leave Policy"},
    {"id": "lp_017", "query": "How do I check my remaining sick leave quota for this year?", "category": "Leave Policy"},
    {"id": "lp_018", "query": "Is a medical certificate required when sick leave exceeds three days?", "category": "Leave Policy"},
    {"id": "lp_019", "query": "Can casual leave be combined with earned leave in a single application?", "category": "Leave Policy"},
    {"id": "lp_020", "query": "What is the policy on compensatory off for weekend operational support?", "category": "Leave Policy"},
    {"id": "lp_021", "query": "How does maternity benefit coverage apply to contract employees?", "category": "Leave Policy"},
    {"id": "lp_022", "query": "Can I cancel an approved leave application before the start date?", "category": "Leave Policy"},
    {"id": "lp_023", "query": "What is the procedure for extending my leave while traveling abroad?", "category": "Leave Policy"},
    {"id": "lp_024", "query": "Are new joinees entitled to earned leaves during their probation period?", "category": "Leave Policy"},
    {"id": "lp_025", "query": "Can I take unpaid leave of absence if I have zero leave balance?", "category": "Leave Policy"},
    {"id": "lp_026", "query": "What is the earned leave balance encashment calculation formula?", "category": "Leave Policy"},
    {"id": "lp_027", "query": "How many days in advance should I apply for a 2-week vacation?", "category": "Leave Policy"},
    {"id": "lp_028", "query": "Are Saturdays and Sundays excluded from casual leave deductions?", "category": "Leave Policy"},
    {"id": "lp_029", "query": "Can I take parental leave immediately following child adoption?", "category": "Leave Policy"},
    {"id": "lp_030", "query": "What is the policy for medical emergencies requiring extended leave?", "category": "Leave Policy"},
    {"id": "lp_031", "query": "How do I apply for maternity leave extension on PeoplePulse?", "category": "Leave Policy"},
    {"id": "lp_032", "query": "Can I encash my casual leave or sick leave balance at year end?", "category": "Leave Policy"},
    {"id": "lp_033", "query": "Do unused casual leaves carry forward to the next financial year?", "category": "Leave Policy"},
    {"id": "lp_034", "query": "What documentation is needed for bereavement leave verification?", "category": "Leave Policy"},
    {"id": "lp_035", "query": "Is sabbatical leave available for employees pursuing higher studies?", "category": "Leave Policy"},
    {"id": "lp_036", "query": "Can male employees take paternity leave prior to baby delivery date?", "category": "Leave Policy"},
    {"id": "lp_037", "query": "How does leave deduction work for unplanned emergency leaves?", "category": "Leave Policy"},
    {"id": "lp_038", "query": "Can I view my department's leave calendar to prevent handover conflicts?", "category": "Leave Policy"},
    {"id": "lp_039", "query": "What is the quarterly earned leave accrual schedule?", "category": "Leave Policy"},
    {"id": "lp_040", "query": "Are temporary interns entitled to paid annual leaves?", "category": "Leave Policy"},
    {"id": "lp_041", "query": "How do I convert a compensatory off into paid leave balance?", "category": "Leave Policy"},
    {"id": "lp_042", "query": "Can leave encashment be credited along with monthly payroll salary?", "category": "Leave Policy"},
    {"id": "lp_043", "query": "What are the rules regarding sandwich leaves over public holidays?", "category": "Leave Policy"},
    {"id": "lp_044", "query": "Does Maternity Benefit Act cover miscarriage recovery leaves?", "category": "Leave Policy"},
    {"id": "lp_045", "query": "How many days of special sick leave are granted for hospitalization?", "category": "Leave Policy"},
    {"id": "lp_046", "query": "Can I take 10 consecutive days of paternity leave in one stretch?", "category": "Leave Policy"},
    {"id": "lp_047", "query": "How do I edit my leave request after submitting on PeoplePulse?", "category": "Leave Policy"},
    {"id": "lp_048", "query": "Is there a restriction on taking earned leave in the first quarter of joining?", "category": "Leave Policy"},
    {"id": "lp_049", "query": "What is the policy for leave on account of voting or civic duties?", "category": "Leave Policy"},
    {"id": "lp_050", "query": "How do I notify HR if I fall ill while on annual earned vacation?", "category": "Leave Policy"},
    {"id": "lp_051", "query": "Can unapproved absence be regularized as casual leave retrospectively?", "category": "Leave Policy"},
    {"id": "lp_052", "query": "What is the maximum consecutive days of casual leave permitted?", "category": "Leave Policy"},
    {"id": "lp_053", "query": "Are earned leaves granted during statutory notice period before exit?", "category": "Leave Policy"},
    {"id": "lp_054", "query": "Who is eligible for 12 weeks of adoption leave at DSPAMC?", "category": "Leave Policy"},
    {"id": "lp_055", "query": "How to report sudden sick leave when unable to access corporate laptop?", "category": "Leave Policy"},
    {"id": "lp_056", "query": "Does maternity leave affect my annual bonus calculation?", "category": "Leave Policy"},
    {"id": "lp_057", "query": "Can paternity leave be claimed if the child is born outside India?", "category": "Leave Policy"},
    {"id": "lp_058", "query": "What is the carry forward limit for casual leave at financial year end?", "category": "Leave Policy"},
    {"id": "lp_059", "query": "How many days per quarter do full-time employees accumulate earned leave?", "category": "Leave Policy"},
    {"id": "lp_060", "query": "Can I encash all 45 days of my carried forward earned leave?", "category": "Leave Policy"},
    {"id": "lp_061", "query": "How does compensatory off expiration work if not utilized within 60 days?", "category": "Leave Policy"},
    {"id": "lp_062", "query": "What happens if an employee falls sick during official business travel?", "category": "Leave Policy"},
    {"id": "lp_063", "query": "Can both parents working at DSPAMC claim full parental leaves?", "category": "Leave Policy"},
    {"id": "lp_064", "query": "How do I check my historic leave records on PeoplePulse HRMS?", "category": "Leave Policy"},
    {"id": "lp_065", "query": "Is earned leave encashment subject to income tax deduction at source?", "category": "Leave Policy"},

    # ─── Reimbursement (65 queries) ──────────────────────────────────
    {"id": "rb_001", "query": "How do I submit an expense reimbursement claim via SAP Concur?", "category": "Reimbursement"},
    {"id": "rb_002", "query": "What is the submission deadline for filing travel expense claims?", "category": "Reimbursement"},
    {"id": "rb_003", "query": "What is the daily per diem meal allowance rate for Tier-1 cities?", "category": "Reimbursement"},
    {"id": "rb_004", "query": "What is the hotel accommodation cap per night in Mumbai and Delhi?", "category": "Reimbursement"},
    {"id": "rb_005", "query": "What is the accommodation allowance for non-metro cities like Pune or Jaipur?", "category": "Reimbursement"},
    {"id": "rb_006", "query": "Can I claim travel expenses if I submit my claim 40 days after the trip?", "category": "Reimbursement"},
    {"id": "rb_007", "query": "Why does my expense claim require an itemized GST tax invoice?", "category": "Reimbursement"},
    {"id": "rb_008", "query": "Can credit card charge slips be used instead of GST invoices for Concur claims?", "category": "Reimbursement"},
    {"id": "rb_009", "query": "How long does the finance team take to process NEFT reimbursement credit?", "category": "Reimbursement"},
    {"id": "rb_010", "query": "Can an employee book business class flights for domestic corporate travel?", "category": "Reimbursement"},
    {"id": "rb_011", "query": "What flight travel class is authorized for Associate Vice Presidents?", "category": "Reimbursement"},
    {"id": "rb_012", "query": "How do I claim reimbursement for client entertainment and business lunch?", "category": "Reimbursement"},
    {"id": "rb_013", "query": "Are local cab and Uber fares reimbursable for official client visits?", "category": "Reimbursement"},
    {"id": "rb_014", "query": "How do I upload receipts using the SAP Concur mobile application?", "category": "Reimbursement"},
    {"id": "rb_015", "query": "Is CFO approval mandatory for claims submitted after 45 calendar days?", "category": "Reimbursement"},
    {"id": "rb_016", "query": "Can I claim mileage allowance for using my personal car for official duties?", "category": "Reimbursement"},
    {"id": "rb_017", "query": "What is the monthly mobile bill reimbursement limit for relationship managers?", "category": "Reimbursement"},
    {"id": "rb_018", "query": "How do I get reimbursement for home internet broadband during hybrid work?", "category": "Reimbursement"},
    {"id": "rb_019", "query": "What happens if my travel expense report is rejected by the accounts department?", "category": "Reimbursement"},
    {"id": "rb_020", "query": "Can I claim airport parking fees as part of official travel expenses?", "category": "Reimbursement"},
    {"id": "rb_021", "query": "Are laundry charges reimbursable on official business trips lasting over 7 days?", "category": "Reimbursement"},
    {"id": "rb_022", "query": "How do I enter foreign currency expenditures into the SAP Concur platform?", "category": "Reimbursement"},
    {"id": "rb_023", "query": "Is toll tax reimbursement covered on intercity client road trips?", "category": "Reimbursement"},
    {"id": "rb_024", "query": "Can I claim reimbursement for books and professional financial journals?", "category": "Reimbursement"},
    {"id": "rb_025", "query": "How do I submit claims for NISM certification exam fee reimbursement?", "category": "Reimbursement"},
    {"id": "rb_026", "query": "What GST number must be displayed on hotel and flight tax invoices?", "category": "Reimbursement"},
    {"id": "rb_027", "query": "What is the per diem subsistence allowance when meals are provided by hosts?", "category": "Reimbursement"},
    {"id": "rb_028", "query": "Can I split a group dinner bill among colleagues in SAP Concur?", "category": "Reimbursement"},
    {"id": "rb_029", "query": "How do I submit an out-of-pocket cash expense report without digital receipts?", "category": "Reimbursement"},
    {"id": "rb_030", "query": "What is the maximum petty cash reimbursement limit without manager pre-approval?", "category": "Reimbursement"},
    {"id": "rb_031", "query": "Are airline cancellation fees refundable if official trip is rescheduled by management?", "category": "Reimbursement"},
    {"id": "rb_032", "query": "How do I track the disbursement status of my approved Concur claim?", "category": "Reimbursement"},
    {"id": "rb_033", "query": "Can I claim relocation moving expenses when transferring between DSP branches?", "category": "Reimbursement"},
    {"id": "rb_034", "query": "What supporting documents are needed for client gift reimbursement?", "category": "Reimbursement"},
    {"id": "rb_035", "query": "Are alcoholic beverages eligible for corporate reimbursement on client dinners?", "category": "Reimbursement"},
    {"id": "rb_036", "query": "How do I request an advance cash float for upcoming international business travel?", "category": "Reimbursement"},
    {"id": "rb_037", "query": "What is the per kilometer fuel reimbursement rate for two-wheelers?", "category": "Reimbursement"},
    {"id": "rb_038", "query": "Can visa application and passport renewal charges be claimed as business expenses?", "category": "Reimbursement"},
    {"id": "rb_039", "query": "How do I submit a corrected expense voucher if finance asked for clarification?", "category": "Reimbursement"},
    {"id": "rb_040", "query": "What is the tier classification for Bengaluru and Hyderabad for hotel caps?", "category": "Reimbursement"},
    {"id": "rb_041", "query": "Can I claim dental treatment bills under corporate mediclaim reimbursement?", "category": "Reimbursement"},
    {"id": "rb_042", "query": "What is the daily per diem incidental rate when traveling to Tier-2 cities?", "category": "Reimbursement"},
    {"id": "rb_043", "query": "Does corporate travel insurance reimburse lost luggage during company trips?", "category": "Reimbursement"},
    {"id": "rb_044", "query": "How do I link corporate credit card transactions directly into SAP Concur?", "category": "Reimbursement"},
    {"id": "rb_045", "query": "Are conference registration and delegate seminar fees 100% reimbursed?", "category": "Reimbursement"},
    {"id": "rb_046", "query": "Can tips and gratuity given to hotel staff be claimed in per diem expenses?", "category": "Reimbursement"},
    {"id": "rb_047", "query": "How do I bill excess airline baggage charges for marketing collateral transport?", "category": "Reimbursement"},
    {"id": "rb_048", "query": "What is the reimbursement policy for home office ergonomic chair purchase?", "category": "Reimbursement"},
    {"id": "rb_049", "query": "Can train tickets under Tatkal quota be reimbursed for urgent site visits?", "category": "Reimbursement"},
    {"id": "rb_050", "query": "What is the procedure to clear an unspent corporate travel cash advance?", "category": "Reimbursement"},
    {"id": "rb_051", "query": "Why was my food bill rejected due to missing vendor GSTIN details?", "category": "Reimbursement"},
    {"id": "rb_052", "query": "How do I claim reimbursement for professional annual CFA or CA membership dues?", "category": "Reimbursement"},
    {"id": "rb_053", "query": "What is the allowed taxi fare limit between Mumbai Airport and BKC office?", "category": "Reimbursement"},
    {"id": "rb_054", "query": "Are flight seat selection and fast-track check-in fees eligible for reimbursement?", "category": "Reimbursement"},
    {"id": "rb_055", "query": "How many days does accounts take to verify tax codes after manager approval?", "category": "Reimbursement"},
    {"id": "rb_056", "query": "What should I do if a vendor does not issue a GST invoice for small meal expenses?", "category": "Reimbursement"},
    {"id": "rb_057", "query": "Can an employee claim optical eye checkup glasses under health reimbursement?", "category": "Reimbursement"},
    {"id": "rb_058", "query": "What is the per diem reimbursement limit for overseas business trips to Singapore?", "category": "Reimbursement"},
    {"id": "rb_059", "query": "How to settle corporate card balances before monthly salary deduction?", "category": "Reimbursement"},
    {"id": "rb_060", "query": "Can I claim taxi reimbursement if I work late past 21:00 IST in the BKC office?", "category": "Reimbursement"},
    {"id": "rb_061", "query": "What is the escalation contact if an expense claim is stuck in finance queue?", "category": "Reimbursement"},
    {"id": "rb_062", "query": "Can team celebration dinner costs be charged to departmental budget in Concur?", "category": "Reimbursement"},
    {"id": "rb_063", "query": "Are roaming mobile packs reimbursable during overseas investor meetings?", "category": "Reimbursement"},
    {"id": "rb_064", "query": "How do I upload scanned PDF invoices in the Concur expense module?", "category": "Reimbursement"},
    {"id": "rb_065", "query": "What happens if a reimbursement claim is submitted after the 45-day deadline?", "category": "Reimbursement"},

    # ─── Approval Workflow (65 queries) ──────────────────────────────
    {"id": "aw_001", "query": "What is the reporting manager SLA to approve or reject a leave application?", "category": "Approval Workflow"},
    {"id": "aw_002", "query": "After how many hours does an unapproved leave request auto-escalate to HOD?", "category": "Approval Workflow"},
    {"id": "aw_003", "query": "Who is required to approve leave requests exceeding 5 consecutive days?", "category": "Approval Workflow"},
    {"id": "aw_004", "query": "What is the approval workflow for Bloomberg Terminal software access requests?", "category": "Approval Workflow"},
    {"id": "aw_005", "query": "How long does InfoSec compliance validation take after manager signoff?", "category": "Approval Workflow"},
    {"id": "aw_006", "query": "What is the validity period of personal trading pre-clearance approvals?", "category": "Approval Workflow"},
    {"id": "aw_007", "query": "Who needs to approve expense reimbursement claims before accounts verification?", "category": "Approval Workflow"},
    {"id": "aw_008", "query": "What is the approval chain for expense claims exceeding 1 lakh rupees?", "category": "Approval Workflow"},
    {"id": "aw_009", "query": "Can a reporting manager delegate approval authority during vacation absence?", "category": "Approval Workflow"},
    {"id": "aw_010", "query": "How do I assign an interim approval proxy on the PeoplePulse HRMS portal?", "category": "Approval Workflow"},
    {"id": "aw_011", "query": "What happens if my manager fails to approve my leave within 48 hours?", "category": "Approval Workflow"},
    {"id": "aw_012", "query": "Who is the final signoff authority for overseas business travel bookings?", "category": "Approval Workflow"},
    {"id": "aw_013", "query": "What is the workflow for requesting elevated database write permissions?", "category": "Approval Workflow"},
    {"id": "aw_014", "query": "Can an employee recall an approval request that was sent by mistake?", "category": "Approval Workflow"},
    {"id": "aw_015", "query": "Who signs off on new hire probation confirmation reviews?", "category": "Approval Workflow"},
    {"id": "aw_016", "query": "What is the escalation hierarchy if my ServiceHub IT ticket is stalled?", "category": "Approval Workflow"},
    {"id": "aw_017", "query": "Does personal trading in mutual funds require pre-clearance workflow?", "category": "Approval Workflow"},
    {"id": "aw_018", "query": "Who approves exceptions to the standard travel hotel accommodation limit?", "category": "Approval Workflow"},
    {"id": "aw_019", "query": "What is the dual signoff requirement for daily mutual fund NAV dissemination?", "category": "Approval Workflow"},
    {"id": "aw_020", "query": "Who must approve corporate credit card issuance for senior team members?", "category": "Approval Workflow"},
    {"id": "aw_021", "query": "What is the multi-level signoff required for client fee discount waivers?", "category": "Approval Workflow"},
    {"id": "aw_022", "query": "How do I check whose approval queue my expense voucher is currently resting in?", "category": "Approval Workflow"},
    {"id": "aw_023", "query": "Can an employee approve their own petty cash reimbursement voucher?", "category": "Approval Workflow"},
    {"id": "aw_024", "query": "What approval is required for booking client hospitality tickets for sporting events?", "category": "Approval Workflow"},
    {"id": "aw_025", "query": "Who authorizes access to the Qdrant vector database and analytical PostgreSQL?", "category": "Approval Workflow"},
    {"id": "aw_026", "query": "What is the turnaround time for ComplianceDesk trade approval requests?", "category": "Approval Workflow"},
    {"id": "aw_027", "query": "Can a department head override a manager rejection for leave application?", "category": "Approval Workflow"},
    {"id": "aw_028", "query": "Who needs to approve hardware replacement for damaged corporate laptops?", "category": "Approval Workflow"},
    {"id": "aw_029", "query": "What is the signoff process for publishing equity research reports to clients?", "category": "Approval Workflow"},
    {"id": "aw_030", "query": "Who approves remote access VPN tokens for third-party external vendors?", "category": "Approval Workflow"},
    {"id": "aw_031", "query": "How are approval notifications sent to managers when a request is submitted?", "category": "Approval Workflow"},
    {"id": "aw_032", "query": "What is the escalation path if the Chief Compliance Officer is unavailable?", "category": "Approval Workflow"},
    {"id": "aw_033", "query": "Who authorizes salary advance loans for full-time permanent employees?", "category": "Approval Workflow"},
    {"id": "aw_034", "query": "What is the approval matrix for procurement vendor purchase orders?", "category": "Approval Workflow"},
    {"id": "aw_035", "query": "Can an approval request be resubmitted after manager rejection with remarks?", "category": "Approval Workflow"},
    {"id": "aw_036", "query": "Who must approve internal job transfers between Mumbai and Delhi branches?", "category": "Approval Workflow"},
    {"id": "aw_037", "query": "What is the approval procedure for attending overseas investor conferences?", "category": "Approval Workflow"},
    {"id": "aw_038", "query": "Does maternity leave application require HR Head approval in addition to manager?", "category": "Approval Workflow"},
    {"id": "aw_039", "query": "What is the signoff workflow for onboarding new distribution partners?", "category": "Approval Workflow"},
    {"id": "aw_040", "query": "Who validates tax withholding exemptions on reimbursement vouchers?", "category": "Approval Workflow"},
    {"id": "aw_041", "query": "How do I trigger an expedited approval for emergency medical leave?", "category": "Approval Workflow"},
    {"id": "aw_042", "query": "Who signs off on the final settlement release during employee exit?", "category": "Approval Workflow"},
    {"id": "aw_043", "query": "What is the approval SLA for IT hardware asset provisioning?", "category": "Approval Workflow"},
    {"id": "aw_044", "query": "Can my skip-level manager approve my expense report directly in Concur?", "category": "Approval Workflow"},
    {"id": "aw_045", "query": "What is the workflow for requesting an exemption from mandatory office days?", "category": "Approval Workflow"},
    {"id": "aw_046", "query": "Who must approve marketing brochure content prior to public release?", "category": "Approval Workflow"},
    {"id": "aw_047", "query": "What approval is required before publishing research analyst blogs online?", "category": "Approval Workflow"},
    {"id": "aw_048", "query": "Who authorizes firewall rule exceptions for cloud infrastructure connections?", "category": "Approval Workflow"},
    {"id": "aw_049", "query": "What is the approval chain for high-value capital expenditure requests?", "category": "Approval Workflow"},
    {"id": "aw_050", "query": "Can managers set up automated out-of-office delegation rules in PeoplePulse?", "category": "Approval Workflow"},
    {"id": "aw_051", "query": "What happens if a trade pre-clearance request expires after 48 hours?", "category": "Approval Workflow"},
    {"id": "aw_052", "query": "Who approves budget allocation for annual team offsite meetings?", "category": "Approval Workflow"},
    {"id": "aw_053", "query": "What is the signoff hierarchy for approving new vendor contract terms?", "category": "Approval Workflow"},
    {"id": "aw_054", "query": "How do I verify if my manager has approved my leave on PeoplePulse?", "category": "Approval Workflow"},
    {"id": "aw_055", "query": "Who is authorized to approve late submission of travel expense reports?", "category": "Approval Workflow"},
    {"id": "aw_056", "query": "What approval is needed to access sensitive client portfolio holdings?", "category": "Approval Workflow"},
    {"id": "aw_057", "query": "Does unpaid leave of absence require Human Resources Director signoff?", "category": "Approval Workflow"},
    {"id": "aw_058", "query": "What is the process to expedite an urgent IT access request in ServiceHub?", "category": "Approval Workflow"},
    {"id": "aw_059", "query": "Who approves employee relocation allowance disbursements?", "category": "Approval Workflow"},
    {"id": "aw_060", "query": "Can an employee see rejection comments from accounts in SAP Concur?", "category": "Approval Workflow"},
    {"id": "aw_061", "query": "Who has the authority to revoke previously granted IT application access?", "category": "Approval Workflow"},
    {"id": "aw_062", "query": "What is the approval cycle for annual compensation reviews and increments?", "category": "Approval Workflow"},
    {"id": "aw_063", "query": "Who verifies employee medical certificates when sick leave exceeds 3 days?", "category": "Approval Workflow"},
    {"id": "aw_064", "query": "What is the approval procedure to obtain an official company credit card?", "category": "Approval Workflow"},
    {"id": "aw_065", "query": "How do I escalate an unapproved trade pre-clearance application?", "category": "Approval Workflow"},

    # ─── Employment Policy (65 queries) ──────────────────────────────
    {"id": "ep_001", "query": "Where do new joiners report on Day 1 for corporate induction at DSPAMC?", "category": "Employment Policy"},
    {"id": "ep_002", "query": "What time does Day 1 new hire orientation start at One BKC Mumbai?", "category": "Employment Policy"},
    {"id": "ep_003", "query": "What is the deadline for completing mandatory NISM regulatory certifications?", "category": "Employment Policy"},
    {"id": "ep_004", "query": "Which NISM certification is required for Wealth Advisors and Sales team?", "category": "Employment Policy"},
    {"id": "ep_005", "query": "Which NISM exam is mandated for Equity Analysts and Research Associates?", "category": "Employment Policy"},
    {"id": "ep_006", "query": "What is the minimum mandatory holding period for personal securities trades?", "category": "Employment Policy"},
    {"id": "ep_007", "query": "Are employees allowed to engage in intraday or day trading activities?", "category": "Employment Policy"},
    {"id": "ep_008", "query": "What is the DSP Restricted List or Grey List for securities transactions?", "category": "Employment Policy"},
    {"id": "ep_009", "query": "What are the rules regarding Chinese Walls and handling UPSI information?", "category": "Employment Policy"},
    {"id": "ep_010", "query": "What statutory forms must be submitted within 30 days of joining DSPAMC?", "category": "Employment Policy"},
    {"id": "ep_011", "query": "Where do new hires submit PF Form 11 and Gratuity nomination Form F?", "category": "Employment Policy"},
    {"id": "ep_012", "query": "What is the remote VPN connection requirement using Cisco AnyConnect?", "category": "Employment Policy"},
    {"id": "ep_013", "query": "Why are dealers and fund managers required to use YubiKey security keys?", "category": "Employment Policy"},
    {"id": "ep_014", "query": "What is the enterprise password complexity standard and expiration policy?", "category": "Employment Policy"},
    {"id": "ep_015", "query": "How many characters minimum must corporate passwords contain at DSPAMC?", "category": "Employment Policy"},
    {"id": "ep_016", "query": "What is the official policy regarding outside directorships and commercial work?", "category": "Employment Policy"},
    {"id": "ep_017", "query": "What is the standard notice period for confirmed permanent employees resigning?", "category": "Employment Policy"},
    {"id": "ep_018", "query": "How long is the probationary period for newly hired full-time staff?", "category": "Employment Policy"},
    {"id": "ep_019", "query": "What is the policy regarding gifts and hospitality received from brokers?", "category": "Employment Policy"},
    {"id": "ep_020", "query": "What are the core working hours and attendance expectations at DSPAMC?", "category": "Employment Policy"},
    {"id": "ep_021", "query": "What is the disciplinary procedure for unauthorized leak of price sensitive info?", "category": "Employment Policy"},
    {"id": "ep_022", "query": "How does DSPAMC handle background verification and reference checks?", "category": "Employment Policy"},
    {"id": "ep_023", "query": "What is the policy for enrolling dependents into the corporate mediclaim policy?", "category": "Employment Policy"},
    {"id": "ep_024", "query": "Can employees trade in IPO shares without prior compliance clearance?", "category": "Employment Policy"},
    {"id": "ep_025", "query": "What is the dress code policy for employees working in corporate offices?", "category": "Employment Policy"},
    {"id": "ep_026", "query": "What are the anti-harassment and POSH compliance policies at DSPAMC?", "category": "Employment Policy"},
    {"id": "ep_027", "query": "How is employee intellectual property handled for software written on company time?", "category": "Employment Policy"},
    {"id": "ep_028", "query": "Are personal social media posts discussing market views permitted under SEBI code?", "category": "Employment Policy"},
    {"id": "ep_029", "query": "What are the guidelines for handling confidential client investment records?", "category": "Employment Policy"},
    {"id": "ep_030", "query": "How does the Peer Buddy program work during the first week of onboarding?", "category": "Employment Policy"},
    {"id": "ep_031", "query": "What is the policy regarding smoking and substance use on company premises?", "category": "Employment Policy"},
    {"id": "ep_032", "query": "What happens if an employee fails to clear their NISM exam within 60 days?", "category": "Employment Policy"},
    {"id": "ep_033", "query": "Are employees required to declare all personal Demat accounts to compliance?", "category": "Employment Policy"},
    {"id": "ep_034", "query": "What is the whistleblower protection mechanism for reporting malpractices?", "category": "Employment Policy"},
    {"id": "ep_035", "query": "How do employees schedule their 30-day milestone check-in with their HRBP?", "category": "Employment Policy"},
    {"id": "ep_036", "query": "What are the regulations on employee personal borrowings from clients or brokers?", "category": "Employment Policy"},
    {"id": "ep_037", "query": "Is moonlighting or secondary employment allowed for DSPAMC employees?", "category": "Employment Policy"},
    {"id": "ep_038", "query": "What is the clean desk policy regarding unattended papers and trade notes?", "category": "Employment Policy"},
    {"id": "ep_039", "query": "How are security access badges and identity cards issued during Day 1 induction?", "category": "Employment Policy"},
    {"id": "ep_040", "query": "What is the policy for personal mobile phone usage on live trading desks?", "category": "Employment Policy"},
    {"id": "ep_041", "query": "Can an employee trade in derivative futures and options on their personal account?", "category": "Employment Policy"},
    {"id": "ep_042", "query": "What is the policy on corporate email monitoring and privacy expectations?", "category": "Employment Policy"},
    {"id": "ep_043", "query": "How do employees disclose potential conflicts of interest with vendors?", "category": "Employment Policy"},
    {"id": "ep_044", "query": "What happens during the probation review meeting after 6 months of service?", "category": "Employment Policy"},
    {"id": "ep_045", "query": "What is the policy for taking company laptops and devices when traveling abroad?", "category": "Employment Policy"},
    {"id": "ep_046", "query": "Are family members' brokerage trading accounts subject to SEBI compliance rules?", "category": "Employment Policy"},
    {"id": "ep_047", "query": "What is the annual mandatory compliance attestation requirement?", "category": "Employment Policy"},
    {"id": "ep_048", "query": "How does DSPAMC handle employee exit interviews and knowledge handover?", "category": "Employment Policy"},
    {"id": "ep_049", "query": "What are the guidelines for communicating with media and financial journalists?", "category": "Employment Policy"},
    {"id": "ep_050", "query": "Is participation in political campaign activities restricted under company code?", "category": "Employment Policy"},
    {"id": "ep_051", "query": "What is the procedure for returning IT assets upon resigning from the company?", "category": "Employment Policy"},
    {"id": "ep_052", "query": "What is the policy for employee mental wellness and counseling support programs?", "category": "Employment Policy"},
    {"id": "ep_053", "query": "Are employees allowed to accept board positions in non-profit charitable trusts?", "category": "Employment Policy"},
    {"id": "ep_054", "query": "What are the health and safety emergency protocols at One BKC headquarters?", "category": "Employment Policy"},
    {"id": "ep_055", "query": "How often must Microsoft Authenticator MFA sessions be re-authenticated?", "category": "Employment Policy"},
    {"id": "ep_056", "query": "What constitutes Unpublished Price Sensitive Information under SEBI regulations?", "category": "Employment Policy"},
    {"id": "ep_057", "query": "What is the policy regarding personal social gatherings and code of conduct?", "category": "Employment Policy"},
    {"id": "ep_058", "query": "How are employee grievances escalated to the internal ombudsman?", "category": "Employment Policy"},
    {"id": "ep_059", "query": "What is the procedure for updating permanent residential address in HR records?", "category": "Employment Policy"},
    {"id": "ep_060", "query": "Can an employee open a new bank account for salary credit without HR approval?", "category": "Employment Policy"},
    {"id": "ep_061", "query": "What is the consequence of violating the 30-day minimum stock holding rule?", "category": "Employment Policy"},
    {"id": "ep_062", "query": "What is the policy on retaining client communication and chat transcripts?", "category": "Employment Policy"},
    {"id": "ep_063", "query": "How does DSPAMC ensure equal opportunity and non-discrimination in hiring?", "category": "Employment Policy"},
    {"id": "ep_064", "query": "What are the statutory guidelines governing gratuity eligibility after 5 years?", "category": "Employment Policy"},
    {"id": "ep_065", "query": "Who is designated as an Access Person subject to pre-clearance rules?", "category": "Employment Policy"},
]

eval_benchmark_data = [
    {
        "id": "eval_001",
        "query": "How many days of Earned Annual Leave are credited to employees per financial year?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s1"],
        "expected_entities": [
            {"text": "18 days", "label": "DURATION"},
            {"text": "Earned Annual Leave", "label": "LEAVE_TYPE"},
            {"text": "financial year", "label": "ELIGIBILITY_PERIOD"}
        ]
    },
    {
        "id": "eval_002",
        "query": "What is the quarterly accrual rate for Earned Leave and the maximum carry forward cap?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s1"],
        "expected_entities": [
            {"text": "4.5 days", "label": "DURATION"},
            {"text": "45 days", "label": "DURATION"},
            {"text": "Earned Leave", "label": "LEAVE_TYPE"}
        ]
    },
    {
        "id": "eval_003",
        "query": "How many days of Casual/Sick Leave are credited annually on April 1st?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s1"],
        "expected_entities": [
            {"text": "12 days", "label": "DURATION"},
            {"text": "Casual/Sick Leave", "label": "LEAVE_TYPE"},
            {"text": "April 1st", "label": "DATE"}
        ]
    },
    {
        "id": "eval_004",
        "query": "How do employees apply for leave on the PeoplePulse HRMS portal?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-HR-001_s2"],
        "expected_entities": [
            {"text": "PeoplePulse", "label": "ORG"},
            {"text": "Earned Leave", "label": "LEAVE_TYPE"},
            {"text": "Casual Leave", "label": "LEAVE_TYPE"},
            {"text": "Sick Leave", "label": "LEAVE_TYPE"}
        ]
    },
    {
        "id": "eval_005",
        "query": "What is the manager approval SLA and advance notice required for leave over 3 consecutive business days?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-HR-001_s2"],
        "expected_entities": [
            {"text": "3 consecutive business days", "label": "DURATION"},
            {"text": "7 working days", "label": "DURATION"},
            {"text": "48-hour", "label": "DURATION"},
            {"text": "72 hours", "label": "DURATION"}
        ]
    },
    {
        "id": "eval_006",
        "query": "How many weeks of paid Maternity Leave are female employees entitled to?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s3"],
        "expected_entities": [
            {"text": "26 weeks", "label": "DURATION"},
            {"text": "Maternity Leave", "label": "LEAVE_TYPE"},
            {"text": "Maternity Benefit Act", "label": "LAW"}
        ]
    },
    {
        "id": "eval_007",
        "query": "What is the Paternity Leave and Bereavement Leave duration granted to DSPAMC employees?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s3"],
        "expected_entities": [
            {"text": "10 working days", "label": "DURATION"},
            {"text": "Paternity Leave", "label": "LEAVE_TYPE"},
            {"text": "6 months", "label": "ELIGIBILITY_PERIOD"},
            {"text": "5 working days", "label": "DURATION"},
            {"text": "Bereavement Leave", "label": "LEAVE_TYPE"},
            {"text": "12 weeks", "label": "DURATION"},
            {"text": "Adoption Leave", "label": "LEAVE_TYPE"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    },
    {
        "id": "eval_008",
        "query": "Where and when should new hires report for Day 1 induction at DSPAMC?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-HR-002_s1"],
        "expected_entities": [
            {"text": "One BKC", "label": "ORG"},
            {"text": "Day 1", "label": "DATE"},
            {"text": "09:30 IST", "label": "TIME"},
            {"text": "Mumbai", "label": "GPE"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    },
    {
        "id": "eval_009",
        "query": "What statutory declarations must new joiners complete between Days 15 to 30?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-HR-002_s1"],
        "expected_entities": [
            {"text": "Days 15–30", "label": "ELIGIBILITY_PERIOD"},
            {"text": "PF Form 11", "label": "DOCUMENT"},
            {"text": "Gratuity Form F", "label": "DOCUMENT"},
            {"text": "Mediclaim", "label": "PRODUCT"}
        ]
    },
    {
        "id": "eval_010",
        "query": "Within how many calendar days must wealth advisors and research analysts obtain NISM certifications?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-HR-002_s2"],
        "expected_entities": [
            {"text": "60 calendar days", "label": "DURATION"},
            {"text": "NISM-Series-V-A", "label": "PRODUCT"},
            {"text": "NISM-Series-XV", "label": "PRODUCT"},
            {"text": "DSP L&D Portal", "label": "ORG"}
        ]
    },
    {
        "id": "eval_011",
        "query": "How do employees request access to Bloomberg Terminal or Qdrant Vector Store on ServiceHub?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-IT-001_s1"],
        "expected_entities": [
            {"text": "ServiceHub", "label": "ORG"},
            {"text": "Bloomberg Terminal", "label": "PRODUCT"},
            {"text": "Qdrant Vector Store", "label": "PRODUCT"},
            {"text": "24 hours", "label": "DURATION"}
        ]
    },
    {
        "id": "eval_012",
        "query": "What are the remote VPN and MFA authentication requirements for DSPAMC staff?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-IT-001_s2"],
        "expected_entities": [
            {"text": "Cisco AnyConnect", "label": "PRODUCT"},
            {"text": "Microsoft Authenticator", "label": "PRODUCT"},
            {"text": "YubiKey", "label": "PRODUCT"},
            {"text": "14 characters", "label": "CARDINAL"},
            {"text": "90 days", "label": "DURATION"}
        ]
    },
    {
        "id": "eval_013",
        "query": "What is the submission deadline for filing travel expense claims via SAP Concur?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s1"],
        "expected_entities": [
            {"text": "SAP Concur", "label": "ORG"},
            {"text": "30 calendar days", "label": "DURATION"},
            {"text": "45 days", "label": "DURATION"},
            {"text": "5 business days", "label": "DURATION"},
            {"text": "CFO", "label": "TITLE"}
        ]
    },
    {
        "id": "eval_014",
        "query": "What are the metro accommodation cap and daily per diem subsistence allowance limits?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s2"],
        "expected_entities": [
            {"text": "₹8,500/night", "label": "MONEY"},
            {"text": "₹5,500/night", "label": "MONEY"},
            {"text": "₹1,800/day", "label": "MONEY"},
            {"text": "Mumbai", "label": "GPE"},
            {"text": "Tier-1", "label": "CATEGORY"}
        ]
    },
    {
        "id": "eval_015",
        "query": "What is the pre-clearance validity period and holding rule under the SEBI personal trading code?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-COMP-001_s1"],
        "expected_entities": [
            {"text": "48 hours", "label": "DURATION"},
            {"text": "30-calendar-day", "label": "DURATION"},
            {"text": "ComplianceDesk", "label": "ORG"},
            {"text": "SEBI", "label": "ORG"}
        ]
    },
    {
        "id": "eval_016",
        "query": "What is the Chinese Wall policy for Unpublished Price Sensitive Information (UPSI)?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-COMP-001_s2"],
        "expected_entities": [
            {"text": "Chinese Walls", "label": "CONCEPT"},
            {"text": "UPSI", "label": "CONCEPT"},
            {"text": "SEBI", "label": "ORG"}
        ]
    },
    {
        "id": "eval_017",
        "query": "What are the trade settlement timeline and STP cut-off on trade day?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-OPS-001_s1"],
        "expected_entities": [
            {"text": "18:30 IST", "label": "TIME"},
            {"text": "T+1", "label": "DATE"},
            {"text": "CCIL", "label": "ORG"},
            {"text": "NSCCL", "label": "ORG"}
        ]
    },
    {
        "id": "eval_018",
        "query": "When are scheme NAVs calculated daily and disseminated to AMFI?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-OPS-001_s2"],
        "expected_entities": [
            {"text": "16:30 IST", "label": "TIME"},
            {"text": "23:00 IST", "label": "TIME"},
            {"text": "AMFI", "label": "ORG"}
        ]
    },
    {
        "id": "eval_019",
        "query": "Can unutilized Earned Leave beyond 45 days be encashed by full-time employees?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s1"],
        "expected_entities": [
            {"text": "45 days", "label": "DURATION"},
            {"text": "Earned Leave", "label": "LEAVE_TYPE"},
            {"text": "AMFI", "label": "ORG"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    },
    {
        "id": "eval_020",
        "query": "What is the manager escalation timeline if a leave application is not actioned after 48 hours?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-HR-001_s2"],
        "expected_entities": [
            {"text": "48-hour", "label": "DURATION"},
            {"text": "72 hours", "label": "DURATION"},
            {"text": "PeoplePulse", "label": "ORG"}
        ]
    },
    {
        "id": "eval_021",
        "query": "How many weeks of Adoption Leave are available to DSPAMC employees?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s3"],
        "expected_entities": [
            {"text": "12 weeks", "label": "DURATION"},
            {"text": "Adoption Leave", "label": "LEAVE_TYPE"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    },
    {
        "id": "eval_022",
        "query": "What are the Day 1 induction activities for new employees arriving at One BKC Mumbai?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-HR-002_s1"],
        "expected_entities": [
            {"text": "Day 1", "label": "DATE"},
            {"text": "One BKC", "label": "ORG"},
            {"text": "09:30 IST", "label": "TIME"}
        ]
    },
    {
        "id": "eval_023",
        "query": "Who reimburses the exam registration fees for NISM-Series-XV certification?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-HR-002_s2"],
        "expected_entities": [
            {"text": "DSP L&D Portal", "label": "ORG"},
            {"text": "NISM-Series-XV", "label": "PRODUCT"},
            {"text": "100%", "label": "PERCENT"}
        ]
    },
    {
        "id": "eval_024",
        "query": "What systems can be requested via the DSP ServiceHub application access portal?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-IT-001_s1"],
        "expected_entities": [
            {"text": "DSP ServiceHub", "label": "ORG"},
            {"text": "Bloomberg Terminal", "label": "PRODUCT"},
            {"text": "Refinitiv Eikon", "label": "PRODUCT"},
            {"text": "Qdrant", "label": "PRODUCT"}
        ]
    },
    {
        "id": "eval_025",
        "query": "What password complexity rules and 90 days expiry are mandated for DSP accounts?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-IT-001_s2"],
        "expected_entities": [
            {"text": "14 characters", "label": "CARDINAL"},
            {"text": "90 days", "label": "DURATION"},
            {"text": "Microsoft Authenticator", "label": "PRODUCT"}
        ]
    },
    {
        "id": "eval_026",
        "query": "Why are expense claims filed past 45 days rejected without CFO approval?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-FIN-001_s1"],
        "expected_entities": [
            {"text": "45 days", "label": "DURATION"},
            {"text": "CFO", "label": "TITLE"},
            {"text": "SAP Concur", "label": "ORG"}
        ]
    },
    {
        "id": "eval_027",
        "query": "What is the per diem incidental rate of ₹1,800/day for Tier-1 metros?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s2"],
        "expected_entities": [
            {"text": "₹1,800/day", "label": "MONEY"},
            {"text": "Tier-1", "label": "CATEGORY"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    },
    {
        "id": "eval_028",
        "query": "How many days must Access Persons hold approved securities under the SEBI code?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-COMP-001_s1"],
        "expected_entities": [
            {"text": "30-calendar-day", "label": "DURATION"},
            {"text": "SEBI", "label": "ORG"},
            {"text": "ComplianceDesk", "label": "ORG"}
        ]
    },
    {
        "id": "eval_029",
        "query": "What is the consequence of sharing Unpublished Price Sensitive Information without authorization?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-COMP-001_s2"],
        "expected_entities": [
            {"text": "UPSI", "label": "CONCEPT"},
            {"text": "SEBI", "label": "ORG"}
        ]
    },
    {
        "id": "eval_030",
        "query": "How does automated Straight-Through Processing (STP) settle equity orders across NSE and BSE?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-OPS-001_s1"],
        "expected_entities": [
            {"text": "STP", "label": "CONCEPT"},
            {"text": "T+1", "label": "DATE"},
            {"text": "CCIL", "label": "ORG"},
            {"text": "NSCCL", "label": "ORG"}
        ]
    },
    {
        "id": "eval_031",
        "query": "Who must provide dual-signoff on mutual fund NAVs before 23:00 IST AMFI submission?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-OPS-001_s2"],
        "expected_entities": [
            {"text": "23:00 IST", "label": "TIME"},
            {"text": "AMFI", "label": "ORG"},
            {"text": "16:30 IST", "label": "TIME"}
        ]
    },
    {
        "id": "eval_032",
        "query": "How many days of Paternity Leave must be taken within 6 months of childbirth?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s3"],
        "expected_entities": [
            {"text": "10 working days", "label": "DURATION"},
            {"text": "Paternity Leave", "label": "LEAVE_TYPE"},
            {"text": "6 months", "label": "ELIGIBILITY_PERIOD"}
        ]
    },
    {
        "id": "eval_033",
        "query": "What is the flight travel class policy for Associate Vice Presidents and below?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s2"],
        "expected_entities": [
            {"text": "Economy Class", "label": "CATEGORY"},
            {"text": "Associate Vice President", "label": "TITLE"},
            {"text": "6 hours", "label": "DURATION"}
        ]
    },
    {
        "id": "eval_034",
        "query": "How long are trade pre-clearance approvals valid on the DSP ComplianceDesk portal?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-COMP-001_s1"],
        "expected_entities": [
            {"text": "48 hours", "label": "DURATION"},
            {"text": "DSP ComplianceDesk", "label": "ORG"}
        ]
    },
    {
        "id": "eval_035",
        "query": "What IT workstation setup and Peer Buddy meeting take place during Week 1 onboarding?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-HR-002_s1"],
        "expected_entities": [
            {"text": "Week 1", "label": "DATE"},
            {"text": "ServiceNow", "label": "ORG"},
            {"text": "PeoplePulse", "label": "ORG"}
        ]
    },
    {
        "id": "eval_036",
        "query": "What notice period must employees provide when applying for 4 days of Earned Leave?",
        "category": "Approval Workflow",
        "expected_chunk_ids": ["DSP-HR-001_s2"],
        "expected_entities": [
            {"text": "7 working days", "label": "DURATION"},
            {"text": "Earned Leave", "label": "LEAVE_TYPE"},
            {"text": "PeoplePulse", "label": "ORG"}
        ]
    },
    {
        "id": "eval_037",
        "query": "How is NEFT reimbursement credited within 5 business days after line manager approval?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s1"],
        "expected_entities": [
            {"text": "5 business days", "label": "DURATION"},
            {"text": "NEFT", "label": "PAYMENT_METHOD"},
            {"text": "SAP Concur", "label": "ORG"}
        ]
    },
    {
        "id": "eval_038",
        "query": "What is the accommodation limit of ₹5,500/night for non-metro business trips?",
        "category": "Reimbursement",
        "expected_chunk_ids": ["DSP-FIN-001_s2"],
        "expected_entities": [
            {"text": "₹5,500/night", "label": "MONEY"},
            {"text": "₹8,500/night", "label": "MONEY"}
        ]
    },
    {
        "id": "eval_039",
        "query": "Why are trades in securities listed on the DSP Restricted List automatically denied pre-clearance?",
        "category": "Employment Policy",
        "expected_chunk_ids": ["DSP-COMP-001_s1"],
        "expected_entities": [
            {"text": "Restricted List", "label": "CONCEPT"},
            {"text": "Grey List", "label": "CONCEPT"},
            {"text": "DSP", "label": "ORG"}
        ]
    },
    {
        "id": "eval_040",
        "query": "How many days of paid Bereavement Leave does DSPAMC offer for grieving employees?",
        "category": "Leave Policy",
        "expected_chunk_ids": ["DSP-HR-001_s3"],
        "expected_entities": [
            {"text": "5 working days", "label": "DURATION"},
            {"text": "Bereavement Leave", "label": "LEAVE_TYPE"},
            {"text": "DSPAMC", "label": "ORG"}
        ]
    }
]

with open("backend/data/nlp/intent_dataset.json", "w", encoding="utf-8") as f:
    json.dump(intent_data, f, indent=2)
print(f"Wrote {len(intent_data)} queries to backend/data/nlp/intent_dataset.json")

with open("backend/data/nlp/eval_benchmark.json", "w", encoding="utf-8") as f:
    json.dump(eval_benchmark_data, f, indent=2)
print(f"Wrote {len(eval_benchmark_data)} benchmark items to backend/data/nlp/eval_benchmark.json")

