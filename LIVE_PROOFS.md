# Live proofs

Verified 2026-09-26 on gasless StudioNet (chain 61999). Every transaction listed
below returned FINALIZED and leader execution SUCCESS. Majority agreement is not
claimed to be unanimous: some validators were cancelled after quorum.

## Matching deployment

- [Contract](https://explorer-studio.genlayer.com/address/0xA0DB832398a6Fbb1cFE7a65de8DA3BFaFDbc588e)
- [Deployment](https://explorer-studio.genlayer.com/tx/0x7317e24990f01a919681031216557df7e48e9760d1710c459b58639cf9cfb890)
- Deployed source exactly matches `contracts/DynamicInfrastructureOrchestrator.py`
  at commit `544144587951afd95ccf95c311d10372bc20fef6`, after newline normalization:
  15,800 characters. Checked with `gen_getContractCode`, base64 decoding, and comparison.
- Sender/owner: `0xDF247b532B6c83E0cD5b5E8612Ca452BaFf1Ec4a`.
- Earlier address `0x40a1A76D649A8F93fD6e70810B4C0AEA0A200137` is superseded.
  Three JSON CLI proposals on that address had execution errors and are not usage proofs.

## Configuration lifecycle

| Operation | Finalized successful transaction |
|---|---|
| Network and evidence commitments | [create_network](https://explorer-studio.genlayer.com/tx/0x29d527463e1bae3975c61721e5e68e96519a0fdca8d87e5e7735b17c459e8d2b) |
| Cooling registration | [register_component](https://explorer-studio.genlayer.com/tx/0xbd310d228ff9030c6329aeb8ae3fc7bea2a8840755f4bb1614a402c715aa8f8b) |
| Dependent machine registration | [register_component](https://explorer-studio.genlayer.com/tx/0xf08c4cfb1b9b3f5d67f94347e66a023f77774cc4b19414b952771cb79f1c7e0e) |
| Immutable configuration seal | [seal_network](https://explorer-studio.genlayer.com/tx/0xd235fb91e8a361a1842d0b8414da721724bd9567982aec93a9e414ed5df0fd1a) |

## Negative semantic proof

The generic state-edge table permits machine ACTIVE → MAINTENANCE, but the fetched
specification and runbook explicitly require prior STANDBY isolation.

- [Forbidden proposal](https://explorer-studio.genlayer.com/tx/0x6f7630436d33ca8b8d77b32a80fbdbd4f84f0b6ee538c7dd0f38257a1e4fb662)
- [Independent semantic resolution](https://explorer-studio.genlayer.com/tx/0xaad66c9cfda50eb42362d6a27c2b4704450fb6d120bfe9ce40138b2e4201fd8a)
- Stored state: `REJECTED`; vector `FAIL / FAIL / PASS`.
- Both sources HTTP 200, full-body hashes matched, completeness true.
- Result root: `df6a568be51b4b48e332421c08d771542d2722e43cedb6408ec746911b616a4a`.
- Rejection did not advance the parent model (version 0).

## Positive ordered-batch proof

Steps: machine ACTIVE → STANDBY, then cooling ACTIVE → MAINTENANCE.

- [Supported proposal](https://explorer-studio.genlayer.com/tx/0xe3164ca2d781a021b51923623bd0780cfdf8cd967ac670936849e49067583bfc)
- [Independent semantic resolution](https://explorer-studio.genlayer.com/tx/0x8bf01ecb9adc3aafe63b0a30e0219eaaf96811732b6123675a0926f74b56f219)
- Stored state: `APPLIED`; vector `PASS / PASS / PASS`.
- Both sources HTTP 200, full-body hashes matched, completeness true.
- Result root: `541d0f41401ea5713969d443c6f1a33e48ca138a23df2bec556adbd77cfa6c73`.
- Model advances once to version 1; machine STANDBY, cooling MAINTENANCE.
- Model root: `dbae6cd07f15bb6873c31c0dbbd7099ddf8433b50d934857d54589cc3704f46c`.

## Competing-parent proof

- [Competing version-0 proposal](https://explorer-studio.genlayer.com/tx/0x5efc6bccef71da7ad736e8cd717a3f0ba8e11e8532d51a9fb05ee332f0ad2415)
- [Stale resolution](https://explorer-studio.genlayer.com/tx/0xfd1ecc02aa596b964587a5c2d6810d6bc0d51df3d48288148f61b8d478666c65)
- Stored state: `STALE`; no model mutation, model stays version 1.
- Result root: `909d367c0843f35f29ba1c88649c12f626f1371b2bdcf7c13d10e9d0b35358e2`.

## Evidence scope

Both public documents are synthetic fixtures pinned to source commit
`544144587951afd95ccf95c311d10372bc20fef6`. They are not independent factual authorities
or evidence of actual equipment behavior. This demonstrates independently acquired
plan/document compatibility and meaningful model mutation, not physical execution.

- Specification SHA-256: `808103080523ed7cf538b9c53251a1370aeda2fcc90f73d52910128e0edb8ad3`.
- Runbook SHA-256: `ac20fdc5634c98111d7a7eed58f6e1c1f8d88a3fb37b0f21fcf4cf42d001bade`.
- GenVM lint/SDK validation passed; 11 direct tests passed (mocked leader path).
- No live hash-mismatch, expiry, forced-validator-disagreement or physical-use claim.
