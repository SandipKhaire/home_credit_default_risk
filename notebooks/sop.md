# 4.Roles and Responsibilities:
4.1 **Data Science/Analytics Team**
-  Lead the technical aspects of scorecard development
-  Perform data analysis, feature engineering, and model development
-  Document methodologies and technical specifications
  
4.2 **Risk Management Team**
- Define Scorecard Objective
- Review and approve scorecard design
- Oversee the implementation of scorecards in decision systems
  
4.3**Business/Product Units**
- Provide business context and requirements
- Support implementation and adoption
  
4.4 **Model Governance/Validation Team**
- Review and approve scorecards
- Oversee the model validation process
- Review periodic performance reports

4.5  **IT team**
- Implement scorecards in production systems and provide the necessary infra
- Maintain & Monitor scorecard api's in production 

# Scorecard Development Process
## Stage1:Prelimanaries & Planning
- Define the business problem clearly,specifying ,current pain points or inefficiencies.
- Define the specific objective and intended use of the scorecard(e.g., reduce defaults, improve approval rates)
- Business or Risk Manager are resposible to define clear business problem and expected solution /output from the scorecard and how the solution will get consume in the existing business workflow.
- Identify key stakeholders and their roles/depndencies.
- Identify Project risks if any like Non-availability of data/insufficient data .Because this will greatly affect the project timelines.

**Output**: Signed-off Business Requirements Document (BRD).

## Stage 2: Data Review and Project Parameters
 ### 2.1 Data Review
- Identify data sources and availability (e.g Internal/External data,prospect/bureau data,Time periods)
- Carry out the quality and quantity review of the data (i.e. to check -Do we have enough data to start the project)
- Document specific criteria for data points to be included or excluded in the scorecard
- Create a waterfall showing data movement from source to final scorecard devlopment data and Document population size at each stage of filtering.
- Only include data that represents your target population(If your scorecard will only be applied to urban residents, exclude rural data)
- Document data extraction queries and logic

### 2.2 Performance ,Sample Windows and Bad Definition

Assume a new account is approved and granted credit at a particular time, or an existing account at a particular time. At some point in time in the future, you need to determine if this account had been good or bad (to assign performance). “Performance window” is the time window where the performance of those accounts is monitored to assign class (target). “Sample window” refers to the time frame from which known good and bad cases will be selected for the scorecard development sample.
(Add a diagram)

- Ensure  the development sample is from a normal time frame and is not affected significantly by seasonality and other factors(e.g Covid Period)
-  To select stable and representative sample window, compare the key characteristic(CIBIL Score) distribution (PSI) between recent sample ((e.g., data from the past two to three months)) and the intended sample window (e.g., the reference development ).This analysis helps identify significant shifts in variable behavior, ensuring model robustness and alignment with current portfolio trends.

Definition of Bad:
- The definition must be in line with project objectives, and decision to be made. If the objective is to increase profitability, then the definition must be set at a delinquency point where the account becomes unprofitable.
- Using Roll Rate and vintage analysis tool define optimal target(bad) definition for scorecard devlopment .Also carry out coverage analysis ensuring that your chosen target variable aligns seamlessly with PFL's portfolio.
- The target definition must meet a minimum capture rate(% of eventual bad cases flagged by the candidate definition) and conversion rate(% of accounts under the candidate definition that become eventual bad.) of 70% against an eventual bad benchmark (e.g.,90+DPD, 180+ DPD, charge-off, or write-off).If not, document deviations and justify.
- The development sample must contain ≥1,000 "bad" cases under the selected target definition.If the count falls below 1,000 then document- Exact number of bad cases available,Justification for proceeding .
- Define Indeterminate accounts :those that do not conclusively fall into either the good or bad definition.If the number of indeterminates is very low, they can be excluded or all assigned as good.
- Define if segmented model required with required segments.

Final bad definition and sample window,segments ,devlopement data(Train/Test/OOT) summary requires sign-off from Model Risk Management and Business Stakeholders.



## Stage 3: Devlopment Data Feature set Creation
- Detailed list of characteristics/features, from internal and external sources, required in the development sample 
- Derived characteristics, with details on exact calculations and logic.







