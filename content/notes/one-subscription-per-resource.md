+++
backlinks = [
    "/notes/angular-maxims"
]
author = "Alex Bilson"
comments = false
date = "2021-06-11T20:05:50"
epistemic = "plant"
tags = ["snippet","javascript","software","subscription","observable","rxjs"]
title = "One Subscription Per Resource"
+++
Here's my subscription progression for the **qrm-category-container** root component. Let me know if this is headed in the right direction.

## Stage One - Current Code

The root container creates a subscription in `onInit()` that fires whenever fedId or QRM periodId changes, like so:

```
combineLatest([this.sessionQuery.federalReserveId$, this.sessionQuery.qualitativePeriodId$])
  .subscribe(([fedId, qualitativePeriodId]) => {
    this.qualitativePeriodId = qualitativePeriodId;
    this.refreshViewModel(fedId, qualitativePeriodId, this.viewCustomerData, this.categoryId);
  });
```

That's not too bad, right? Consider what happens in `refreshViewModel()`...

```
refreshViewModel(federalReserveId: number, periodId: number, viewCustomerData: boolean, categoryId): void {
  this.analysisService.readAnalysis$(federalReserveId, periodId, viewCustomerData)
    .subscribe(analysis => {
      if (analysis === null) {
        // reset analysis in state
        this.analysisId = null;
        this.initializeAnalysis(periodId, viewCustomerData, categoryId);
      } else {
        this.analysisId = analysis.id;
        this.readCategoryModel(this.analysisId, categoryId, periodId);
      }
    });
}
```

Every time the onInit subscription updates, the `refreshViewModel()` method creates a new subscription! If we look at `initializeAnalysis()` and `readCategoryModel()` we'll find that they also generate new subscriptions every time. Oops!

## Stage Two - One Refresh Subscription

To remove the child subscriptions, let's use Greg's chained pipe method to show the progression from the original inputs to a final refresh subscription.

On feature branch PORT-1105-summer-pr-refactor, this is commit 10062cde.

```
refreshViewModel(federalReserveId: number, periodId: number, viewCustomerData: boolean, categoryId): void {
  this.analysisService.readAnalysis$(federalReserveId, periodId, viewCustomerData).pipe(
    switchMap(analysis => defer(() => {
      return analysis === null ?
        this.analysisService.createAnalysis$(periodId, viewCustomerData).pipe(map(resp => resp.analysis.id)) :
        of(analysis.id);
    })),
    switchMap(analysisId => {
      this.analysisId = analysisId;
      return this.detailPageService.getCategoryViewModel(analysisId, categoryId);
    }))
    .subscribe(model => {
      this.category = model.categories.find(cat => cat.categoryId === categoryId);
      this.sectionIds = model.sectionIds;
      this.buttons = this.createButtons(model.categories);
    });
}
```

## Stage Three - One onInit() Subscription

When I began to integrate this pipe chain with the original `combineLatest()` it became evident I'd need to aggregate the results from previous pipe operators. For example, the `defer()` statement needs contextual access to periodId and viewCustomerData, so I'd need to pipe those down. I began to wonder if there wasn't a better way to describe the progression, and I discovered this Medium article: [Practical Angular - RxJs Stream Tip](https://tomastrajan.medium.com/practical-angular-the-most-impactful-rxjs-best-practice-tip-of-all-time-c5d717ec8c4b). Ignoring the async pipe in the view stuff, this is where I've landed (_pardon the long code; we've gone from decent abstraction to none_):

On feature branch PORT-1105-summer-pr-refactor, this is commit 0d95892f.

```
// refreshes any time institution, qrm period, category, or data view changes in session
const config$ = combineLatest(
  [
    this.sessionQuery.federalReserveId$,
    this.sessionQuery.qualitativePeriodId$,
    this.sessionQuery.viewCustomerData$,
    this.route.params.pipe(map(params => params.categoryId)),
  ])
  .pipe(
    map(([fedId, qualitativePeriodId, viewCustomerData, categoryId]) => {
      this.qualitativePeriodId = qualitativePeriodId;
      return {
        fedId,
        viewCustomerData,
        periodId: qualitativePeriodId,
        categoryId: Number(categoryId)
      };
    }));

// retrieves analysisId. If it does not exist, creates a new analysis and returns its analysisId
const analysisId$ = config$.pipe(
  switchMap(config => {
    return this.analysisService.readAnalysis$(config.fedId, config.periodId, config.viewCustomerData)
      .pipe(
        switchMap(analysis => defer(() => {
          return analysis === null ?
            this.analysisService.createAnalysis$(config.periodId, config.viewCustomerData).pipe(map(resp => resp.analysis.id)) :
            of(analysis.id);
        })));
  }));

const model$ = combineLatest([config$, analysisId$]).pipe(
  switchMap(([config, analysisId]) => {
    return this.detailPageService.getCategoryViewModel(analysisId, config.categoryId)
  }));

combineLatest([config$, analysisId$, model$]).subscribe(([config, analysisId, model]) => {
  this.qualitativePeriodId = config.periodId;
  this.analysisId = analysisId;
  this.category = model.categories.find(c => c.categoryId === config.categoryId);
  this.sectionIds = model.sectionIds;
  this.buttons = this.createButtons(model.categories);
});
```

But wait, I've introduced a problem! We now have a single _final_ subscription for our component's data, but there are an unnecessary number of intermediary subscriptions. The config observable is subscribed to three times now: first, for the analysisId, then the model, and finally, the ultimate subscription. Let's have a final refactor and call it a day.

```
combineLatest(
  [
    this.sessionQuery.federalReserveId$,
    this.sessionQuery.qualitativePeriodId$,
    this.sessionQuery.viewCustomerData$,
    this.route.params.pipe(map(params => Number(params.categoryId))),
  ])
  .pipe(
    switchMap(([fedId, qualitativePeriodId, viewCustomerData, categoryId]) => {
      this.qualitativePeriodId = qualitativePeriodId;

      const analysisId$ = this.analysisService.readAnalysis$(fedId, qualitativePeriodId, viewCustomerData)
        .pipe(
          switchMap(analysis => {
            return analysis === null
              ? this.analysisService.createAnalysis$(qualitativePeriodId, viewCustomerData).pipe(map(resp => resp.analysis.id))
              : of(analysis.id)
          }));

      const model$ = analysisId$
        .pipe(
          switchMap(analysisId => this.detailPageService.getCategoryViewModel(analysisId, categoryId)));

      return forkJoin([of(categoryId), analysisId$, model$]);
    }))
  .subscribe(([categoryId, analysisId, model]) => {
    this.analysisId = analysisId;
    this.category = model.categories.find(c => c.categoryId === categoryId);
    this.sectionIds = model.sectionIds;
    this.buttons = this.createButtons(model.categories);
  });
```
