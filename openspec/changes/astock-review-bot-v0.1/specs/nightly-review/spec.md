# Spec: Nightly Review

## ADDED Requirements

### Requirement: Scheduled Nightly Review

The system SHALL generate a nightly review report at 21:30 Asia/Shanghai on trading days.

#### Scenario: Review job runs at configured time

- GIVEN the configured review time is `21:30`
- WHEN the scheduler reaches the configured time on a trading day
- THEN the system SHALL start the nightly review job

### Requirement: Main-board Stock Universe

The system SHALL only include Shanghai/Shenzhen main-board common stocks in v0.1.

#### Scenario: Candidate stock is outside allowed prefixes

- GIVEN a model output includes a stock code outside `600`, `601`, `603`, `605`, `000`, `001`, `002`, or `003`
- WHEN the risk filter validates candidates
- THEN the system SHALL reject that candidate

### Requirement: Structured Trade Plan

The system SHALL require a structured trade plan before generating the final report.

#### Scenario: Candidate has no stop loss

- GIVEN a candidate stock has no explicit stop-loss field
- WHEN the system validates the trade plan
- THEN the system SHALL reject that candidate

### Requirement: Candidate Count

The system SHALL output no more than 3 candidate stocks per report.

#### Scenario: Model outputs more than 3 candidates

- GIVEN a model output contains more than 3 candidates
- WHEN the risk filter processes the plan
- THEN the system SHALL keep at most 3 candidates

### Requirement: LLM Review Pass

The system SHALL use Doubao as the initial generator and DeepSeek as the reviewer in v0.1.

#### Scenario: Reviewer finds weak execution logic

- GIVEN Doubao outputs a candidate with vague entry or invalidation conditions
- WHEN DeepSeek reviews the plan
- THEN the system SHALL request a clearer condition or mark the candidate as lower confidence

### Requirement: Push Notification

The system SHALL push the final Markdown report through PushPlus first, with Feishu as fallback.

#### Scenario: PushPlus fails

- GIVEN the final report is rendered
- AND PushPlus returns a failed response
- WHEN fallback push is enabled
- THEN the system SHALL send the report through Feishu

