## Software Cost & Costing

## Outline

Lesson

1. Software cost estimation

2. Cost structure in software lifecycle

## 14.1 Software cost estimation

##  Cost

In business, the cost may be one of acquisition, in which case the amount of money expended to acquire it is counted as cost. In this case, money is the input that is gone in order to acquire software.

In software development, the cost is the value of money that has been used up to design & produce software or deliver an information service to users, and hence is not available for use anymore.

This acquisition cost may be the sum of the cost of production as incurred by the original producer, and further costs of transaction as incurred by the acquirer over and above the price paid to the producer.

Cost is not as same as price, usually, the price also includes a mark-up for profit over the cost of software production.

In software engineering, cost estimation is the first step of software engineering management and your business.

## 14.1 Software cost estimation

## Fundamental questions about software cost estimation

– How much effort is required to complete an activity?

– How much calendar time is needed to complete an activity?

What is the cost of an activity?

– What is the total cost of a software product production?

– Project estimation and scheduling are interleaved management activities.

## Components of software cost

– Hardware costs and software costs.

– Travel and training costs.

– Effort costs (the dominant factor in most projects)

• The salaries of engineers involved in the project;

• Social and insurance costs.

– Effort costs must take overheads into account

• Costs of building, heating, lighting.

• Costs of networking and communications.

• Costs of shared facilities (e.g library, staff restaurant, etc.).

## 14.1 Software cost estimation

## Techniques of software cost estimation

<table><tr><td>Algorithmic cost modelling</td><td>A model based on historical cost information that relates some software metric (usually its size) to the project cost is used. An estimate is made of that metric and the model predicts the effort required.</td></tr><tr><td>Expert judgement</td><td>Several experts on the proposed software development techniques and the application domain are consulted. They each estimate the project cost. These estimates are compared and discussed. The estimation process iterates until an agreed estimate is reached.</td></tr><tr><td>Estimation by analogy</td><td>This technique is applicable when other projects in the same application domain have been completed. The cost of a new project is estimated by analogy with these completed projects. Myers (Myers 1989) gives a very clear description of this approach.</td></tr><tr><td>Parkinson&#x27;s Law</td><td>Parkinson&#x27;s Law states that work expands to fill the time available. The cost is determined by available resources rather than by objective assessment. If the software has to be delivered in 12 months and 5 people are available, the effort required is estimated to be 60 person- months.</td></tr><tr><td>Pricing to win</td><td>The software cost is estimated to be whatever the customer has available to spend on the project. The estimated effort depends on the customer&#x27;s budget and not on the software functionality.</td></tr></table>

## 14.1 Software cost estimation

## Estimation methods

• Each method has strengths and weaknesses.

Estimation should be based on several methods.

• If these methods do not return approximately the same result, then you have insufficient information available to make an estimate.

• Some actions should be taken to find out more in order to make more accurate estimates.

• Pricing to win is sometimes the only applicable method.

## 14.1 Software cost estimation

## Pricing to win

• The project costs whatever the customer has to spend on it.

Advantages:

– You will get the contract in Tendering and Bidding.

Disadvantages:

The probability that the customer gets the system, he or she wants is small. Costs do not accurately reflect the work required.

However, when detailed information is lacking, it may be the only appropriate strategy.

• The project cost is agreed on the basis of an outline proposal and the development is constrained by that cost.

• A detailed specification may be negotiated or an evolutionary approach used for system development.

## 14.1 Software cost estimation

## Algorithmic cost modelling

• Cost is estimated as a mathematical function of product, project and process attributes whose values are estimated by project managers:

$$
- \mathrm {  ~ \sf ~ E F f o r t } = \sf A _ { \mathrm { ~ } } ^ { \mathrm { ~ * ~ } } S i z e ^ { \mathrm {  ~ B ~ } * } \sf N
$$

– A is an organisation-dependent constant,

B reflects the disproportionate effort for large projects

– M is a multiplier reflecting product, process and people attributes.

• The most commonly used product attribute for cost estimation is software code size.

• Most models are similar, but they use different values for A, B and M.

## 14.1 Software cost estimation

## National Standard in software cost estimation

Chinese National Standard (GB/T 36964-2018)

Software engineering specification for software development cost measurement

Three methods for software development cost estimation：

$\mathrm { S D C } = \mathrm { D H C } + \mathrm { D N C } + \mathrm { I H C } + \mathrm { I N C }$

. $\mathrm { S D C } = \ \sum _ { i = 1 } ^ { n } ( E _ { i } \times F _ { i } ) \quad + \mathrm { D N C }$

. $\mathrm { S D C } = \mathbf { P } \mathbf { \times } \mathbf { S } + \mathbf { D N C }$

<!-- image-->

中华人民共和国国家标准

GB/T36964-2018

## 软件工程软件开发成本度量规范

Software engineering—Specification for softwaredevelopment cost measurement

## 14.1 Software cost estimation

## Components of Software Cost in GB/T 36964-2018

