+++
backlinks = [
  "/notes/angular-maxims"
]
author = "Alex Bilson"
comments = true
date = "2021-06-23T21:06:30"
epistemic = "plant"
tags = ["software","iteration","table","angular"]
title = "Simplify Loop With Iterator Swap"
+++
When operating on two or more collections you may encounter loops that filter one collection by another.

Say we have a collection of dinners and a collection of ingredients. We want to find out, given our ingredients, which dinners are using at least one ingredient. We might write our filter like this:

{{< highlight js >}}
const dinners = this.getDinnerRecipes();
const ingredients = this.getIngredients();
const dinnerIds = ingredients.map(i => i.dinnerId);

const dinnerOptions = dinners.filter(dinner => {
  if (dinnerIds.includes(dinner.id)) {
    return dinner;
  }
});
{{< / highlight >}}

The `includes()` method tells us there's something amiss that we could refactor. Let's try swapping the collection we're iterating over.

{{< highlight js >}}
const dinners = this.getDinnerRecipes();
const ingredients = this.getIngredients();
const dinnerIds = ingredients.map(i => i.dinnerId);

const dinnerOptions = dinnerIds.map(id => dinners.find(d => d.id === id);
{{< / highlight >}}

Much better. We get the same result back but with less code and cyclomatic complexity.

Whenever you're working with two collections, consider whether you might simplify your loopb by swapping the primary iterator.
