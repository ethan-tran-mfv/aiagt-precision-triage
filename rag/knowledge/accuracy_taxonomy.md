# QA Issue Taxonomy

This document defines classification rules for different types of QA issues.
Used by the RAG agent to ground issue classification for any filter_criteria type.

---

## ACCURACY ISSUES

### Definition
An accuracy bug is any issue where the system produces incorrect, misleading,
or imprecise output that a user relies on for decisions or actions.

### Categories

**Numerical Accuracy** — wrong calculations, aggregations, or numerical outputs:
- Revenue total shown as $1,200 but actual is $12,000
- Percentage off by a factor of 100 (0.5% shown as 50%)
- Unit conversion incorrect (km shown as miles)
- Average computed on wrong data subset

**Data Accuracy** — wrong records, stale data, or incorrect values displayed:
- Customer profile shows a different customer's data
- Report shows last month's data instead of current
- Deleted record still appears in results
- Wrong user's order history displayed

**Classification Accuracy** — wrong labels, categories, or predictions:
- ML model classifies fraud transaction as legitimate
- Sentiment analysis labels negative review as positive
- Risk score calculated with wrong model version

**Ranking Accuracy** — items ordered incorrectly:
- Search results ranked by date instead of relevance
- Leaderboard positions calculated incorrectly

**Aggregation Accuracy** — wrong totals, counts, or summaries:
- Dashboard KPI shows wrong monthly active users
- Report total does not match sum of line items

### Non-Accuracy Issues (exclude)
- UI layout bugs, button alignment
- Performance/latency issues
- Authentication failures
- Missing features
- Typos in labels (unless causing data misread)
- Infrastructure crashes

---

## PERFORMANCE ISSUES

### Definition
A performance bug is any issue where the system is slower, less responsive,
or less efficient than expected, impacting user experience or system capacity.

### Categories

**Latency Issues** — slow response times:
- API response takes > 5 seconds under normal load
- Page load exceeds 3 seconds on standard hardware
- Database query takes 30s instead of expected <1s

**Throughput Issues** — system can't handle expected load:
- System degrades above 100 concurrent users
- Batch job takes 10x longer than baseline

**Memory Issues** — excessive memory consumption:
- Memory leak causes service restart after 24 hours
- High memory usage during file processing

**Timeout Issues** — operations exceeding time limits:
- Search request times out on large datasets
- File upload times out for files > 10MB

### Non-Performance Issues (exclude)
- Incorrect results (accuracy issues)
- Crashes and errors (reliability issues)
- UI layout problems

---

## SECURITY ISSUES

### Definition
A security bug is any issue that creates a vulnerability, exposes sensitive data,
or allows unauthorized access to system resources or user information.

### Categories

**Authentication Issues** — failures in user identity verification:
- Login bypassed with special characters in username
- Session token not invalidated after logout
- Password reset does not expire old tokens

**Authorization Issues** — improper access control:
- User can view other users' private data
- Regular user can access admin endpoints
- API allows writes without authentication

**Injection Vulnerabilities** — unsanitized input executed:
- SQL injection possible in search field
- XSS vulnerability in user profile display
- Command injection in file processing

**Data Exposure** — sensitive data leaked or improperly stored:
- API response includes password hashes
- PII logged in plaintext in application logs
- Credit card numbers stored unencrypted

### Non-Security Issues (exclude)
- General bugs that don't create vulnerabilities
- Performance issues
- UI/UX problems

---

## CRITICAL / P1 ISSUES

### Definition
A critical issue is any bug that causes system outage, data loss, financial impact,
or complete loss of a core feature. Severity = P1 or "critical" regardless of type.

### Indicators
- System is completely down or unusable
- Data loss or data corruption
- Financial discrepancy or billing errors
- Core workflow completely broken
- Security breach in progress
- Severity explicitly labelled P1 or critical

### Non-Critical Issues
- Issues that have a workaround
- Issues affecting a small subset of users
- Cosmetic issues
- Feature requests

---

## CONFIDENCE GUIDANCE

| Scenario | Confidence Range |
|----------|-----------------|
| Clear match with strong evidence | 0.85 – 1.0 |
| Likely match, some ambiguity | 0.65 – 0.84 |
| Possibly matches, needs context | 0.40 – 0.64 |
| Probably not a match | 0.0 – 0.39 |
