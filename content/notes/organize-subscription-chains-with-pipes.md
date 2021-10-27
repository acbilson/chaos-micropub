+++
backlinks = [
  "/notes/angular-maxims"
]
author = "Alex Bilson"
comments = true
date = "2021-07-12T21:06:30"
epistemic = "plant"
tags = ["software","observables","subscriptions","angular"]
title = "Organize Subscription Chains With Pipes"
+++
Often, two or more observables depend upon one another for execution. This can lead to chained subscriptions. Take this real-world example:

{{< highlight js >}}
this.openInvalidPeriodDialog$(dialog).subscribe(dialog => {
  dialog.afterClosed().subscribe(jumpToLatestPeriod => {
    if (jumpToLatestPeriod) {
      this.periodService.getLatestPeriod().subscribe(latestPeriod => {
        this.analysisService.getPreliminaryPeriodId$(federalReserveId, analysisId, latestPeriod.id)
        .subscribe(periodId => this.sessionService.setQualitativePeriod(periodId ?? latestPeriod.id))
      });
    }
  });
});
{{< / highlight >}}

The multiple `subscribes()` might be written in a more descriptive chain with a pipe and use of `switchMap()` and `filter()`.

{{< highlight js >}}
this.openInvalidPeriodDialog$(rejectionDialog)
  .pipe(
      switchMap(invalidPeriodDialog => invalidPeriodDialog.afterClosed()),
      filter(jumpToLatestPeriod => jumpToLatestPeriod),
      switchMap(() => this.periodService.getLatestPeriod()),
      switchMap(latestPeriod => forkJoin({
          preliminaryPeriod: this.analysisService.getPreliminaryPeriodId$(federalReserveId, analysisId, latestPeriod.id),
          latestPeriod: of(latestPeriod.id)
      }))
  ).subscribe(periodToUse =>
      this.sessionService.setQualitativePeriod(periodToUse.preliminaryPeriod ?? periodToUse.latestPeriod)
  );
{{< / highlight >}}

The refactored example makes explicit that further subscriptions happen only when the boolean filter passes and keeps a single `subscription()` line that describes what actually needs to happen after all observables have been properly mapped and resolved.
