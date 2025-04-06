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
- Also check if reject inferencing is needed or not(Critical for Bias Mitigation) and also clearly document the reject inference method which is used.

Final bad definition and sample window,segments ,devlopement data(Train/Test/OOT) summary requires sign-off from Model Risk Management and Business Stakeholders.



## Stage 3: Devlopment Data Feature set Creation
- Detailed list of characteristics/features, from internal and external sources, required in the development sample 
- Derived characteristics, with details on exact calculations and logic.
- Mentioned the source of features (bureau,applications,Account aggregator)


### **Stage 4: Scorecard Development**  

#### **4.1 Exploratory Data Analysis (EDA)**  
- Perform **univariate analysis** (distributions) and **bivariate analysis** (correlation,IV, trend validation).  
- Identify and treat **missing values** (e.g., imputation, exclusion) and **outliers** (winsorization/capping).  
- Document treatment logic (e.g., "Missing values imputed with median for numerical variables; categorical variables treated as a separate category").  

#### **4.2 Variable Selection**  
1. **Initial Screening**:  
   - Remove **constant variables** (Var(feature) = 0).  
   - Exclude features with **>80% missing values** (unless imputed with justification).  
   - Avoid absolute amount-based variables (e.g., *total unsecured sanctioned amount*). Prefer **normalized ratios** (e.g., *current balance unsecured / total sanctioned amount for live loans*).  

2. **Correlation Check**:  
   - Eliminate highly correlated features (**corr > 0.7**) to reduce multicollinearity.  

3. **IV-Based Selection**:  
   - Retain variables with **IV ≥ 0.03 (3%) and IV ≤ 0.5 (50%)** to ensure predictive power without overfitting.  
   - Validate logical risk trends (e.g., higher credit utilization → higher risk). Remove illogical variables (e.g., *older customers riskier than younger* without business rationale).  

4. **Diverse Feature Representation**:  
   - Include features from **multiple risk dimensions** for stability:  
     - **Bureau Data**: Enquiries, delinquencies, trade performance, utilization, vintage, payment recency.  
     - **Transactional Data**: Cash flow patterns, bounce rates.  
     - **Demographic/Behavioral Data**: Income stability, employment vintage.
     
 (Note: Data points subject to availability)

 5. Check Characteristic Stability Index (CSI) between Train and OOT (Out-of-Time) samples:CSI ≤ 10%: Accept variable (stable across time).


### **4.3 Model Development**  

#### **1. Algorithm Selection**  
- **Traditional Approach**: WOE-based Logistic Regression (Baseline) – Preferred for interpretability and compliance.  
- **Advanced ML Models** : XGBoost/CatBoost: Handle non-linear relationships; use SHAP values for explainability.  
 

#### **2. Performance Validation**  
- **Metrics to Document**:  
  | **Metric**  | **Benchmark** |  
  |----------|---------------|  
  | **KS**     |  ≥ 0.20        |  
  | **GINI**   | ≥ 0.35        |  
  | **AUC-ROC**|≥ 0.60        |  

- **Risk Ranking Table**:  
  - Ensure monotonic risk increase across score bands .  

#### **3. Scorecard Scaling**  
- **Convert Probability to 3-Digit Score**:  
  - Formula: `Score = Offset + Factor * ln(odds)`  
  - **Example**:  
    - Set `Odds = 50:1` or averate bad rate  at Score 600 and `PDO (Points to Double Odds) = 20`.  
    - Calculate: `Factor = PDO / ln(2)`, `Offset = Score – (Factor * ln(50))`.  
  - **Document**: Scaling parameters (Offset, Factor, PDO) and business rationale.  

#### **4. Stability Checks**  
- **Population Stability Index (PSI)**:  
  - **Threshold**: PSI ≤ 0.10 (Stable), 0.10–0.25 (Investigate), >0.25 (Reject).  
  - **Action**: Recalibrate if PSI > 0.25 between Train/OOT.  
  - **Formula**:  
    ```  
    PSI = Σ [(%OOT − %Train) * ln(%OOT/%Train)]  
    ```  





![alt text](image.png)