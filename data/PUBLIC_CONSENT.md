# Publishing names of living family members by consent

The public tree normally anonymises living people and recent people without a death
date. The encrypted source remains the place where their full records are maintained.

For a person who has explicitly agreed to public naming, the private record can carry:

```json
"public_consent": true
```

This is an individual opt-in, not a family-wide inference. Only set it for people
whose consent has actually been obtained. Do not set it on relatives who have not
agreed, and do not publish sensitive notes, addresses, contact details or other
private material merely because the person agreed to have their name shown.

## Local workflow

1. Decrypt locally; never share the password or decrypted file:
   `FAMILY_PASSWORD=... python3 data/private_tool.py decrypt`
2. Edit the gitignored `data/private_people.json`. Add
   `"public_consent": true` to each agreed record. The root Johannes is
   `p1`; his mother Vivi is `p3`. Include other relatives only after checking
   the relevant person's consent.
3. Re-encrypt and regenerate the public data:
   `FAMILY_PASSWORD=... python3 data/private_tool.py encrypt`
   `python3 data/build_data.py`
4. Review the generated `data/family.json` before committing. Check that only
   the agreed names and appropriate genealogical details are public.

The encryption key is never needed by an assistant or committed to the repository.
