USE [Reporting]
GO
/****** Object:  StoredProcedure [dbo].[sp_monthly1_AllClaims]    Script Date: 2025/09/08 10:34:58 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
/*********************************************************************************
Changes:
**********************************************************************************
EBIT-18304	|	2019/02/27	|	R Hickman	|	Migrate to "MCBTITYellow@momentum.co.za"
MCBT-27213	|	2023/06/07	|	T Dweba		|	Add 410 workflow detail
*********************************************************************************/
ALTER procedure [dbo].[sp_monthly1_AllClaims] @secure_groups_only char(1) = 'n'	--n for all. If y, @grpno = '*'
AS

Set nocount on

Declare @sqltext varchar(max)
Declare @sq char(1)
Declare @grpno varchar(3)
Declare @filename varchar(500)
Declare @filename2 varchar(500)
Declare @msg varchar(100)
Declare @ToEmail varchar(max)
Declare @Copy varchar(max)
Declare @BlindCopy varchar(max)
Declare @subject nvarchar(255)
Declare @body nvarchar(max)
--Declare @secure_groups_only char(1)

Create table #fsgrppf (grpgrpno char(3),
                       grpgrpname varchar(100), --EBIT-1058 F de Jager
                       grpteamcod varchar(8))

Create table #fsschpf (schgrpno char(3),
                       schconno int,
                       prdprdname varchar(40))

Create table #fsperpf (perperno int,
                       perinit varchar(6),
                       persurname varchar(40),
                       pergcode varchar(8),
                       permcode varchar(80),
                       perdob char(10),
                       peridno varchar(13))

Create table #fsrolpf (rolgrpno char(3),
                       rolperno int,
                       rolrolno int,
                       rolenddt char(10))

Create table #fsmprpf (mprgrpno char(3),
                       mprperno int,
                       mprrolno int,
                       mprtotunt Money)

Create table #fsbenpf (bengrpno char(3),
                       benconno int,
                       benbenno int,
                       benconref int)

Create table #fsmbppf (mbpgrpno char(3),
                       mbpperno int,
                       mbprolno int,
                       mbpparmnm varchar(10),
                       mbpparmval varchar(30))

Create table #fscodpf (codcodtype varchar(10),
                       codsubcode varchar(8),
                       codavalue varchar(80))

Create table #fsrskpf (rskgrpno char(3),
                       rskconno int,
                       rskbenno int,
                       rskperno int,
                       rskrolno int,
                       rsksumassr money,
                       cbebentype char(3),
                       cbebenid char(3))

Create table #claimdata (claltxno bigint,
                         clalthtype varchar(12),
                         claindttm char(10),
                         clagrpno char(3),
                         claconno int,
                         clabenno  int,
                         claperno int,
                         clarolno int,
                         clastatus char(2),
                         clasthtype char(1),
                         claporno int,
                         claarands Money,
                         clafthtype varchar(12),
                         clafthold varchar(80),
                         clafthnew varchar(80),
                         clatrxarea varchar(80),
                         cladibamt money,
                         claapproved char(1),
                         clasalary money,
                         clafcl1 money,
                         mbfdod char(10),
                         udwevtdate char(10),
                         Workflow_Id varchar(15))

Create Table #BBCRPf   (bbcrgrpno	char(3),
                        bbcrconno	char(6),
                        bbcrmvdte   char(10),
                        bbcrptdte   char(10),
                        bbcramt		money,
                        bbcrperno	char(10),
                        bbcrtype	char(1),
                        bbcrstat	char(1),
                        bbcrdoct	char(2))

Create table #PTD_casedata (
        ptd_procid int,
        ptd_casenum int,
        ptd_fldname varchar(32),
        ptd_fldvalue varchar(255))

Create table #DTH_casedata (
        dth_procid int,
        dth_casenum int,
        dth_fldname varchar(32),
        dth_fldvalue varchar(255))

Create table #wf_started (
        Workflow_Start_ID varchar(20),
        WF_Started char(10))

Create table #outstanding_addr (
        proc_id int,
        casenum int,
        stepname varchar(64))

Create table #case_information (
        proc_id int,
        casenum int,
        started char(10))

Create table #case_data (
        proc_id int,
        casenum int,
        grpno char(3),
        perno int,
        rolno int,
        deathdate char(10))

Create table #been_notified (
        casenum int)

Create table ##CLM_Progress (
        id int identity(1,1),
        msg varchar(100),
        DT datetime)