<!-- image-->

Direct labor cost can be got from FPA.

Question: How to distinguish direct cost from indirect cost ?

## Answer:

When the project is terminated or cancelled, check whether the relevant expenses will continue to be incurred. If so, they are indirect expenses, otherwise the relevant expenses are no longer incurred, they are direct costs.

## 14.1 Software cost estimation

## Methods of software development cost estimation

Method 1: Calculate direct labor costs, direct non-labor costs, indirect labor costs and indirect non-labor costs according to the software cost components, and then sum them up to calculate the software development cost.

$$
\mathrm { S D C } = \mathbf { D H C } + \mathbf { D N C } + \mathbf { I H C } + \mathbf { I N C }
$$

In the above formula: SDC is the software development cost; DHC is the direct labor cost; DNC is the direct non-labor cost; IHC is the indirect labor cost; INC is the indirect non-labor cost.

Method 2: Based on the workload estimation results and the average labor cost rate, directly calculate the sum of direct labor costs and indirect costs, and then add the direct non-labor costs to obtain the software development cost.

$$
\mathbf { S D C } = \sum _ { i = 1 } ^ { n } ( E _ { i } \times F _ { i } ) + \mathbf { D N C }
$$

In the above formula: SDC is the software development cost; n is the number of personnel categories; Ei is the workload of the i-th category of personnel; Fi is the labor cost rate of the i-th category of personnel; DNC is the direct non-labor cost. 10

## 14.1 Software cost estimation

## Methods of software development cost estimation

Method 3: Based on the scale estimation results and scale comprehensive unit price, the sum of direct labor costs and indirect costs is directly calculated, and then added to the direct non-labor costs, the software development cost is obtained.

$$
\mathbf { S D C } = \mathbf { P } \mathbf { \times } \mathbf { S } + \mathbf { D N C }
$$

In the above formula: SDC is the software development cost; P is the scale comprehensive unit price (yuan/per function point); S is the software scale (function point); DNC is the direct non-labor cost.

## 14.1 Software cost estimation

## Process of software cost estimation

The following steps can be used in software cost estimation:

. Get software size.

• Select a suitable productivity standards (in HH/FP, or HM/FP).

• Convert to calendar time according to the productivity standard.

Obtain software cost - monetary measurement.

Documentation and report.

## Productivity cases

. Real-time embedded systems：40～160 LOC/P-month.

Systems programs：150～400 LOC/P-month.

： Commercial applications：200～900 LOC/P-month.

• In Object Points, productivity has been measured between

• 4 ～50 object points/month depending on tool support and developer capability.

## 14.1 Software cost estimation

## Estimating methods in development phase

<!-- image-->  
1 U.1 uIいU1 U1∠

## 14.1 Software cost estimation

## Estimation accuracy

• The size of a software system can only be known accurately when it is finished.

• Several factors influence the final size

– Use of COTS and components

– Programming language

– Distribution of system

• As the development process progresses then the size estimate becomes more accurate.

## 14.1 Software cost & costing

## Economic cost vs Accounting cost

One type of cost is explicit cost, also known as accounting cost, which can be measured in currency, such as employee wages.

Another type of cost is implicit cost, which cannot be directly reflected on the book and is therefore difficult to accurately measure. For example, opportunity cost is an implicit cost.

<!-- image-->

## 14.1 Software cost & costing

## Case: Economic cost vs Accounting cost

Accurate measurement of software cost is one of the key factors for the success of a software project or product.

The steps for estimating software cost include:

• First, identify the true cost driver of a certain business;

Second, calculate the cost driver rate of the business;

• Third, multiply the first two factors to obtain the accuracy of the cost;

• Fourth, verify the estimated results of the cost in the previous steps, continuously improving in order to effectively monitor & control costs.

Example: A company, already has an off-line physical bookstore, plans to set up a new online bookstore.

Question: What are the costs of opening an online bookstore?

Tip: pay attention to implicit cost and opportunity cost

## 14.2 Cost structure in software lifecycle

## Cost structure of software in its lifecycle

Maintenance cost is main part of the total cost in software life-cycle.

<!-- image-->  
Estimated Generic Software Major Cost CostbyPhase LifeCycle

<!-- image-->

<!-- image-->

<!-- image-->  
ReworkCaused byPoorQuality

<!-- image-->

## 14.2 Cost structure in software lifecycle

## Cost structure of software in its lifecycle Cost of defects and the hidden-cost of software.

Cost of Defects  
<!-- image-->  
The more time we save your team,the more time they have to find bugs sooner.  
That Saves Money

## Core concepts & Assignments

## Core Concepts

Software development cost estimation standard (GB/T 36964-2018)

Methods of software cost estimation

Economic cost &Accounting cost

Cost structure of software lifecycle

## Assignment

Learn Software Engineering Economics(软件工程经济学) MOOC Chapter 3, the linkage is

https://coursehome.zhihuishu.com/courseHome/1000050734#teachTeam