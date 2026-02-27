# Accuracy-Related Bug Taxonomy

## Definition

An accuracy bug is any issue where the system produces incorrect, misleading,
or imprecise output that a user relies on for decisions or actions.

Accuracy bugs directly affect the correctness of data, calculations, predictions,
classifications, or rankings that the system presents as truth.

---

## Categories of Accuracy Bugs

### 1. Numerical Accuracy
Issues where calculations, aggregations, or numerical outputs are wrong.

Examples:
- Revenue total shown as $1,200 but actual is $12,000
- Percentage calculation off by a factor of 100 (e.g., 0.5% shown as 50%)
- Rounding error causes financial discrepancy
- Unit conversion is incorrect (km shown as miles)
- Average computed on wrong subset of data

### 2. Data Accuracy
Issues where the wrong records, stale data, or incorrect values are displayed.

Examples:
- Customer profile shows data from a different customer
- Report reflects last month's data instead of current period
- Search results return items from wrong category
- Deleted record still appears in results
- Wrong user's order history displayed

### 3. Classification Accuracy
Issues where the system assigns wrong labels, categories, or predictions.

Examples:
- ML model classifies a fraud transaction as legitimate
- Sentiment analysis labels negative review as positive
- Image classifier identifies a cat as a dog
- Spam filter marks legitimate email as spam
- Risk score calculated with wrong model version

### 4. Ranking Accuracy
Issues where items are ordered incorrectly relative to expected criteria.

Examples:
- Search results ranked by date instead of relevance
- Recommendation engine shows lowest-rated items first
- Leaderboard positions calculated incorrectly
- Products sorted by wrong price tier

### 5. Aggregation Accuracy
Issues where totals, counts, averages, or summaries are wrong.

Examples:
- Dashboard KPI shows wrong monthly active users
- Report total does not match sum of line items
- Count query returns duplicate rows
- Average includes null values incorrectly

---

## Non-Accuracy Issues (Exclude These)

The following issue types are NOT accuracy bugs even if they affect quality:

- **UI/UX issues**: Button misalignment, wrong color, layout broken on mobile
- **Performance issues**: Page load slow, API timeout, high latency
- **Authentication/Authorization**: Login fails, wrong permissions
- **Missing features**: Functionality not yet implemented
- **Typos and labels**: Text misspellings, wrong field labels (unless the label causes a data misread)
- **Infrastructure**: Server crashes, deployment failures, memory leaks
- **Usability**: Confusing flow, hard to find a feature

---

## Borderline Cases (Require High Confidence)

These require careful reasoning — classify as accuracy only if the output
is objectively wrong, not just suboptimal:

- Search ranking that feels "off" but has no objective correct order
- Recommendation results that are valid but not personalized
- Date formatting differences (timezone issues vs wrong date)
- Rounding that follows a documented rule (not a bug)

---

## Confidence Guidance

| Scenario | Confidence Range |
|----------|-----------------|
| Clear numerical/data error with evidence | 0.85 – 1.0 |
| Likely accuracy bug, some ambiguity | 0.65 – 0.84 |
| Possibly accuracy-related, needs context | 0.40 – 0.64 |
| Probably not accuracy-related | 0.0 – 0.39 |
