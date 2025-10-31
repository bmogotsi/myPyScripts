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
Update ##CLM_Progress set msg = Rtrim(msg) + ': ' + ltrim(rtrim(convert(char(10),@@rowcount))) + ' records loaded' where msg = 'Processing FACS Data