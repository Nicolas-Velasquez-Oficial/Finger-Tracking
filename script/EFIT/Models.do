clear all
cap log close
set more off
cls
capture noisily cf


if "`c(username)'"=="juan.velasquez" gl path "C:\Users\PERSONAL\OneDrive - Universidad de los Andes\Maestria\Tesis\Finger-Tracking\script\EFIT"
else{	
	*cd "COPIE AQUÍ LA RUTA DE SU DIRECTORIO"
	* No cree un global data para que Stata busque las bases en su directorio
	cd "C:\Users\juan.velasquez\OneDrive - Universidad de los andes\Maestria\Tesis\Finger-Tracking\script\EFIT"
}

 

import delimited prosocial_merged_total.csv, bindquote(strict) case( preserve) encoding(utf8) 

encode par  , g(Pair)
encode Faculty , g(Carrer)


global sociodemograficas RT MT semester age gender_y Harmedbytheconflict ///
Affectedphysicallypsycologically Affecteddirectlyindirectlybythec ///
Familyaffectedbytheconflict Conflictknowledge Conflicthistoryknowledge ///
PeacejurisdictionJEPknowledge PeacejurisdictionJEPchangesknowl HomosexualMarrige ///
Adoptionbyhomosexualcouples Euthanasialegalization Abortionlegalization ///
Marijuanalegalization Flexiblegenderroles i.Carrer



**********Tables for Journal****************************************************
********************************************************************************
**********Dependent standarizadas for conviction proxy**************************
preserve
sum csi zeta1 zeta2
g csi_conviction= ((csi-.1856129 )/.2491943)*-1
g zeta1_conviction= ((zeta1-.0218141)/.068139 )*-1
g zeta2_conviction= ((zeta2-.0428116 )/.0993172)*-1

*hist csi_conviction
*hist zeta1_conviction
*hist zeta2_conviction

***Results tables with fixed effects by id and trial for csi, zeta1 and zeta2***

xtset id_x trial, g
xtdescribe 

xtreg csi_conviction ib(15).Pair Log_RT Log_MT, fe 
est store csi_conviction

xtreg zeta1_conviction ib(15).Pair Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(15).Pair Log_RT Log_MT , fe
est store zeta2_conviction

ssc install outreg2

outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Prosocial_conviction.doc , tex replace append label dec(3)
*******************************Interaction T and Response **********************
*********************************xi*********************************************

xtreg csi_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT  , fe 
est store csi_conviction_tot

xtreg csi_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, fe
est store csi_conviction_exg

xtreg csi_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, fe
est store csi_conviction_exp

xtreg csi_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, fe
est store csi_conviction_vic

xtreg csi_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==13 | Pair==14| Pair==16| Pair==15, fe
est store csi_conviction_stu
ssc install outreg2

outreg2 [csi_conviction_tot  csi_conviction_exg csi_conviction_exp csi_conviction_vic csi_conviction_stu] using Prosocial_csi_conviction.doc , tex replace append label dec(3)

*********************************Z1*********************************************

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT  , fe 
est store zeta1_conviction_tot

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, fe
est store zeta1_conviction_exg

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, fe
est store zeta1_conviction_exp

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, fe
est store zeta1_conviction_vic

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==13 | Pair==14| Pair==16| Pair==15, fe
est store zeta1_conviction_stu
ssc install outreg2

outreg2 [zeta1_conviction_tot  zeta1_conviction_exg zeta1_conviction_exp zeta1_conviction_vic zeta1_conviction_stu] using Prosocial_zeta1_conviction.doc , tex replace append label dec(3)
*********************************Z2*********************************************

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT  , fe 
est store zeta2_conviction_tot

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, fe
est store zeta2_conviction_exg

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, fe
est store zeta2_conviction_exp

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, fe
est store zeta2_conviction_vic

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp Log_RT Log_MT if Pair==13 | Pair==14| Pair==16| Pair==15, fe
est store zeta2_conviction_stu
ssc install outreg2

outreg2 [zeta2_conviction_tot  zeta2_conviction_exg zeta2_conviction_exp zeta2_conviction_vic zeta2_conviction_stu] using Prosocial_zeta2_conviction.doc , tex replace append label dec(3)
*******************************Robust WITH**************************************
****************************SOCIODEMOGRAPHIC CONTROLS***************************
*********************************xi*********************************************

xtreg csi_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas  , fe 
est store csi_conviction_tot

xtreg csi_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, be
est store csi_conviction_exg

xtreg csi_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, be
est store csi_conviction_exp

xtreg csi_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, be
est store csi_conviction_vic

