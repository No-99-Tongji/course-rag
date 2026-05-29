## 13.1 Software Size Measurement

##  Function Point Counting Procedure

An enhancement project function point count is the activity of applying the Functional Size Measurement (FSM) Method to measure the functional size of an enhancement project. It includes all the functions being added, changed, and deleted. It also includes conversion functions developed as part of the enhancement project.

A development project is often estimated a number of times before its completion (see following Figure). At the time of completion, a final development project count is measured, and an application count is determined. Later, enhancements to that application can be estimated until their completion. Upon completion of each enhancement project, a final enhancement project count is measured, and the application count is modified to reflect the changes.

<!-- image-->

## 13.1 Software Size Measurement

## Use of FPM: application vs project

## Functional size of a new development applications

This pertains to the functional size of applications in the process of being built or that have already been built at the request of a user or user organization, and that provide a solution to the needs or wishes of the user or user organization.

If the application in a development project is realized in a single project, determining the functional size of an application does not occur differently than when determining the functional size of a project. Notice, however, that the size of any conversion software shall not be counted when the functional size of an application is determined.

If the application is being realized in the form of a number of sub-projects carried out in parallel, then the total functionality furnished by all the sub-projects will have to be examined in order to determine the functional size of an application. When examining these sub-projects, make sure that functionality appearing in more than one sub-project (such as a logical file) is not counted twice.

## 13.1 Software Size Measurement

## Use of FPM: application vs project

## Functional size of enhanced applications

Step1: Determine the number of function points of the application before the change (AFPB).

Step2: Identify which transactions and/or logical files are added to the application and establish how many function points they represent (ADD).

Step3: Determine which transactions and/or logical files are deleted from the existing application and count how many function points they represent (DEL).

Step4: Establish which transactions and/or logical files change. Then determine the number of function points that they represent before the change (CHGB) and after the change (CHGA).

Step5: Determine the functional size of the application after the enhancement (AFPA) as follows:

$$
\mathsf { A F P A } = [ \mathsf { A F P B } + \mathsf { A D D } - \mathsf { D E L } + ( \mathsf { C H G A } - \mathsf { C H G B } ) ]
$$

## 13.1 Software Size Measurement

## Use of FPM: application vs project

## Functional size of enhancement projects

An enhancement project considers enhancements to one or more existing applications. This means that functionality can be added to, changed in, and deleted from these applications. The steps required to determine the functional size of the project in function points are as follows.

Step1: Identify which transactions and/or logical files are going to be added to the application(s) and establish how many function points they represent (ADD).

Step2: Determine which transactions and/or logical files are going to be deleted from the existing application(s) and determine how many function points they represent (DEL).

Step3: Establish which transactions and/or logical files change. Then determine the number of function points they represent after the change (CHGA).

Step4: Calculate the functional size for the enhancement project as follows (EFP):

$$
\mathsf { E F P } = \mathsf { A D D } + \mathsf { D E L } + \mathsf { C H G A }
$$

## 13.1 Software Size Measurement

## Use of FPM: Application vs Project

Table13.1 Functional Size of a project versus an application
<table><tr><td rowspan=2 colspan=1>Size type</td><td rowspan=1 colspan=5>Lifecyclestage</td></tr><tr><td rowspan=1 colspan=1>Initial release</td><td rowspan=1 colspan=2>Release 1</td><td rowspan=1 colspan=2>Release 2</td></tr><tr><td rowspan=1 colspan=1>ADD</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=2>200</td><td rowspan=1 colspan=2>500</td></tr><tr><td rowspan=1 colspan=1>DELETE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>40</td><td rowspan=1 colspan=2>100</td></tr><tr><td rowspan=1 colspan=1>BeforeCHANGEAfter</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>80100</td><td rowspan=1 colspan=2>220200</td></tr><tr><td rowspan=1 colspan=1>Project size</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>ADDCHANGEAfterDELETETOTAL</td><td rowspan=1 colspan=1>20010040340</td><td rowspan=1 colspan=1>ADDCHANGEAfterDELETETOTAL</td><td rowspan=1 colspan=1>500200100800</td></tr><tr><td rowspan=1 colspan=1>Application size</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>InitialreleaseADDCHANGEAfterCHANGEBeforeDELETETOTAL</td><td rowspan=1 colspan=1>1000+200+100-80-401180</td><td rowspan=1 colspan=1>Release1ADDCHANGEAfterCHANGEBeforeDELETETOTAL</td><td rowspan=1 colspan=1>1180+500+200-220-1001560</td></tr></table>

