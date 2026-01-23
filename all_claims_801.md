--Insert Death claims on workflow not yet notified on Orbit
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select oa.proc_id, oa.casenum, oa.stepname
from ODSSWPRO.OUTSTANDING_ADDR oa '
If @grpno <> '*'
or @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + '
    Inner join 	ODSSWPRO.CASE_DATA cd
    on  oa.proc_id = cd.proc_id
    and oa.casenum = cd.casenum
    and ' + @sq + @sq + 'GRPNO' + @sq + @sq + ' = cd.field_name '
 End
Set @sqltext = Rtrim(@sqltext) + '
where oa.proc_id = 89 '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and cd.field_value_n = ' + @sq + @sq + @grpno + @sq + @sq
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and cd.field_value_n in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext)  + ' '
+ @sq + ')'
Set @msg = 'Insert Death claims on workflow not yet notified on Orbit'
Insert into ##CLM_Progress values (@msg, getdate())
Delete from #outstanding_addr
Insert into #outstanding_addr Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Death claims on workflow not yet notified on Orbit'

Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select	ci.proc_id, ci.casenum,
        to_char(ci.started,' + @sq + @sq + 'yyyy-mm-dd' + @sq + @sq + ') as started
from ODSSWPRO.CASE_INFORMATION ci '
If @grpno <> '*'
or @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + '
    Inner join 	ODSSWPRO.CASE_DATA cd
    on  ci.proc_id = cd.proc_id
    and ci.casenum = cd.casenum
    and ' + @sq + @sq + 'GRPNO' + @sq + @sq + ' = cd.field_name '
 End
Set @sqltext = Rtrim(@sqltext) + '
Where ci.proc_id = 89
  and ci.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 89) '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and cd.field_value_n = ' + @sq + @sq + @grpno + @sq + @sq
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and cd.field_value_n in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext)  + ' '
+ @sq + ')'
Set @msg = 'Insert Death claims Case Information'
Insert into ##CLM_Progress values (@msg, getdate())
Delete from #case_information
Insert into #case_information Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Death claims Case Information'

Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select	cd.proc_id, cd.casenum,
        Max(Case When cd.field_name = ' + @sq + @sq + 'GRPNO' + @sq + @sq + ' then cd.field_value else ' + @sq + @sq + '' + @sq + @sq + ' end) as grpno,
        Max(Case When cd.field_name = ' + @sq + @sq + 'PERNO' + @sq + @sq + ' then cd.field_value else ' + @sq + @sq + '0' + @sq + @sq + ' end) as perno,
        Max(Case When cd.field_name = ' + @sq + @sq + 'ROLENO' + @sq + @sq + ' then cd.field_value else ' + @sq + @sq + '0' + @sq + @sq + ' end) as rolno,
        Max(Case When cd.field_name = ' + @sq + @sq + 'DEATHDATE' + @sq + @sq + ' then cd.field_value_n else ' + @sq + @sq + '' + @sq + @sq + ' end) as deathdate
from ODSSWPRO.CASE_DATA cd '
If @grpno <> '*'
or @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + '
    Inner join 	ODSSWPRO.CASE_DATA grp
    on  cd.proc_id = grp.proc_id
    and cd.casenum = grp.casenum
    and ' + @sq + @sq + 'GRPNO' + @sq + @sq + ' = grp.field_name '
 End
Set @sqltext = Rtrim(@sqltext) + '
Where cd.proc_id = 89
  and cd.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 89)
  and cd.field_name in (' + @sq + @sq + 'GRPNO' + @sq + @sq + ', '
                          + @sq + @sq + 'PERNO' + @sq + @sq + ', '
                          + @sq + @sq + 'ROLENO' + @sq + @sq + ', '
                          + @sq + @sq + 'DEATHDATE' + @sq + @sq + ') '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n = ' + @sq + @sq + @grpno + @sq + @sq
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext)  + '
Group by cd.proc_id, cd.casenum '
+ @sq + ')'
Set @msg = 'Insert Death claims Case Data'
Insert into ##CLM_Progress values (@msg, getdate())
Delete from #case_data
Insert into #case_data Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Death claims Case Data'

Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select aut.casenum
from ODSSWPRO.AUDIT_TRAIL aut '
If @grpno <> '*'
or @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + '
    Inner join 	ODSSWPRO.CASE_DATA grp
    on  aut.proc_id = grp.proc_id
    and aut.casenum = grp.casenum
    and ' + @sq + @sq + 'GRPNO' + @sq + @sq + ' = grp.field_name '
 End