xtreg csi_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==13 | Pair==14| Pair==16| Pair==15, be
est store csi_conviction_stu
ssc install outreg2

outreg2 [csi_conviction_tot  csi_conviction_exg csi_conviction_exp csi_conviction_vic csi_conviction_stu] using Prosocial_csi_conviction_SOCIO.doc , tex replace append label dec(3)

*********************************Z1*********************************************

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas  , be
est store zeta1_conviction_tot

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, be
est store zeta1_conviction_exg

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, be
est store zeta1_conviction_exp

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, be
est store zeta1_conviction_vic

xtreg zeta1_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==13 | Pair==14| Pair==16| Pair==15, be
est store zeta1_conviction_stu
ssc install outreg2

outreg2 [zeta1_conviction_tot  zeta1_conviction_exg zeta1_conviction_exp zeta1_conviction_vic zeta1_conviction_stu] using Prosocial_zeta1_conviction_SOCIO.doc , tex replace append label dec(3)
*********************************Z2*********************************************

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas  , fe 
est store zeta2_conviction_tot

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==1 | Pair==2 | Pair==3| Pair==4| Pair==15, be
est store zeta2_conviction_exg

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==5 | Pair==6 | Pair==7| Pair==8| Pair==15, be
est store zeta2_conviction_exp

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==9 | Pair==10 | Pair==11| Pair==12| Pair==15, be
est store zeta2_conviction_vic

xtreg zeta2_conviction ib(15).Pair##ib(2).sideResp $sociodemograficas if Pair==13 | Pair==14| Pair==16| Pair==15, be
est store zeta2_conviction_stu
ssc install outreg2

