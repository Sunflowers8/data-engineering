# Question 7 — Distributed Processing Judgment

I would not rewrite the existing daily pipeline in PySpark because it processes 3 GB of data in approximately eight minutes, which already meets the current processing requirements.

The temporary 2 TB historical backfill is a separate workload. I would first evaluate whether the existing warehouse can process it within the required time and cost constraints.

If the warehouse cannot handle the backfill efficiently, I would consider using PySpark specifically for that task while keeping the regular daily pipeline unchanged.

One important Spark concern is **data skew**, where certain partitions contain significantly more records than others. This can cause uneven processing times and reduce performance.

Overall, I would prioritize a simple, maintainable solution and introduce distributed processing only when its benefits justify the additional complexity.
