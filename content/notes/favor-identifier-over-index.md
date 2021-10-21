+++
backlinks = [
  "/notes/angular-maxims"
]
author = "Alex Bilson"
comments = true
date = "2021-06-09T21:06:30"
epistemic = "plant"
tags = ["software","iteration","table","angular"]
title = "Favor Identifier Over Index"
+++
If there are several arrays of data retrieved from different service calls it can be tempting to iterate over them all by index.

{{< highlight js >}}
const columnsFirst = this.dataService.getFirstData();
const columnsSecond = this.dataService.getSecondData();
columnsTotal = [];

for (var i = 0; i < columnsFirst.length(); i++)
{
  const total = columnsFirst[i].value + columnsSecond[i].value;
  columnsTotal.append(total);
}

return columnsTotal;
{{< / highlight >}}

Iteration by index is prone to many errors, however. The order of each column array must match, their lengths must equal (although this can be overcome with a null check), and it's not clear to other developers why there's a hard dependency between these arrays without further investigation.

Instead, prefer to use a common identifier when possible:

{{< highlight js >}}
const rows = this.dataService.getRowData();
const columnsFirst = this.dataService.getFirstData();
const columnsSecond = this.dataService.getSecondData();

return rows.map((row) => {
  return columnsFirst.find((c) => c.id === row.id)?.value + columnsSecond.find((c) => c.id === row.id)?.value;
});
{{< / highlight >}}

This example does not rely upon array order and is more explicit about how the total is calculated based on the column value's row.

Thanks to Greg Nikitow for the tip!

