# Publishing names of living family members by consent

The public site anonymizes living people and people born in 1926 or later without a recorded death date.

For a person who has explicitly agreed to public naming, the person's Markdown front matter may carry:

    public_consent: true

This is an individual opt-in, not a family-wide inference. Only set it when that person's consent has actually been obtained. Do not publish sensitive notes, addresses, contact details or other private material merely because the person agreed to have their name shown.

The public build reads only Markdown under content/. There is no encrypted private JSON supplement or decryption tool in the publishing pipeline. Keep private working records outside the repository and never commit passwords or decrypted private data.
