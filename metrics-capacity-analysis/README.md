# Metrics capacity analysis

This project compares Data Disk Write Operations/Sec for `vm://checkout-vm` by its `LUN` dimension. The analyzer filters to the explicit UTC window from 2026-10-03 20:00 through 20:10, validates matching dimensions and numeric values, computes averages only over shared timestamps, requires three aligned samples, and checks persistence before recommending an action.

The JSON values are illustrative teaching inputs, not live measurements. The policy recommends `tune` when the average leader is at least twice the next series and that imbalance persists across the minimum aligned samples. It recommends `scale` when every covered series averages above 80 without a dominant leader. Otherwise it recommends `measure_more`.

Metric imbalance is evidence for an investigation, not proof of causation. Validate thresholds against representative workload periods and connect the result to workload logs before making an infrastructure change.
