+++
draft = true
category = "family"
comments = true
date = "2021-08-10"
lastmod = "2021-08-06 14:43:49"
description = "In which Alex investigates what a vaccine is and how it works."
tags = ["vaccine","covid","safety"]
title = "What is a Vaccine?"
[featuredImage]
  alt = ""
  large = ""
  small = ""
+++
There are numerous resources on the subject of vaccinology, but I learn best when I write it down for myself. Constructive criticism welcome; I'm figuring this out as I go!

# What is a Virus

Before we look at vaccines, let's consider the problem: viruses. What is a virus? No virus has received more recent attention than SARS-CoV-2, so let's focus on it.

> A virus is a submicroscopic infectious agent that replicates only inside the living cells of an organism. ({{< outref name="Wikipedia" src="https://en.wikipedia.org/wiki/Virus" >}})

A SARS-CoV-2 virus, pre-infection, consists of:

1. {{< acronym RNA "RiboNucleic Acid" >}}, which is a virus' genetic code, or genome.
2. The capsid, or a coat of protein which protects the virus' genome.
3. An outer envelope composed of proteins and lipids (fats).

# How does SARS-CoV-2 Hurt Me?

The short answer is, replication inside crucial cells.

# How does a virus replicate?

If you remember back to high school, there are four nucleobases: Adenine, Thymine, Guanine, and Cytosine (ATGC). Adenine pairs with Thymine, Guanine with Cytosine. Since we're talking about RNA, however, we swap Thymine for Uracil (AUGC).

Like other viruses, SARS-CoV-2 replicates at an extreme pace. As a {{< acronym "+ssRNA" "positive-sense single-stranded RNA" >}}, it replicates inside living cells by attracting opposite nucleobases to form a double strand of base pairs, separates, and the opposite strand attracts a duplicate nucleobase set.

Let's say this chain of nucleobases aref part of the SARS-CoV-2 RNA strand:

```
A
A
G
U
C
```

To replicate, these nucleotides attract opposite nucleobases like so:

```
A - T
A - T
G - C
U - A
C - G
```

When this strand separates, you have the original SARS-CoV-2 RNA strand (AAGUC) and an opposite copy of itself (TTCAG) which, through the same process, will make a second copy of the original. That's how it creates new copies of its genome.

But if you remember what composes a virus, the genome is only its center. It also has a capsid and an envelope. Both of these require the virus to replicate proteins.

# How does a virus generate proteins?

An RNA virus like SARS-CoV-2 can replicate itself by attracting nucleobases, but it can also encode proteins through a process called transcription. For this reason, it is considered both an RNA and {{< acronym mRNA "messenger RiboNucleic Acid" >}}.

Sets of nucleobase base pairs, called codons, encode the binding of specific proteins. With the help of cell ribosome's, which are protein synthesis factories, the mRNA strand's codons are paired with the correct amino acid sequence to form a protein. SARS-CoV-2 encodes four proteins, a spike, envelope, membrane, and nucleocapsid protein. The nucleocapsid protein coats the genome while the other three form an envelope around the nucleocapsid which attracts lipids.

TODO: answer: when does it replicate the genome, when does it transcribe proteins?

Ok, so that's what happens when SARS-CoV-2 gets inside you, but how does it get there in the first place?

# How does that virus get inside my cells?

The protein envelope on a virus has an affinity for specific cell enzymes. SARS-CoV-2's affinity is for the {{< acronym ACE2 "Angiotensin-converting enzyme 2" >}} found in the outer casing of cells in the intestines, kidney, testis, gallbladder, and heart ([ACE2](https://en.wikipedia.org/wiki/Angiotensin-converting_enzyme_2)). When a SARS-CoV-2 virus interacts with a cell that has ACE2, it attaches to the enzyme site and deposits its RNA into the cell through a process called membrane fusion.

# What does my body do when a virus starts to replicate?

Humans have two immune responses when foreign invaders are detected, the innate and adaptive.

Skin, snot and white blood cells (leukosytes) fall into the innate category. These are generalists who prevent or absorb any intruder not recognized as a healthy human cell.

B and T cells are in the adaptive category. These are ~specialists~ assassins which activate only when a specific antigen trigger is received.

TODO: Figure out how the adaptive B and T cells are activated and what they do to viruses that are found. Memory T cells are what vaccines create to prep the body for a SARS-CoV-2 invasion.

# What is a vaccine?

Now let's look at the definition of a vaccine.

> A vaccine is a biological preparation that provides active acquired immunity to a particular infectious disease. [Wikipedia](https://en.wikipedia.org/wiki/Vaccine)

# How does a vaccine protect me from a virus?

Before we can