outreg2 [zeta2_conviction_tot  zeta2_conviction_exg zeta2_conviction_exp zeta2_conviction_vic zeta2_conviction_stu] using Prosocial_zeta2_conviction_SOCIO.doc , tex replace append label dec(3

restore

********************************************************************************
**********Tabals de resultados con efectos fijos para csi-conviction, zeta1-conviction y zeta2-conviction********
*****************************Side_resp_1 Solo desiciones Prosociales***************
preserve
keep if sideResp==1
sum psi csi zeta1 zeta2
g psi_conviction= ((psi- .2412065  )/.2756077 )*-1
g csi_conviction= ((csi- .1933447  )/.2386284 )*-1
g zeta1_conviction= ((zeta1-.045862)/.0916293 )*-1
g zeta2_conviction= ((zeta2-.0019999)/.0251537 )*-1

sum csi_conviction zeta1_conviction zeta2_conviction

xtset id_x trial, g
xtdescribe 

xtreg csi_conviction ib(15).Pair RT MT , fe
est store csi_conviction

xtreg zeta1_conviction ib(15).Pair RT MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(15).Pair RT MT, fe
est store zeta2_conviction

ssc install outreg2

outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Prosocial_side1_conviction.doc , tex replace append label dec(3)


xtreg csi_conviction ib(15).Pair $sociodemograficas ,re
est store csi_conviction

xtreg zeta1_conviction ib(15).Pair $sociodemograficas ,re
est store zeta1_conviction

xtreg zeta2_conviction ib(15).Pair $sociodemograficas ,re
est store zeta2_conviction
outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Prosocial_side1_conviction_controls.doc , tex replace append label dec(3)

restore
*********Tabals de resultados con efectos fijos para csi-conviction, zeta1-conviction y zeta2-conviction*********
*****************************Side_resp_1 Solo desiciones Egositas************
preserve
keep if sideResp==2
sum csi zeta1 zeta2
g csi_conviction= ((csi- .1792949  )/.257369  )*-1
g zeta1_conviction= ((zeta1-.0021637)/.0268111)*-1
g zeta2_conviction= ((zeta2-.0761603 )/.1222112)*-1
xtset id_x trial, g

xtreg csi_conviction ib(15).Pair Log_RT Log_MT, fe
est store csi_conviction

xtreg zeta1_conviction ib(15).Pair Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(15).Pair Log_RT Log_MT, fe
est store zeta2_conviction

ssc install outreg2

outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Prosocial_side2_conviction.doc , tex replace append label dec(3)

xtreg csi_conviction ib(15).Pair $sociodemograficas ,be
est store csi_conviction

xtreg zeta1_conviction ib(15).Pair $sociodemograficas ,be
est store zeta1_conviction

xtreg zeta2_conviction ib(15).Pair $sociodemograficas ,be

est store zeta2_conviction
outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Prosocial_side2_conviction_controls.doc , tex replace append label dec(3)
restore


********************************Risk Model**************************************
clear
import delimited risk_merged_total.csv, bindquote(strict) case( preserve) encoding(utf8) 

*encode par  , g(Pair)
encode GS , g(id_2)
encode Faculty , g(Carrer)

g Log_RT = ln(RT)
g Log_MT = ln(MT)

global sociodemograficas Log_RT Log_MT semester age gender_y Harmedbytheconflict ///
Affectedphysicallypsycologically Affecteddirectlyindirectlybythec ///
Familyaffectedbytheconflict Conflictknowledge Conflicthistoryknowledge ///
PeacejurisdictionJEPknowledge PeacejurisdictionJEPchangesknowl HomosexualMarrige ///
Adoptionbyhomosexualcouples Euthanasialegalization Abortionlegalization ///
Marijuanalegalization Flexiblegenderroles i.Carrer


**********Dependent standarized for conviction proxy***************************
* Risk aversion in WIN
preserve

keep if subjID_x==1
sum csi zeta1 zeta2
g csi_conviction= ((csi-.1771703)/.2442217)*-1
g zeta1_conviction= ((zeta1-.0387018 )/.0872266)*-1
g zeta2_conviction= ((zeta2-.0211913 )/.0749562)*-1

xtset id_2 trial, g
xtdescribe 

xtreg csi_conviction ib(1).sideResp Log_RT Log_MT, fe 
est store csi_conviction

xtreg zeta1_conviction ib(1).sideResp Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(1).sideResp Log_RT Log_MT, fe
est store zeta2_conviction
outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Risk_Win_conviction.doc , tex replace append label dec(3)
restore

*  Risk aversion in Loose
preserve
keep if subjID_x==0
sum csi zeta1 zeta2
g csi_conviction= ((csi-.1776419 )/.2599726 )*-1
g zeta1_conviction= ((zeta1-.0158286 )/.0616962 )*-1
g zeta2_conviction= ((zeta2-.0551398 )/ .1060186)*-1


xtset id_2 trial, g
xtdescribe 

xtreg csi_conviction ib(1).sideResp Log_RT Log_MT, fe 
est store csi_conviction

xtreg zeta1_conviction ib(1).sideResp Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(1).sideResp Log_RT Log_MT , fe
est store zeta2_conviction
outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Risk_Loose_conviction.doc , tex replace append label dec(3)
restore
*********************************************************************************
preserve
gen Win =0
replace Win=1 if subjID_x==1
g csi_conviction= ((csi-.1774078 )/.2522356)*-1
g zeta1_conviction= ((zeta1-.0271833  )/.0763073)*-1
g zeta2_conviction= ((zeta2-.0382871 )/ .09346)*-1
xtset id_2 trial, g
xtdescribe 

xtreg csi_conviction ib(1).sideResp##ib(0).Win Log_RT Log_MT, fe 
est store csi_conviction

xtreg zeta1_conviction ib(1).sideResp##ib(0).Win Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(1).sideResp##ib(0).Win Log_RT Log_MT , fe
est store zeta2_conviction

restore

**************************TEMPORAL MODEL****************************************

clear
import delimited temporal_merged_total.csv, bindquote(strict) case( preserve) encoding(utf8) 

*encode par  , g(Pair)
encode GS , g(id_2)
encode Faculty , g(Carrer)
sum csi zeta1 zeta2
g csi_conviction= ((csi-.1693994)/.2390434)*-1
g zeta1_conviction= ((zeta1-.0266156)/.0742551)*-1
g zeta2_conviction= ((zeta2-.0341687)/.0890668 )*-1

g Log_RT = ln(RT)
g Log_MT = ln(MT)

global sociodemograficas Log_RT  Log_MT semester age gender_y Harmedbytheconflict ///
Affectedphysicallypsycologically Affecteddirectlyindirectlybythec ///
Familyaffectedbytheconflict Conflictknowledge Conflicthistoryknowledge ///
PeacejurisdictionJEPknowledge PeacejurisdictionJEPchangesknowl HomosexualMarrige ///
Adoptionbyhomosexualcouples Euthanasialegalization Abortionlegalization ///
Marijuanalegalization Flexiblegenderroles i.Carrer


xtset id_2 trial, g
xtdescribe 

xtreg csi_conviction ib(1).sideResp Log_RT Log_MT, fe 
est store csi_conviction

xtreg zeta1_conviction iib(1).sideResp Log_RT Log_MT, fe
est store zeta1_conviction

xtreg zeta2_conviction ib(1).sideResp Log_RT Log_MT , fe
est store zeta2_conviction

outreg2 [csi_conviction zeta1_conviction zeta2_conviction] using Temporal_conviction.doc , tex replace append label dec(3)
