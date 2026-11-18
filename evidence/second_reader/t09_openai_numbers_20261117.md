# T09 targeted verification — OpenAI incident numbers

**Date:** 17 November 2026  
**Scope:** The three OpenAI numbers that the automated numeric-source audit could not check because the OpenAI page refused the workflow runner’s HTTP request.

## Claim checked

The manuscript states, with attribution to OpenAI, that:

- 198 of 898 ExploitGym tasks had not been solved by OpenAI models before the incident; and
- 93% of the tasks discussed on the Artifactory message board came from that set of 198.

## Primary-source result

**Pass.** The official OpenAI post, *The Hugging Face incident and the road ahead* (26 August 2026), section “Difficult tasks without a safe exit,” reports the same three numbers and relationship:

https://openai.com/index/hugging-face-incident-and-the-road-ahead/

The post was opened and checked on 17 November 2026. The matching statement is around lines 240–243 in the retrieved page view. This is a semantic check, not only a numeric string match.

## Audit interpretation

The automated audit result of 103/106 is therefore not three unresolved claims. It is:

- 103 numeric strings found automatically in locally fetched primary-source text; and
- 3 additional numeric strings verified manually against the cited official OpenAI page.

The manuscript claim requires no change. The workflow log must continue to report the access limitation rather than presenting 106/106 as an automated result.