Set @sqltext = Rtrim(@sqltext) + '
where aut.proc_id = 89
  and aut.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 89)
  and aut.stepname in (' + @sq + @sq + 'NOTIFCLM' + @sq + @sq + ', ' + @sq + @sq + 'NOTIFCL1' + @sq + @sq + ', ' + @sq + @sq + 'NOTCLM2' + @sq + @sq + ')
  and aut.type_id = 2 '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n = ' + @sq + @sq + @grpno + @sq + @sq
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext)  + ' '
+ @sq + ')'
Set @msg = 'Insert 89 NOTIFCLM Audit Step Data'
Insert into ##CLM_Progress values (@msg, getdate())
Delete from #been_notified
Insert into #been_notified  Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert 89 NOTIFCLM Audit Step Data'

delete from #outstanding_addr
where casenum in (Select casenum from #been_notified)

delete from #outstanding_addr
Where Convert(varchar(3),proc_id) + '-' + Convert(varchar(10),casenum) in (Select Workflow_Id from #claimdata)

delete from #case_information
where casenum in (Select casenum from #been_notified)

delete from #case_information
Where Convert(varchar(3),proc_id) + '-' + Convert(varchar(10),casenum) in (Select Workflow_Id from #claimdata)

delete from #case_data
where casenum in (Select casenum from #been_notified)

delete from #case_data
Where Convert(varchar(3),proc_id) + '-' + Convert(varchar(10),casenum) in (Select Workflow_Id from #claimdata)

Set @msg = 'Insert 89TYPES Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata
Select	0,
        '89TYPES',
        started,
        IsNull(grpno,''),
        0,
        0,
        perno,
        rolno,
        '',
        '',
        0,
        0,
        '',
        '',
        '',
        '',
        0,
        '',
        0,
        0,
        deathdate,
        '',
        Rtrim(Ltrim(Convert(char(5),ci.proc_id))) + '-' + Rtrim(Ltrim(Convert(char(10),ci.casenum)))
from #case_information ci
Left Join #case_data cd
on  ci.proc_id = cd.proc_id
and ci.casenum = cd.casenum
If @grpno <> '*'
 Begin
    Delete from #claimdata where clagrpno <> @grpno
 End
If @secure_groups_only = 'y'
 Begin
    Delete from #claimdata where clagrpno not in (Select SecureGroupCode from securegrouptable())
 End
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert 89TYPES Data'

--Get Current cover
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select rskgrpno, rskconno, rskbenno, rskperno, rskrolno, rsksumassr, cbebentype, cbebenid
from FAWDATA.FSRSKPF
Left join FAWDATA.FSCBEPF
on  rskconno = cbeconno
and rskbenno = cbebenno
where rskactind = ' + @sq + @sq + 'Y' + @sq + @sq + '
  and rskstate = ' + @sq + @sq + 'N'  + @sq + @sq + '
  and rsksumassr <> 0 '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and rskgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and rskgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Get Current cover'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsrskpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Get Current cover'

update #claimdata set clafthtype = '' where clafthtype is null
update #claimdata set clafthold = '' where clafthold is null
update #claimdata set clafthnew = '' where clafthnew is null
update #claimdata set clatrxarea = '' where clatrxarea is null

Set @msg = 'Main Select'
Insert into ##CLM_Progress values (@msg, getdate())

Select	grpteamcod as Team_Code,
        clagrpno as Group_No,
        grpgrpname as Employer_Name,
        Case when clalthtype = 'CLMNOTCLAIM' and isnumeric(substring(clafthnew,31,6)) = 1 then convert(int,substring(clafthnew,31,6))
             else IsNull(benconref,0)
        End as Contract_Reference,
        convert(char(40),'') as Product_Name,
        claperno as Person_No,
        clarolno as Role_No,
        perinit as Initials,
        persurname as Surname,
        peridno as ID_Number,
        Max(pergcode) as Gender,
        Max(permcode) as Marital_Status,
        Max(perdob) as DOB,
        Min(Case When clalthtype = 'UDRDTH' Then '0 - Death'
                 When clalthtype = 'UDRDIS' Then '1 - Disability'
                 When clalthtype = 'UDRPTD' Then '2 - Lump Sum Disability'
                 When clalthtype = 'UDRDRD' Then '3 - Dread Disease'
                 When clalthtype = 'UDRSAC' Then '4 - SAC'
                 When clalthtype = 'UDRSLC' Then '5 - Spouse Life Cover'
                 When clalthtype = 'UDRFDB' Then '7 - Funeral'
                 When clalthtype = 'UDRFCB' Then '8 - Funeral'
                 When clalthtype = '96TYPES' Then '8 - Funeral'
                 When clalthtype = '89TYPES' Then '0 - Death'
                 When clalthtype = 'ADJCLMDTH' Then '0 - Death'
                 else '9 - Non Risk' end) as Claim_Type,
        Max(Case When clalthtype = 'UDRDTH' Then convert(char(255),codavalue) else convert(char(255),'') end) as Cause_Of_Death_Disability,
        Max(Case When clalthtype in ('ADJCLMDTH', 'UDRDTH', 'CLMDTHACCEPT')then rolenddt
                 When clalthtype in ('UDRFDB', 'UDRFCB') and IsNull(mbfdod,'') <> '' then mbfdod
                 When clalthtype in ('UDRFDB', 'UDRFCB', 'UDRDIS', 'URDPTD') and IsNull(mbfdod,'') = '' and clafthold not like '%DECL%' and IsNull(udwevtdate,'') <> '' then udwevtdate
                 When clalthtype in ('UDRFDB', 'UDRFCB') and IsNull(mbfdod,'') = '' and IsNull(udwevtdate,'') = '' then rolenddt
                 else '' end) as Date_Of_Death_Disability,
        Min(Case When clalthtype in ('CLD', 'CLDGUAR', 'CLDWRKFLW', 'CLMNOTCLAIM') then claindttm
                 When clalthtype like 'UDR%' then claindttm
                 When clalthtype in ('96TYPES', '89TYPES') then 'Z - Not Notified'
                 else 'Z - Unknown' end) as Orbit_Notification_Date,
        Min(Case When Workflow_Id = '' then 'Z - Unknown'
                 else Workflow_Id end) as Worflow_No,
        Min(Case When clalthtype in ('96TYPES', '89TYPES') then claindttm
                 When WF_Started <> '' then WF_Started
                 else 'Z - Unknown' end) as Worflow_Start_Date,
        Min(Case When clalthtype in ('CLD', 'CLDGUAR') and clastatus = 'A' Then '9 - Trade Completed'
                 When clalthtype in ('CLD', 'CLDGUAR') and clastatus = 'P' Then '5 - Confirming Trade'
                 When clalthtype in ('CLD', 'CLDGUAR') and clastatus = 'S' Then '3 - Trade Requested'
                 When clalthtype Not in ('CLD', 'CLDGUAR') Then '99 - No SOF'
                 Else '1 - Unknown' end) as SOF_Disinvestment_Status,
        Sum(Case When clalthtype in ('CLD', 'CLDGUAR') and claporno = 5 and clasthtype in ('I', 'B') then claarands
                 When clalthtype in ('CLD', 'CLDGUAR') and claporno = 5 and clasthtype in ('D', 'S') then claarands * -1
                 Else 0 end) as Total_Amount_Disinvested,
        Min(Case When clalthtype like 'UDR%' then claindttm
                 When clalthtype in ('96TYPES', '89TYPES') then 'Not Notified'
                 else 'Z - Unknown' end) as Underwriting_Request_Date,
        Max(Case When clalthtype like '%DTH%' and clalthtype not like '%UDW%' then clasalary else 0 end) as DTH_Salary,
        Max(Case When clalthtype like '%DTH%' and clalthtype like '%UDW%' then clasalary else 0 end) as UDWDTH_Salary,
        Max(Case When clalthtype = 'UDRDTH' and claapproved = 'Y' then clafcl1 else 0 end) as DTH_Approved_FCL,
        Max(Case When clalthtype = 'UDRDTH' and claapproved <> 'Y' then clafcl1 else 0 end) as DTH_UnApproved_FCL,
        Sum(Case When clalthtype = 'UDRDTH' then claarands else 0 end) as UDWDTH_Amount,
        Sum(Case When clalthtype = 'UDRDTH' and claapproved = 'Y' then claarands
                 else Convert(Money,0) end) as UDRDTH_Approved_Amount,
        Sum(Case When clalthtype = 'UDRDTH' and claapproved <> 'Y' then claarands
                 else Convert(Money,0) end) as UDRDTH_UnApproved_Amount,
        Max(Case When clalthtype = 'UDRDTH' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRDTH'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRDTH' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWDTH_Decision,
        Sum(Case When clalthtype = 'CLMDTHACCEPT' and clasthtype in ('I', 'B') then claarands
                 When clalthtype = 'CLMDTHACCEPT' and clasthtype not in ('I', 'B') then claarands
                 else Convert(Money,0) end) as DTHACCEPT_Amount,
        Sum(Case When clalthtype = 'ADJCLMDTH' and clasthtype in ('I', 'B') then claarands
                 When clalthtype = 'ADJCLMDTH' and clasthtype not in ('I', 'B') then claarands * -1
                 else Convert(Money,0) end) as DTH_Adjustment_Amount,
        Max(Case When clalthtype in ('UDRDRD', 'UDRDIB', 'UDRPHI') then udwevtdate else '' end) as Event_Date,
        Max(Case When clalthtype = 'UDRPTD' then claarands else 0 end) as UDWPTD_Amount,
        Max(Case When clalthtype = 'UDRPTD' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRPTD'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRPTD' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWPTD_Decision,
        Sum(Case When clalthtype = 'CLMPTDACCEPT' then claarands
                 else Convert(Money,0) end) as PTDACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRDIS' then cladibamt else 0 end) as UDWDIS_Amount,
        Max(Case When clalthtype = 'UDRDIS' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRDIS'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRDIS' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWDIS_Decision,
        Sum(Case When clalthtype = 'UDRDIS' and SubString(clafthnew,1,16) = 'Disability Amt =' and SubString(clafthold,1,14) = 'UW Decision = '
                    then Convert(Money,Rtrim(Ltrim(SubString(clafthnew,17,20))))
                 else Convert(Money,0) end) as UDWDIS_Approved_Amount,
        Max(Case When clalthtype = 'UDRDRD' then claarands else 0 end) as UDWDRD_Amount,
        Max(Case When clalthtype = 'UDRDRD' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRDRD'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRDRD' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWDRD_Decision,
        Sum(Case When clalthtype = 'CLMDRDACCEPT' then claarands
                 else Convert(Money,0) end) as DRDACCEPT_Amount,
        Max(Case When clalthtype = 'UDRSAC' then claarands else 0 end) as UDWSAC_Amount,
        Max(Case When clalthtype = 'UDRSAC' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRSAC'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRSAC' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWSAC_Decision,
        Sum(Case When clalthtype = 'CLMSACACCEPT' then claarands
                 else Convert(Money,0) end) as SACACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRSLC' then claarands else 0 end) as UDWSLC_Amount,
        Max(Case When clalthtype = 'UDRSLC' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRSLC'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRSLC' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWSLC_Decision,
        Sum(Case When clalthtype = 'CLMSLCACCEPT' then claarands
                 else Convert(Money,0) end) as SLCACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRFCB' then claarands else 0 end) as UDWFCB_Amount,
        Max(Case When clalthtype = 'UDRFCB' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRFCB'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRFCB' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWFCB_Decision,
        Sum(Case When clalthtype = 'CLMFCBACCEPT' then claarands
                 else Convert(Money,0) end) as FCBACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRFDB' then claarands else 0 end) as UDWFDB_Amount,
        Max(Case When clalthtype = 'UDRFDB' and SubString(clafthold,1,14) = 'UW Decision = '  and clastatus = 'A' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRFDB'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRFDB' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWFDB_Decision,
        Sum(Case When clalthtype = 'CLMFDBACCEPT' then claarands
                 else Convert(Money,0) end) as FDBACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRMED' then claarands else 0 end) as UDWMED_Amount,
        Max(Case When clalthtype = 'UDRMED' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRMED'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRMED' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWMED_Decision,
        Sum(Case When clalthtype = 'CLMMEDACCEPT' then claarands
                 else Convert(Money,0) end) as MEDACCEPT_Amount,
        Sum(Case When clalthtype = 'UDREDU' then claarands else 0 end) as UDWEDU_Amount,
        Max(Case When clalthtype = 'UDREDU' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDREDU'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDREDU' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWEDU_Decision,
        Sum(Case When clalthtype = 'CLMEDUACCEPT' then claarands
                 else Convert(Money,0) end) as EDUACCEPT_Amount,
        Sum(Case When clalthtype = 'UDRSPB' then claarands else 0 end) as UDWSPB_Amount,
        Max(Case When clalthtype = 'UDRSPB' and SubString(clafthold,1,14) = 'UW Decision = ' then SubString(clafthold,15,4)
                 When clalthtype = 'UDRSPB'
                  and clafthold in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                    'MDEC','NMED','RES','RESC','RESM','STD') then SubString(clafthold,1,4)
                 When clalthtype = 'UDRSPB' and SubString(clafthold,1,14) <> 'UW Decision = '
                  and clafthold not in ('ACCW','AMAX','AMED','CANC','DECL','DEF','DEF3','DEF6','DEFI','EXCL','EXLD','LOAD',
                                        'MDEC','NMED','RES','RESC','RESM','STD') then 'Pending'
                 else '' end) as UDWSPB_Decision,
        Sum(Case When clalthtype = 'CLMSPBACCEPT' then claarands
                 else Convert(Money,0) end) as SPBACCEPT_Amount,
        Sum(Case When clalthtype like 'CLM%' and clalthtype not like '%ACCEPT%' and clalthtype not like '%PAY%'
                    then claarands
                 else 0 end) as Net_Movements,
        Sum(Case When clalthtype like 'CLM%' and clalthtype like '%PAY%'
                    then claarands * -1
                 else 0 end) as Total_All_Payments,
        Min(Case When clalthtype = 'MEMPAYFACS' then claindttm
                 When clalthtype like 'CLM%' and clalthtype like '%PAY%' then claindttm
                 else '9999-99-99'
            end) as First_Payment_Date,
        Max(Case When clalthtype = 'MEMPAYFACS' then claindttm
                 When clalthtype like 'CLM%' and clalthtype like '%PAY%' then claindttm
                 else '0000-00-00'
            end) as Last_Payment_Date,
        Sum(Case When clalthtype like 'CLM%' and clalthtype like '%PAY%' and clalthtype like '%TAX%' and clasthtype in ('I', 'B')
                    then claarands
                 When clalthtype like 'CLM%' and clalthtype like '%PAY%' and clalthtype like '%TAX%' and clasthtype not in ('I', 'B')
                    then claarands * -1
                 else 0 end) as Total_Tax_Payments,
        Max(IsNull(mprtotunt,0)) as Current_Bank_Balance,
        Max(Case When clalthtype = '96TYPES' and cbebentype = 'DTH' and cbebenid in ('FCB', 'FDB') then rsksumassr
                 When clalthtype = '89TYPES'  and cbebentype = 'DTH' and cbebenid = 'LSD' Then rsksumassr
                 Else 0
            End) as Current_Cover
into ##clmot
from #claimdata
Left join #wf_started
on Workflow_Id = Workflow_Start_ID
Left join #fsgrppf
on clagrpno = grpgrpno
Left join #fsperpf
on claperno = perperno
Left join #fsrolpf
on  clagrpno = rolgrpno
and claperno = rolperno
and clarolno = rolrolno
Left join #fsmprpf
on  clagrpno = mprgrpno
and claperno = mprperno
and clarolno = mprrolno
Left join #fsmbppf
   Left join #fscodpf
   on  'DEATHCAUSE' = codcodtype
   and mbpparmval = codsubcode
on  clagrpno = mbpgrpno
and claperno = mbpperno
and clarolno = mbprolno
and 'DEATHCAUSE' = mbpparmnm
Left Join #fsbenpf
on  clagrpno = bengrpno
and claconno = benconno
and clabenno = benbenno
Left join #fsrskpf
on  clagrpno = rskgrpno
and claconno = rskconno --Removed as not notified has no conno?
and clabenno = rskbenno
and claperno = rskperno
and clarolno = rskrolno
Group by	grpteamcod, clagrpno, grpgrpname,
            Case when clalthtype = 'CLMNOTCLAIM' and isnumeric(substring(clafthnew,31,6)) = 1 then convert(int,substring(clafthnew,31,6))
                 else IsNull(benconref,0)
            End,
            claperno, clarolno, perinit, persurname, peridno
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Main Select'

Set @msg = 'Cleaning Data'
Insert into ##CLM_Progress values (@msg, getdate())

Update ##clmot
Set Product_Name = IsNull(prdprdname,'')
from ##clmot
Left join #fsschpf
on  Group_No = schgrpno
and Contract_Reference = schconno

Update ##clmot
Set First_Payment_Date = ''
Where First_Payment_Date = '9999-99-99'

Update ##clmot
Set Last_Payment_Date = ''
Where Last_Payment_Date = '0000-00-00'

Update ##clmot
Set Last_Payment_Date = ''
Where Last_Payment_Date = '0000-00-00'

Update ##clmot
Set Date_of_Death_Disability = ''
Where Date_of_Death_Disability = '0001-01-01'

--Delete all non risk claims with no pending underwriting
Delete from ##clmot
Where Current_Bank_Balance = 0
  and UDWDTH_Decision <> 'Pending'
  and UDWPTD_Decision <> 'Pending'
  and UDWDRD_Decision <> 'Pending'
  and UDWSAC_Decision <> 'Pending'
  and UDWFCB_Decision <> 'Pending'
  and UDWFDB_Decision <> 'Pending'
  and UDWSLC_Decision <> 'Pending'
  and UDWMED_Decision <> 'Pending'
  and UDWEDU_Decision <> 'Pending'
  and Claim_Type = '9 - Non Risk'

--Delete all non risk claims with no underwriting amounts
Delete from ##clmot
Where Claim_Type = '9 - Non Risk'
  and UDWDTH_Amount = 0
  and UDWPTD_Amount = 0
  and UDWDRD_Amount = 0
  and UDWSAC_Amount = 0
  and UDWFCB_Amount = 0
  and UDWFDB_Amount = 0
  and UDWSLC_Amount = 0
  and UDWMED_Amount = 0
  and UDWEDU_Amount = 0

--Testing for death claims only
--Delete from ##clmot
--Where Claim_Type <> '0 - Death'

Update ##clmot Set Claim_Type = SubString(Claim_Type,4,len(Claim_Type)-3)
Update ##clmot Set SOF_Disinvestment_Status = 'No Trade Found' where SOF_Disinvestment_Status = '99 - No SOF'
Update ##clmot Set SOF_Disinvestment_Status = 'Trade Completed' where SOF_Disinvestment_Status = '9 - Trade Completed'
Update ##clmot Set SOF_Disinvestment_Status = 'Confirming Trade' where SOF_Disinvestment_Status = '5 - Confirming Trade'
Update ##clmot Set SOF_Disinvestment_Status = 'Trade Requested' where SOF_Disinvestment_Status = '3 - Trade Requested'
Update ##clmot Set Underwriting_Request_Date = 'Unknown' where Underwriting_Request_Date = 'Z - Unknown'
Update ##clmot Set Worflow_Start_Date = '' where Worflow_Start_Date = 'Z - Unknown'
Update ##clmot Set Orbit_Notification_Date = 'Not Notified' where Orbit_Notification_Date = 'Z - Not Notified'
Update ##clmot Set Worflow_No = '' where Worflow_No = 'Z - Unknown'
Update ##clmot Set Worflow_No = ' ' where ascii(Worflow_No) = 0

--Get Disability PTD Case Data and update main file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select	proc_id, casenum,
        field_name,
        field_value_n as field_value
from ODSSWPRO.CASE_DATA
where proc_id in (105, 252)
  and field_name in (' + @sq + @sq + 'DISABILITYDATE' + @sq + @sq + ', ' + @sq + @sq + 'CLAIMCAUSE' + @sq + @sq + ') '
+ @sq + ')'
Set @msg = 'Get Disability PTD Case Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #PTD_casedata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Get Disability PTD Case Data'

Set @msg = 'Update CLAIMCAUSE Data'
Insert into ##CLM_Progress values (@msg, getdate())
Update ##clmot
Set Cause_Of_Death_Disability = RTrim(ptd_fldvalue)
from ##clmot
Inner join #PTD_casedata
on  Worflow_No = Rtrim(Ltrim(Convert(char(5),ptd_procid))) + '-' + Rtrim(Ltrim(Convert(char(10),ptd_casenum)))
and ptd_fldname = 'CLAIMCAUSE'
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Update CLAIMCAUSE Data'

Set @msg = 'Update DISABILITYDATE Data'
Insert into ##CLM_Progress values (@msg, getdate())
Update ##clmot
Set Date_Of_Death_Disability = RTrim(ptd_fldvalue)
from ##clmot
Inner join #PTD_casedata
on Worflow_No = Rtrim(Ltrim(Convert(char(5),ptd_procid))) + '-' + Rtrim(Ltrim(Convert(char(10),ptd_casenum)))
and ptd_fldname = 'DISABILITYDATE'
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Update DISABILITYDATE Data'

--Get Date of Death from Case Data
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select	proc_id, casenum,
        field_name,
        field_value_n as field_value
from ODSSWPRO.CASE_DATA
where proc_id = 89
  and field_name in (' + @sq + @sq + 'DEATHDATE' + @sq + @sq + ') '
+ @sq + ')'
Set @msg = 'Get Date of death from workflow'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #DTH_casedata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records updated' where msg = 'Get Date of death from workflow'

Set @msg = 'Update Date of Death Data from workflow'
Insert into ##CLM_Progress values (@msg, getdate())
Update ##clmot
Set Date_Of_Death_Disability = RTrim(dth_fldvalue)
from ##clmot
Inner join #DTH_casedata
on  Worflow_No = Rtrim(Ltrim(Convert(char(5),dth_procid))) + '-' + Rtrim(Ltrim(Convert(char(10),dth_casenum)))
and dth_fldname = 'DEATHDATE'
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records updated' where msg = 'Update Date of Death Data from workflow'

--Write data to analytics database
If @secure_groups_only <> 'y'
 Begin
    Set @msg = 'MCAnalytics'
    Insert into ##CLM_Progress values (@msg, getdate())

    Update ##clmot
    set Surname = 'Secure group',
        Initials = '',
        ID_Number = ''
    where Group_No in (Select SecureGroupCode from securegrouptable())

    If @grpno = '*'
     Begin
        Truncate table [MCAnalytics].[dbo].[monthly_all_claims_extract]
        Insert into [MCAnalytics].[dbo].[monthly_all_claims_extract]
        Select * from ##clmot
     end
 end

--Remove secure groups for septimus version
If @secure_groups_only <> 'y'
 Begin
    Delete from ##clmot where Group_No in (Select SecureGroupCode from securegrouptable())
 End

--Select * from ##clmot where Person_No = 2825275

Set @msg = 'Generating BCP file'
Set @filename = '\\mmcenhnasfs14.metmom.mmih.biz\Packagers\Data_Transfers\Monthly_Data\All_Claims_' + convert(char(10),getdate(),120) + '.csv'

If @grpno <> '*'
 Begin
    Set @filename = '\\mmcenhnasfs14.metmom.mmih.biz\glenn\All_Claims_for_Group_' + @grpno + '_' + convert(char(10),getdate(),120) + '.csv'
 End

If @secure_groups_only = 'y'
 Begin
    Set @filename = '\\mmcenhnasfs14.metmom.mmih.biz\glenn\Secure_All_Claims_' + convert(char(10),getdate(),120) + '.csv'

    --send Capitec claims to Elria
    select * into #IX2clm from ##clmot where Group_No = 'IX2'
    Set @filename2 = '\\mmcenhnasfs14.metmom.mmih.biz\glenn\IX2_All_Claims_' + convert(char(10),getdate(),120) + '.csv'
    Exec sp_bcp_csv '#IX2clm', @filename2, '##ix2bcptab', 'Group_No, Person_No, Role_No', 'y'
    Set @ToEmail = 'Elria.Kraemer@momentum.co.za; Shane.Tasker@momentum.co.za'
    Set @Copy = ''
    Set @BlindCopy = 'glenn.jackson@momentum.co.za; rheino.hickman@momentum.co.za'
    Set @subject = 'IX2 Claims Extract as at ' + Convert(char(10),getdate(),120)
    Set @body = Ltrim(Rtrim(@subject))+ Char(13) + Char(13) +
                'The Monthly IX2 Claims extract has been generated and is attached.' + Char(13) +
                'This is an Automated email. Please do not reply to this email, but rather send any ' +
                'enquiries to FAWUserSupport@mxme.momentum.co.za' + Char(13) + Char(13)
    EXEC msdb.dbo.sp_send_dbmail
            @profile_name = 'SQLTeam',
            @recipients = @ToEmail,
            @copy_recipients = @Copy,
            @blind_copy_recipients = @BlindCopy,
            @subject = @subject,
            @body = @body,
            @file_attachments = @filename2

    Drop table #IX2clm
 End

Exec sp_bcp_csv '##clmot', @filename, '##acebcptab', 'Group_No, Person_No, Role_No', 'y'

Set @ToEmail = 'Naledi.Maneje@momentum.co.za; Tumishi.Malepa@momentum.co.za; Laurinda.Fernandes@momentum.co.za; Bernadine.Petersen@Momentum.co.za; mvanzyl@momentum.com.na; moureen.mahlangu@momentum.co.za; crystal.thyssen@momentum.co.za'
Set @Copy = 'Fareedah.Booley@momentum.co.za; ARamthal@metropolitan.co.za; Maretha.Fischer@Momentum.co.za; Welile.Simelane@metropolitansz.com'
Set @BlindCopy = 'glenn.jackson@momentum.co.za; rheino.hickman@momentum.co.za'
If @grpno <> '*'
 Begin
    Set @ToEmail = 'glenn.jackson@momentum.co.za'
    Set @Copy = 'glenn.jackson@momentum.co.za'
    Set @BlindCopy = 'glenn.jackson@momentum.co.za'
 End
If @secure_groups_only = 'y'
 Begin
    Set @ToEmail = 'glenn.jackson@momentum.co.za' --'rheino.hickman@momentum.co.za;glenn.jackson@momentum.co.za'--'MCBTITYellow@momentum.co.za'
    Set @Copy = ''
    Set @BlindCopy = ''
 End

Set @subject = 'All Claims Extract as at ' + Convert(char(10),getdate(),120)
If @grpno <> '*'
 Begin
    Set @subject = 'All Claims Extract as at ' + Convert(char(10),getdate(),120) + ' for group ' + @grpno
 End
If @secure_groups_only = 'y'
 Begin
    Set @subject = 'Secure All Claims Extract as at ' + Convert(char(10),getdate(),120)
 End

Set @body = Ltrim(Rtrim(@subject))+ Char(13) + Char(13) +
            'The Monthly All Claims extract has been generated. The file can be found at the following location: ' + Char(13) +
            '	' + @filename + ' ' + Char(13) + Char(13) +
            'NOTE: This extract excludes claims from Secure Groups. ' + Char(13) + Char(13) +
            'This is an Automated email. Please do not reply to this email, but rather send any ' +
            'enquiries to FAWUserSupport@mxme.momentum.co.za' + Char(13) + Char(13)

EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'SQLTeam',
        @recipients = @ToEmail,
        @copy_recipients = @Copy,
        @blind_copy_recipients = @BlindCopy,
        @subject = @subject,
        @body = @body

Set @msg = 'Job Completed'
Insert into ##CLM_Progress values (@msg, getdate())
Set @subject = 'All Claims Extract Completed'
Set @body = Ltrim(Rtrim(@subject))
Set @ToEmail = 'glenn.jackson@momentum.co.za'
Set @Copy = 'glenn.jackson@momentum.co.za'
Set @BlindCopy = 'glenn.jackson@momentum.co.za'
EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'SQLTeam',
        @recipients = @ToEmail,
        @copy_recipients = @Copy,
        @blind_copy_recipients = @BlindCopy,
        @subject = @subject,
        @body = @body,
        @query = 'Select id, Rtrim(msg) as msg, convert(char(8),DT,108) as tm from ##CLM_Progress order by id',
        @attach_query_result_as_file = False,
        @query_result_header = false

Drop table #fsgrppf
Drop table #fsschpf
Drop table #fsperpf
Drop table #fsrolpf
Drop table #fsmprpf
Drop table #fsmbppf
Drop table #fsbenpf
Drop table #fscodpf
Drop table #fsrskpf
Drop table #claimdata
Drop table ##clmot
Drop table #BBCRPf
Drop table #bbcrmv
Drop table #outstanding_addr
Drop table #case_information
Drop table #been_notified
Drop table #case_data
Drop table #wf_started
Drop table #PTD_casedata
Drop table #DTH_casedata
Drop table ##CLM_Progress