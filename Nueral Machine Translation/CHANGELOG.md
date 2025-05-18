### Starter Code v1.3

Address bug fixes and other enhancements listed below:

1. A2 Bugs Tracker on [piazza](https://piazza.com/class/lnlv5iq4kgria/post/325)
   - [1] `a2_main.py` [ln 126]: fixed erroneous import from 'starter'
   - [2] made `--with-transformer` True by default (--with-transformer is no longer an option)
   - [3] changed `--epochs` default value to `5` from `7`
   - [4] Wandb: resolved (use `python3 -m wandb login` to login)
   - [5] Fixed by `starter_v1.2` [here](https://piazza.com/class/lnlv5iq4kgria/post/323)
   - [6] Changed `data/english_vocab.txt` to `/u/cs401/A2/data/Hansard/Processed/vocab.e.gz` (and analagously for french-vocab)

2. A2 Translate bug on [piazza](https://piazza.com/class/lnlv5iq4kgria/post/334). Added `id` suffix to `target_eos` and `target_sos` in a2_dataloader.py
   
3. Clarifying comments and headers in the code for beam search, in response to piazza posts [320](https://piazza.com/class/lnlv5iq4kgria/post/320) and [321](https://piazza.com/class/lnlv5iq4kgria/post/321).

4. Removed unused method `plot_attention` in a2_transformer_model.py.

5. Removed unnecessary imports. Ensured necessary `from math import exp` is present in a2_bleu_score.py (see piazza posts [here](https://piazza.com/class/lnlv5iq4kgria/post/336) and [here](https://piazza.com/class/lnlv5iq4kgria/post/332)).

6. Applied linter.