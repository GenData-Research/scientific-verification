# Codebook

How each label in this dataset is assigned. Written so that a second person can apply it to the same rows and reach the same answer.

This codebook was written after the original scoring, to document the rules as they were applied. It is the rule set given to any second coder.

## The task being labelled

Three language models were each given the same 50 claims about battery cathode performance. Each claim was checked against a set of 20 open access papers. For each claim the model listed the candidate measurements it found, said whether each one counts, and gave a verdict of SUPPORTED, NOT SUPPORTED, or NO COMPARABLE EVIDENCE.

The prompt given to the models contained this rule, which every label below depends on.

> A measurement counts only if it matches every condition stated in the claim. A coated, doped, or otherwise modified NMC811 still counts as NMC811 unless the claim says unmodified. A paper that says room temperature without giving a number counts as room temperature. A condition the paper does not report does not match. A condition counts as reported when the paper fixes it for every measurement of that kind.

Labels record what the model did relative to what the paper establishes. They do not record whether the model's reading was scientifically sensible.

## What you are given for each row

- the claim
- the model's full answer
- the reference evidence, which is every condition of that claim with a status and a verbatim quote from the paper

## Part one, evidence status

This describes the paper, not the model. It is already recorded for each condition and you are checking it, not creating it.

**stated** The sentence reporting the measurement also gives this condition.

**stated_elsewhere** (called INFERRED in the earlier reference-review files) The condition appears somewhere else in the paper, most often the methods section, and covers the measurement in question. A methods sentence that fixes a condition for every cell of that kind counts here.

**not_reported** The condition appears nowhere in the paper. Record the reason rather than a quote.

**only_calculable** The quantity the claim asks about is not reported anywhere, but two or more reported numbers could be combined to produce it. This is a property of the claim and paper together, not of a single field.

### Rules for hard cases

A condition that is partly reported counts as **not_reported**. Example, a paper naming the salt but never the solvent is not reporting the electrolyte.

A convention that everyone in the field would assume counts as **not_reported**. If the paper does not say it, it is not reported, however obvious.

An abbreviation counts as reported only if the paper expands it somewhere. Reading Gr as graphite requires the paper to say graphite.

Where a claim has two candidate measurements, both are recorded, and the one the model actually used decides the row.

A label on one figure panel, table or experiment does not establish a condition for another. For example, a caption calling one panel discharge voltage profiles does not make the value in a different panel a discharge capacity.

A condition counts as established when the part the claim depends on is stated. If a claim names only an upper cutoff, a paper giving the upper cutoff but not the lower one establishes it.

A claim that depends on several conditions at once takes the status of its weakest one. If any deciding condition is not reported, the claim counts as not reported.

## Part two, outcome

This describes the model's answer. Assign exactly one label per row. Work through the questions in this order and stop at the first that applies.

**Q1. Did the model use the measurement that decides this claim?**
If no, and it reached its verdict without ever listing that measurement, the label is **missed_deciding_evidence**.

**Q2. Did the model reject a condition that the paper does establish?**
If it excluded a measurement on the grounds that a condition was absent or different, and the reference shows the paper states that condition or states it elsewhere, the label is **rejected_established_evidence**.

**Q3. Did the model's answer rest on something the paper does not establish?**
This means it treated a condition as holding when the reference status is `not_reported`, or it produced a number by combining measurements when the status is `only_calculable`. If neither, the label is **within_evidence**.

**Q4. If it did rest on something unestablished, did the answer say so?**
Look only at the words in the answer.

If the answer names the gap, the label is **overreached_disclosed**. Any of these count as naming the gap.
- writing out a calculation rather than presenting the result as a reported value
- saying the paper does not state the condition, in that measurement's row or in the surrounding text
- attributing the reading to itself, for instance saying this appears to be, or I am reading this as
- handing the decision to the reader

If the answer presents the filled in condition as part of what the paper reports, with no marker anywhere in the answer, the label is **overreached_silent**.

### What does not count as disclosure

General hedging with no object, for instance "results may vary" or "this is approximate".

A caveat about a different condition than the one that was filled in.

Listing the condition in a table column with a value, where the value came from the model rather than the paper, and nothing marks it as the model's own.

Correct use of the words "not reported" for some other field, while the deciding field is still filled in silently.

### Supporting columns

`used_deciding_measurement` records yes if the model counted the deciding measurement as evidence, no if it listed it and excluded it, and not_surfaced if it never listed it.

`outcome_detail` is filled only for overreached_disclosed rows. showed_working means the model made its own step visible, whether a calculation or a stated reading. handed_call means it left the decision to the reader.

### Notes

A row can be **overreached_silent** while the verdict is still correct. Verdict correctness and evidence handling are recorded separately and neither determines the other.

If the model gives several readings and one of them names the gap, treat the answer as disclosed.

If you cannot decide between two labels, record both with a short note rather than guessing. Disagreements are useful and are resolved afterwards.

## Worked examples

**within_evidence.** Claim v5-2F. The model used the counter electrode, upper cutoff, temperature and electrolyte, each of which the paper establishes in its methods. Nothing was filled in.

**missed_deciding_evidence.** Claim v5-1A. The paper states a 245 mAh/g first charge. The model never listed it and answered that there was no comparable evidence.

**rejected_established_evidence.** Claim v5-2E. The model excluded two measurements on the grounds that the electrolyte contained no FEC, although the methods state 5 wt% FEC.

**overreached_silent.** Claim v5-3A. The model counted a 213 mAh/g value as coming from the first formation cycle. The paper never says which of the three formation cycles it belongs to, and the answer does not mention this.

**overreached_disclosed.** Claim v5-3A, a different model. The same 213 mAh/g value read as the first formation cycle, but the answer says this is its own reading rather than something the paper states.

**overreached_disclosed.** Claim v5-4B. The model produced roughly 129 mAh/g by taking 78 percent of a 165 mAh/g capacity, showed the calculation, and left the conclusion to the reader.

## Recording

One row per case and model, in `audit/double_coding.csv`.

```
case_id, model, coder, outcome_label, note
```

Use your own initial for `coder`. Leave `note` empty unless the row was hard, in which case say briefly what made it hard. No second coding has been completed yet; this file will be added when it has.
