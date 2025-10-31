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

-- Rest of the original procedure content...