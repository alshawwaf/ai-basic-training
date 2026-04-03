# Discussion Guide — Session 0.4: Discovery Questions

> **For facilitators and self-study.** Use these exercises during the live session or work through them independently.

---

## Exercise 1: PDFC Warm-Up — Your Last Customer (10 min)

Think about the last security engagement you were part of (a deal, a POC, an architecture review). Apply PDFC retroactively:

| Phase | What You Knew Then | What You'd Ask Now |
|-------|-------------------|-------------------|
| **Pain** — What was the customer's core problem? | | |
| **Data** — What data did they have available? | | |
| **Fit** — Was their problem genuinely ML-solvable? | | |
| **Commitment** — Did they have the resources to operationalise? | | |

**Reflection:** If you had used PDFC during that engagement, would the outcome have been different? What question would have changed the conversation?

---

## Exercise 2: ML Fit Scoring (10 min)

For each scenario below, score it against the ML Fit Checklist (1 point per criterion met). Recommend whether to proceed with ML.

### Scenario A: A government agency wants to classify all incoming emails as phishing or legitimate.
- [ ] Pattern-based?
- [ ] Data available?
- [ ] Tolerance for imperfection?
- [ ] Scale problem?
- [ ] Dynamic threat landscape?
- [ ] Measurable outcome?

**Score:** /6 — **Recommendation:**

### Scenario B: A startup wants AI to predict which employees will become insider threats based on HR performance reviews.
- [ ] Pattern-based?
- [ ] Data available?
- [ ] Tolerance for imperfection?
- [ ] Scale problem?
- [ ] Dynamic threat landscape?
- [ ] Measurable outcome?

**Score:** /6 — **Recommendation:**

### Scenario C: A hospital wants to reduce the time it takes to triage security incidents from 45 minutes to 10 minutes.
- [ ] Pattern-based?
- [ ] Data available?
- [ ] Tolerance for imperfection?
- [ ] Scale problem?
- [ ] Dynamic threat landscape?
- [ ] Measurable outcome?

**Score:** /6 — **Recommendation:**

**Discussion:** Scenario B is a red flag — low data availability, low tolerance for false positives (labelling an employee a threat based on HR data is legally risky), and dubious pattern validity. Good discovery means qualifying OUT of this one.

---

## Exercise 3: Discovery Role-Play (20 min)

### Instructions
Work in pairs. Use PDFC. The architect must uncover at least 2 AI opportunities and 1 red flag. The customer answers based on the scenario — improvise details as needed.

### Scenario 1: Mid-Size Healthcare Network
- 3 hospitals, 200-bed network
- Palo Alto firewalls + CrowdStrike EDR
- No SIEM — logs go to a shared drive
- Compliance: HIPAA, regular audits
- 2 security staff, no data science background
- Main concern: ransomware
- Budget: minimal, but willing to invest if ROI is clear

### Scenario 2: National Retailer
- 500 stores, major e-commerce platform
- Splunk Enterprise with 1 year of logs
- 15-person SOC, 3 shifts
- 8,000 alerts/day, 85% are false positives
- PCI-DSS compliant
- Recently had a breach (credit card skimmer on e-commerce site)
- Board has mandated "AI investment" — $1M allocated
- Data science team of 4 people (currently focused on marketing analytics)

### Debrief
- For each scenario: what's the highest-value AI use case? What approach?
- Where did you encounter a red flag? How did you handle it?
- Did the DATA phase change your initial hypothesis?
- What POC would you propose?

---

## Exercise 4: Build a One-Page Discovery Cheat Sheet (10 min)

Create a personal reference card you can use in real customer meetings. Fill in the blanks:

```
MY DISCOVERY CHEAT SHEET

TOP 3 PAIN QUESTIONS:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

TOP 3 DATA QUESTIONS:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

TOP 3 FIT QUESTIONS:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

TOP 3 COMMITMENT QUESTIONS:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

RED FLAG CHECKLIST:
[ ] Need 100% accuracy
[ ] Fewer than 50 events/day
[ ] Zero FP tolerance
[ ] No success metrics defined
[ ] AI mandate with no problem identified
[ ] No data ownership plan
[ ] ___________________________________ (add your own)
```

**Keep this card. Bring it to your next customer meeting.**

---

## Exercise 5: Pain-to-Solution Mapping (5 min)

For each customer pain point, write the ML approach and the specific Stage lesson where you'll learn to build it:

| Customer Says | ML Approach | Stage & Lesson |
|--------------|------------|----------------|
| "We get too many false positives" | | |
| "We can't detect insider threats" | | |
| "Our analysts spend hours writing reports" | | |
| "We need to prioritise vulnerabilities" | | |
| "We don't know what normal looks like in our network" | | |

**Check your answers against the mapping table in the session README.**

---

## Self-Study Reflection Questions

1. Of the four PDFC phases, which one do you think you'd naturally skip in a real conversation? How would you force yourself to cover it?
2. Think about a deal you lost. Was the customer's AI readiness (data, commitment) a factor? Could better discovery have changed the outcome?
3. What's the most common "red flag" you see in your customers' AI aspirations?
4. After completing Stage 0, what's the single most valuable thing you've learned for customer conversations?
