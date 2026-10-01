---
title: Deals and savings Data Product Charter
status: local-source-pilot
created: 2026-08-08
updated: 2026-09-08
tags: [template, data-engineering, data-product, governance]
description: Outcome, consumers, ownership, contract, quality, privacy, and operating boundary for a data product.
---

# Data Product Charter

## Document control

| Field | Value |
|---|---|
| Data product ID/version | book-deal-data / deal.v1 |
| Product owner | bookchaowalit |
| Data owner/steward | bookchaowalit |
| Producer team | Domain repository |
| Status/review date | Local source pilot / 2026-09-08 |
| Evidence boundary | schema.json, source policy, capture adapter, fixtures and tests in this repository |

## Product contract

- Decision or user outcome: Compare conditional savings against required spending and renewal.
- Consumers and use cases: Discovery applications; integration planned.
- Source systems and lake layers: Six reviewed public offer pages (Apple education, Microsoft Education, Rakuten, ENERGY STAR Rebate Finder, Steam bundles, Dropbox referral) → immutable landing → Bronze through the shared local runtime.
- In scope/out of scope: Offers requiring purchase or a commercial condition; zero-price claims belong to freebie.
- Freshness, availability, and volume expectation: Target source review every 24h; open filter rejects checks older than 72h; no live SLA.
- Data classification, residency, retention, and access: Public program metadata only; no user profile; raw retention is private local operational storage.
- Quality thresholds and incident route: Contract, source-drift and replay tests pass; owner handles source failures and parser drift.
- Cost/capacity guardrail: Manual capture only; max 10,000 records per envelope.
- Versioning, deprecation, and migration policy: Draft v1; breaking changes version separately; no legacy migration or live consumer yet.

## Acceptance and ownership

| Gate | Evidence | Owner | Result/status |
|---|---|---|---|
| Contract | Versioned schema and compatibility rules | bookchaowalit | pass (local) |
| Quality | Checks and threshold report | bookchaowalit | pass (fixtures; live monitoring pending) |
| Lineage | Source-to-consumer map | bookchaowalit | pass (local capture) |
| Access/privacy | Classification and access review | bookchaowalit | pass (public metadata only) |
| Operations | Runbook, alert, replay, and recovery | bookchaowalit | partial (manual capture; no scheduler) |

## Approval

| Role | Name/date | Decision |
|---|---|---|
| Product/data owner |  | Approve charter / revise |
| Producer owner |  | Accept delivery boundary |
| Consumer representative |  | Accept use and SLA |
