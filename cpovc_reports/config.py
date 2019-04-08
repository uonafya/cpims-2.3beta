"""Document templates configuration file."""
reports = {}

# Default if no template
reports['NONE'] = (''' ''')

# DSCE - Social enquiry
reports['DSCE'] = ('''
    PERSONAL DETAILS
    Name of Child: %(name)s
    Age: %(age)s
    Nationality: %(nationality)s
    Religion: %(religion)s
    Physical/mental fitness: %(padd_dash)s
    Source of information: %(source)s
    Education Details:
    <line>:
    <line>:
    <blank>
    HOME DETAILS
    County: %(child_county)s
    Sub-County: %(child_sub_county)s
    Ward: %(child_ward)s
    Village: %(child_village)s
    Area Chief: %(child_chief)s
    <blank>
    NAME OF PARENTS / GUARDIANS
    <parents>
    <blank>
    SIBLINGS
    <siblings>
    CASE HISTORY OF THE CHILD
    Type of Case: %(padd_dash)s
    Needs of the child:%(padd_dash)s
    Risk of the Child: %(padd_dash)s
    <blank>
    FAMILY BACKGROUND
    <line>:
    <line>:
    <line>:
    ''')

blank_txt = '.' * 20
# DSUM - Summons
reports['DSUM'] = ('''
    <line>:
    <line>:
    <blank>
    CHILD(REN)'S WELFARE
    <siblings>
    You are hereby requested to report to the Sub-County Children's Officer on %(summon_date)s
    at %(summon_time)s am/pm to discuss matters pertaining to the child/children named above.
    <blank>
    Our offices are situated at %(physical_location)s.
    <blank>
    Name of Office
    SUB-COUNTY CHILDREN OFFICER
    %(case_geo)s
    <blank>
    Copy to: Mr/Mrs/Miss
    ''')

# DCCR - Case conference report
reports['DCCR'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DORD - Court order
reports['DORD'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DFOS - Foster certificate
reports['DFOS'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DHEA - Home environment adjustment report
reports['DHEA'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DADM - Institution admission report
reports['DADM'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DINT - Interview
reports['DINT'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DJPA - Joint Parental responsibility agreement
reports['DJPA'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DMNR - Maintenance reciept
reports['DMNR'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DMED - Medical report
reports['DMED'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DDIS - Plan of disengagement
reports['DDIS'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DITP - Plan of treatment / individual treatment plan
reports['DITP'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DPAR - Post adoption report
reports['DPAR'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DPPR - Post placement report
reports['DPPR'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DREF - Referral letter
# Name 							Age 			Sex

reports['DREF'] = ('''
    <title>TO OTHER AGENCIES, CHILDREN'S INSTITUTIONS, VCOS
    <title>AND ANY OTHER RELEVANT AGENCY OR OFFICE
    <blank>
    TO:
    <line>
    FROM:
    <blank>
    I.  PARTICULARS OF THE CHILD(REN)
    1:
    2:
    3:
    4:
    5:
    <blank>
    Reasons for Referral
    - By Court Order
    - Supervision
    - Others (specify)
    <blank>
    Mother:
    Father:
    <blank>
    II. DOCUMENTS ATTACHED
    1. Case Record Sheet
    2. Social Enquiry Report
    3. Court Order
    4. Individual Treatment Plan
    5. Written Promise
    6. Any Other Document e.g. Medical report/Birth certificate
    Other Details:
    <line>:
    <line>:
    <blank>
    NAME OF REFERRING OFFICER:
    SIGNATURE:
    <blank>
    DATE:
    <blank>
    ''')

# DRNI - Risk and needs assessment report (by institution or Getathuru)
reports['DRNI'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DRNS - Risk and needs assessment report (by SCCO)
reports['DRNS'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DSCH - School report
reports['DSCH'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DTRN - Training report
reports['DTRN'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')

# DWPM - Written promise
reports['DWPM'] = ('''
    <para><font size=12>
    %(padd_dot)s
    </font></para>
    ''')