## 13.1 Software Size Measurement

The cone of uncertainty of estimation

<!-- image-->

## 13.1 Software Size Measurement

## Estimating methods in development phase

<!-- image-->

## 13.1 Software Size Measurement

## Case study

<!-- image-->

## 13.1 Software Size Measurement

## Case study

## Calculation of CFP Crude Function Points

Analysis of the software system as presented in the DFD summarizes the number of the various components:

Number of user inputs = 2

Number of user outputs = 3

Number of user online queries = 3

Number of logical files = 2

Number of external interfaces = 2

The degree of complexity (simple, average or complex) was evaluated for each component.

## 13.1 Software Size Measurement

##  Case study

The ATTEND MASTER - CFP calculation form
<table><tr><td rowspan=4 colspan=1>Softwaresystemcomponents</td><td rowspan=1 colspan=9>Complexity level</td><td rowspan=4 colspan=1>TotalCFP</td></tr><tr><td rowspan=1 colspan=3>Simple</td><td rowspan=1 colspan=3>average</td><td rowspan=1 colspan=3>complex</td></tr><tr><td rowspan=1 colspan=1>Count</td><td rowspan=1 colspan=1>WeightFactor</td><td rowspan=1 colspan=1>Points</td><td rowspan=1 colspan=1> Count</td><td rowspan=1 colspan=1>WeightFactor</td><td rowspan=1 colspan=1>Points</td><td rowspan=1 colspan=1>Count</td><td rowspan=1 colspan=1>WeightFactor</td><td rowspan=1 colspan=1>Points</td></tr><tr><td rowspan=1 colspan=1>A</td><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>C=AxB</td><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1>E</td><td rowspan=1 colspan=1>F=DxE、</td><td rowspan=1 colspan=1>G</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>FGxH</td></tr><tr><td rowspan=1 colspan=1>User inputs</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>!!</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>、</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>User outputs</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>---</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>17</td></tr><tr><td rowspan=1 colspan=1>User.onlinequeries</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>13</td></tr><tr><td rowspan=1 colspan=1>Logical files</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>!</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>!</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>22</td></tr><tr><td rowspan=1 colspan=1>Externalinterfaces</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>！</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>!!</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>Total CFP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>81</td></tr></table>

## 13.1 Software Size Measurement

## Case study

The ATTEND MASTER - RCAF calculation form
<table><tr><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Subject</td><td rowspan=1 colspan=1>Grade</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Requirement for reliable backup and recovery</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Requirement for data communication</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Extent of distributed processing</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Performance requirements</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Expected operational environment</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Extent of online data entries</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Extent of multi-screen or multi-operation online data input</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Extent of online updating of master files</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Extent of complex inputs, outputs, online queries and files</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Extent of complex data processing</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>Extent that currently developed code can be designed for reuse</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>Extent of conversion and installation included in the design</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1> Extent of multiple installations in an organization and variety of customerorganizations</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>Extent of change and focus on ease of use</td><td rowspan=1 colspan=1>012345</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Total=RCAF</td><td rowspan=1 colspan=1>41</td></tr></table>

## 13.1 Software Size Measurement

## Case study

The ATTEND MASTER – Function points calculation

$$
\mathsf { F P } = \mathsf { C F P } \times ( 0 . 6 5 + 0 . 0 1 \times \mathsf { R C A F } )
$$

$$
\mathsf { F P } = \mathrm { ~ \mathbb { S } ~ } | \mathrm { ~ } \times ( 0 . 6 5 + 0 . 0 1 \times 4 1 ) = 8 5 . 8 6
$$

## Core concepts & Assignments

## Core Concepts

Methods of software size measurement

Function Point Analysis and its standards

## Assignment

Learn Chapter 3 of Software Engineering Economics(软件工程经济学) MOOC. The linkage is as follow

https://coursehome.zhihuishu.com/courseHome/1000050734#teachTeam