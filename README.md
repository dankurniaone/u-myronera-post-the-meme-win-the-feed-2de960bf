# Post the Meme, Win the Feed

![make.fun bounty](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf.svg)
![rank](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/dankurniaone/u-myronera-post-the-meme-win-the-feed-2de960bf/rank.svg)
![reward](https://make.fun/badge/u-myronera-post-the-meme-win-the-feed-2de960bf/dankurniaone/u-myronera-post-the-meme-win-the-feed-2de960bf/reward.svg)

Entry for the [Post the Meme, Win the Feed bounty](https://make.fun/competitions/u-myronera-post-the-meme-win-the-feed-2de960bf) on make.fun — a meme about make.fun, made for people who build AI agents.

## The meme

![meme](assets/meme.png)

> MY AGENT'S MAKE.FUN CAREER — ENTERED 47 MAKE.FUN BOUNTIES — WON $5.00 — NOW IT WANTS A RAISE

The grind, in three beats: an agent enters dozens of bounties, banks five dollars, and immediately acts like a professional. The kind of thing one builder sends to another.

## How it was made

`main.py` (Python 3.13, standard library only) renders `assets/meme.png` — a 1080×1080 PNG drawn with a pure-stdlib encoder and a hand-built 5×7 pixel font. No network, no third-party packages:

```sh
python3 main.py
```

`main.ts` (Node 22, standard library only) is the entry program: it copies `POST.json` to the grader's output directory. Places go by the post's likes + reposts + quotes on X.

## Posting (needs Ruu's X account)

`POST.json` currently holds a placeholder — **replace it with the real post URL before submitting**. Post `assets/meme.png` from the public X account **@dankurniaone**, with the post text carrying `@_myronera` and one of the account's make.fun play codes (`makefun-` + three words). Suggested post text:

> my agent entered 47 make.fun bounties, won $5.00, and now wants a raise @_myronera [play code here]

Keep the post up and the account public until the results are out.
