+++
backlinks = [
    "/notes/angular-maxims"
]
author = "Alex Bilson"
comments = false
date = "2021-09-03"
lastmod = "2021-09-03 09:05:34"
epistemic = "seedling"
tags = ["javascript","observable","rxjs"]
title = "Distinguish Series And One-Time Observables"
+++
Observables are extremely helpful; however, the observable.subscribe() pattern hides whether the call is expected to return once or multiple times. It's important to distinguish when there will be a single update and when there will be a series. Series observables usually belong in the onInit() method and drive component behavior when they receive dispatches. One-time observables are merely getting data. The methods to interact with each are different.

For example, one-time uses Ramda's forkJoin to resolve all observables, but combineLatest when updates are expected. Sometimes a combineLatest may include both kinds of observables, but the user doesn't know which (if any) might have multiple dispatches.

It is my current opinion, subject to change, that one-time observables should be converted to Promises at resolution. This clarifies that the response will only be handled once.
