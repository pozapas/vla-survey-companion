# Contributing a new system

The systems table is meant to grow, but only with systems that can be placed from their own paper. This page explains the entry rule, what a proposal should contain, and how it is checked.

## Entry rule

A system is placed on the four axes only when its own paper states all five of the following items.

1. The backbone.
2. The action representation.
3. The action decoder.
4. The training data.
5. At least one benchmark together with its evaluation protocol.

An in-house real-robot suite counts as a benchmark when the paper gives the tasks and the number of trials. Systems documented only in blog posts, product pages, or model cards are not placed, because none of the five items can be checked against a citable record. A report that describes a cloud backbone and an on-robot decoder without saying what passes between them cannot be placed either, since the architecture test has nothing to decide on.

## What to send

Open an issue or a pull request that adds one row to `data/systems.csv` and one row to `data/system_links.csv`.

- Fill every column of `systems.csv` from the system's own paper, using the vocabulary of the existing rows where one applies.
- Assign the `arch_code`, `learning_class`, and `deployment_class` codes with the decision rules in the README. For the learning class, check VS, CT, XE, and BC in that order and record the first that applies, then add +RL if the paper uses a reward signal beyond demonstrations.
- In `source_page`, give the section, table, figure, or page for each filled cell, in column order and separated by semicolons.
- Use the year of the first public version, which is usually the first arXiv posting.
- In `system_links.csv`, give the DOI link when the paper has a publisher DOI, otherwise the proceedings or OpenReview page, and otherwise the arXiv abstract page.
- Run `python scripts/build_readme_table.py` and commit the updated README together with the data.

For each class code, the proposal should quote the sentence of the paper that decides it, so that a reviewer can apply the rule without rereading the paper.

## How a proposal is checked

A maintainer rereads the cited locations, applies the four decision rules independently, and compares the result with the proposed codes. When the two placements differ, the proposal is discussed in the issue until the rule settles it. If the paper does not state an item that the rule needs, the system is listed in the issue as not placeable and stays out of the table. Numbers are taken only from the paper that reports them, and a re-evaluation of an earlier system by a later paper is attributed to the paper that ran it.

Corrections to existing rows follow the same process. Please give the location in the source paper that supports the change.