Set @sq = ''''
Set @grpno = '*'
--Set @secure_groups_only = 'n' --n for all. If y, @grpno = '*'

Set @msg = 'Starting All Claims Extract: GRPNO = ' + @grpno
Insert into ##CLM_Progress values (@msg, getdate())

If @secure_groups_only = 'y'
 Begin
    Set @msg = 'SECURE GROUPS ONLY'
    Insert into ##CLM_Progress values (@msg, getdate())
 End

--Get local Grp file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  grpgrpno, grpgrpname, grpteamcod
FROM FAWDATA.FSGRPPF '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where grpgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where grpgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Group Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsgrppf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Group Data'

--Get local Sch file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  schgrpno, schconno, prdprdname
FROM FAWDATA.FSSCHPF
Left Join FAWDATA.FSPRDPF
on schprdno = prdprdno '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where schgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where schgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Scheme Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsschpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Scheme Data'

--Get local Per file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  perperno, perinit, persurname, pergcode, codevalue, char(perdob), peridno
FROM FAWDATA.FSPERPF
left join FAWDATA.FSCODPF
on ' + @sq + @sq + 'MSTATUS' + @sq + @sq + ' = codcodtype
and permcode = codsubcode '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where perperno in (Select rolperno
                                                         FROM FAWDATA.FSROLPF
                                                         Where rolgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ') '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where perperno in (Select rolperno
                                                         FROM FAWDATA.FSROLPF
                                                         Where rolgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF))'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Person Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsperpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Person Data'

--Get local Rol file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  rolgrpno, rolperno, rolrolno, Cast(rolenddt as Char(10))
FROM FAWDATA.FSROLPF '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where rolgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ''
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where rolgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Role Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsrolpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Role Data'

--Get local Cod file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  codcodtype, codsubcode, codavalue
FROM FAWDATA.FSCODPF
where codcodtype in (' + @sq + @sq + 'DEATHCAUSE' + @sq + @sq + ') '
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Code Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fscodpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Code Data'

--Get local Mbp file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  mbpgrpno, mbpperno, mbprolno, mbpparmnm, mbpparmval
FROM FAWDATA.FSMBPPF
Where mbpparmnm in (' + @sq + @sq + 'DEATHCAUSE' + @sq + @sq +') '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and mbpgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ''
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and mbpgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Member Parameter Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsmbppf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Member Parameter Data'

--Get local Ben file
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  bengrpno, benconno, benbenno, benconref
FROM FAWDATA.FSBENPF '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where bengrpno = ' + @sq + @sq + @grpno + @sq + @sq + ''
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where bengrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Benefits Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsbenpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Benefits Data'

--Get local Mpr file for Bank Balance
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  mprgrpno, mprperno, mprrolno, Sum(mprtotunt)
FROM FAWDATA.FSMPRPF
Where mprporno = 5
  and mprtotunt <> 0 '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and mprgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ''
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and mprgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + ' Group by mprgrpno, mprperno, mprrolno '
+ @sq + ')'
Set @msg = 'Getting Member Holdings Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #fsmprpf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Member Holdings Data'

--Get all Processed CLD's
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  lthltxno, lthtype, SubStr(Char(lthindttm),1,10), lthgrpno, lthconno, lthbenno, lthperno, lthrolno, lthstatus, sthtype, sthporno, stharands, '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', 0, ' + @sq + @sq + '' + @sq + @sq + ', 0, 0, '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', lthwrkflw
FROM FAWDATA.FTLTHPF
left join FAWDATA.FTSTHPF
on lthltxno = sthltxno
Where (lthtype like ' + @sq + @sq + 'CLD%' + @sq + @sq + '
   or  lthtype like ' + @sq + @sq + 'ADJCLM%' + @sq + @sq + ')
  and lthstatus = ' + @sq + @sq + 'A' + @sq + @sq + ' '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Historic CLD Transaction Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Historic CLD Transaction Data'

--Get all Processing CLD's
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  ltxltxno, ltxtype, SubStr(Char(ltxindttm),1,10), ltxgrpno, ltxconno, ltxbenno, ltxperno, ltxrolno, ltxstatus, stxtype, stxporno, stxcrands, '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', 0, ' + @sq + @sq + '' + @sq + @sq + ', 0, 0, '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', ltxwrkflw
FROM FAWDATA.FTLTXPF
left join FAWDATA.FTSTXPF
on ltxltxno = stxltxno
Where ltxtype like ' + @sq + @sq + 'CLD%' + @sq + @sq + ' '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and ltxgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and ltxgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Active CLD Transaction Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Active CLD Transaction Data'

--Download BBCRPF records
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
select	 SubStr(crcde2,2,3)
        ,char(SubString(crcde2,5,6))
        ,char(crdtmv)
        ,char(crdtpt)
        ,crcamt
        ,char(SubString(crcde2,11,10))
        ,SubString(crtrtp,5,1)
        ,crstat
        ,crdoct
from FAWDATA.BCCRPF '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where SubStr(crcde2,2,3) = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' Where SubStr(crcde2,2,3) in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting FACS Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #BBCRPf Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting FACS Data'

Set @msg = 'Processing FACS Data'
Insert into ##CLM_Progress values (@msg, getdate())
select   bbcrgrpno	as mvgrpno
        ,bbcrconno	as mvconno
        ,bbcrmvdte	as mvdate
        ,bbcramt	as mvamt
        ,bbcrperno	as mvperno
        ,bbcrtype	as mvtype
        ,bbcrstat	as mvstat
        ,bbcrdoct	as mvdoct
into #bbcrmv
from #BBCRPf
Where  isdate(bbcrmvdte) = 1
and    isnumeric(bbcrconno) = 1
and    isnumeric(bbcrperno) = 1
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Processing FACS Data'

--Insert FACS Member Payments
Set @msg = 'Insert FACS Member Payments'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata
Select	0,
        'MEMPAYFACS',
        Convert(char(10),mvdate,120),
        mvgrpno,
        Convert(int,mvconno),
        01,
        Convert(int,mvperno),
        0,
        'A',
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
        '',
        '',
        ''
From #bbcrmv
Where mvtype in ('W', 'R', 'D')
  and mvstat = '7'
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert FACS Member Payments'
If @grpno <> '*'
 Begin
    Delete from #claimdata where clagrpno <> @grpno and clalthtype = 'MEMPAYFACS'
 End
If @secure_groups_only = 'y'
 Begin
    Delete from #claimdata where clagrpno not in (Select SecureGroupCode from securegrouptable()) and clalthtype = 'MEMPAYFACS'
 End

--Get all Processed UDR's
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  lthltxno, lthtype, SubStr(Char(lthindttm),1,10), lthgrpno, lthconno, lthbenno, lthperno, lthrolno, lthstatus, '
        + @sq + @sq + '' + @sq + @sq + ', 0, udwsumass, fthtype,
        case when fthfldold = ' + @sq + @sq + '' + @sq + @sq + ' then udwunddec else fthfldold end as fthfldold,
        fthfldnew, fthtrxarea, udwdibamt, conapprove, udwmbrsal, dtrfcl1,
        cast(mbfdod as char(10)), cast(udwevtdate as char(10)), lthwrkflw
FROM FAWDATA.FTLTHPF
left join FAWDATA.FTFTHPF
   Left join FAWDATA.FTUDWPF
   on  fthftxno = udwftxno
   and fthltxno = udwltxno
on lthltxno = fthltxno
Left join FAWDATA.FSMBFPF
on lthltxno = mbfltxno
Left join FAWDATA.FSCONPF
on lthconno = conconno
Left join FAWDATA.FSMBRPF
   Left join FAWDATA.FSDTRPF
   on  mbrgrpno = dtrgrpno
   and mbrconno = dtrconno
   and mbrbenno = dtrbenno
   and mbrclsno = dtrclsno
on  lthgrpno = mbrgrpno
and lthconno = mbrconno
and lthbenno = mbrbenno
and lthperno = mbrperno
and lthrolno = mbrrolno
Where lthtype like ' + @sq + @sq + 'UDR%' + @sq + @sq + '
  and lthstatus = ' + @sq + @sq + 'A' + @sq + @sq + '
  and udwcancel <> ' + @sq + @sq + 'Y' + @sq + @sq + ' '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Processed URD Transaction Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Processed URD Transaction Data'

--Get all Processing UDR's
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  ltxltxno, ltxtype, SubStr(Char(ltxindttm),1,10), ltxgrpno, ltxconno, ltxbenno, ltxperno, ltxrolno, ltxstatus, '
        + @sq + @sq + '' + @sq + @sq + ', 0, udwsumass, ftxtype, ftxfldold, ftxfldnew, ftxtrxarea, udwdibamt, conapprove, 0, dtrfcl1,
        cast(mbfdod as char(10)), cast(udwevtdate as char(10)), ltxwrkflw
FROM FAWDATA.FTLTXPF
left join FAWDATA.FTFTXPF
   Left join FAWDATA.FTUDWPF
   on  ftxftxno = udwftxno
   and ftxltxno = udwltxno
on ltxltxno = ftxltxno
Left join FAWDATA.FSMBFPF
on ltxltxno = mbfltxno
Left join FAWDATA.FSCONPF
on ltxconno = conconno
Left join FAWDATA.FSMBRPF
   Left join FAWDATA.FSDTRPF
   on  mbrgrpno = dtrgrpno
   and mbrconno = dtrconno
   and mbrbenno = dtrbenno
   and mbrclsno = dtrclsno
on  ltxgrpno = mbrgrpno
and ltxconno = mbrconno
and ltxbenno = mbrbenno
and ltxperno = mbrperno
and ltxrolno = mbrrolno
Where ltxtype like ' + @sq + @sq + 'UDR%' + @sq + @sq + '
  and udwcancel <> ' + @sq + @sq + 'Y' + @sq + @sq + ' '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and ltxgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and ltxgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Active URD Transaction Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Active URD Transaction Data'

--Get all Processed ACCEPT's
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
SELECT  lthltxno, lthtype, SubStr(Char(lthindttm),1,10), lthgrpno, lthconno, lthbenno, lthperno, lthrolno, lthstatus, sthtype, sthporno,
        Case When sthtype in (' + @sq + @sq + 'D' + @sq + @sq + ', '
                                + @sq + @sq + 'S' + @sq + @sq + ') then stharands * -1
             Else stharands end,
        fthtype, fthfldold, fthfldnew, fthtrxarea, 0, conapprove, mbrbensal, dtrfcl1, '
         + @sq + @sq + '' + @sq + @sq + ', '
         + @sq + @sq + '' + @sq + @sq + ', ' + @sq + @sq + '' + @sq + @sq + '
FROM FAWDATA.FTLTHPF
left join FAWDATA.FTSTHPF
on lthltxno = sthltxno
left join FAWDATA.FTFTHPF
on lthltxno = fthltxno
Left join FAWDATA.FSCONPF
on lthconno = conconno
Left join FAWDATA.FSMBRPF
   Left join FAWDATA.FSDTRPF
   on  mbrgrpno = dtrgrpno
   and mbrconno = dtrconno
   and mbrbenno = dtrbenno
   and mbrclsno = dtrclsno
on  lthgrpno = mbrgrpno
and lthconno = mbrconno
and lthbenno = mbrbenno
and lthperno = mbrperno
and lthrolno = mbrrolno
Where lthtype like ' + @sq + @sq + 'CLM%' + @sq + @sq + '
  and lthstatus = ' + @sq + @sq + 'A' + @sq + @sq + '
  and ifnull(fthstatus,' + @sq + @sq + '' + @sq + @sq + ') <> ' + @sq + @sq + 'X' + @sq + @sq
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno = ' + @sq + @sq + @grpno + @sq + @sq + ' '
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and lthgrpno in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + @sq + ')'
Set @msg = 'Getting Processed CLM Transaction Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Getting Processed CLM Transaction Data'

--Get all workflow start dates
Set @sqltext = 'Select * from OPENQUERY (MEBAS400HA,' + @sq + '
Select  trim(Cast(ci.proc_id as char(10)))||' + @sq + @sq + '-' + @sq + @sq + '||trim(Cast(ci.casenum as char(10))),
        to_char(started,' + @sq + @sq + 'yyyy-mm-dd' + @sq + @sq + ') as WF_Started
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
Where ci.proc_id in (101, 102, 105, 108, 109, 189, 54, 56, 66, 68, 87, 89, 96, 99, 252, 410) '
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
Set @msg = 'Get all workflow start dates'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #wf_started Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Get all workflow start dates'

--Insert Funeral/Family claims on workflow not yet notified on Orbit
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
where oa.proc_id = 96 '
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
Set @msg = 'Insert Funeral/Family claims on workflow not yet notified on Orbit'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #outstanding_addr Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Funeral/Family claims on workflow not yet notified on Orbit'

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
Where ci.proc_id = 96
  and ci.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 96) '
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
Set @msg = 'Insert Funeral/Family Case Information'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #case_information Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Funeral/Family Case Information'

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
Where cd.proc_id = 96
  and cd.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 96)
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
Set @msg = 'Insert Funeral/Family Case Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #case_data Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert Funeral/Family Case Data'

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
where aut.proc_id = 96
  and aut.casenum in (Select casenum from ODSSWPRO.OUTSTANDING_ADDR where proc_id = 96)
  and aut.stepname = ' + @sq + @sq + 'NOTIFCLM' + @sq + @sq + '
  and aut.type_id = 2 '
If @grpno <> '*'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n = ' + @sq + @sq + @grpno + @sq + @sq
 End
If @secure_groups_only = 'y'
 Begin
    Set @sqltext = Rtrim(@sqltext)  + ' and grp.field_value_n in (Select sengrpno from FAWDATA.FSGRPSENPF)'
 End
Set @sqltext = Rtrim(@sqltext) + ' '
+ @sq + ')'
Set @msg = 'Insert NOTIFCLM Step Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #been_notified Exec (@sqltext)
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert NOTIFCLM Step Data'

delete from #outstanding_addr
where casenum in (Select casenum from #been_notified)
delete from #case_information
where casenum in (Select casenum from #been_notified)
delete from #case_data
where casenum in (Select casenum from #been_notified)

Set @msg = 'Insert 96TYPES Data'
Insert into ##CLM_Progress values (@msg, getdate())
Insert into #claimdata
Select	0,
        '96TYPES',
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
    Delete from #claimdata where clagrpno not in(Select SecureGroupCode from securegrouptable())
 End
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Insert 96TYPES Data'
