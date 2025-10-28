# Project Review

## Addressing Relevant Implications

### Accessibility

During development, I made sure to test my website at various desktop and laptop resolutions to ensure the design remained consistent and easy to use for the target device types. I designed my theme to be readable for myself despite only supporting dark mode, which I did by ensuring the contrast between the background and text was never too great, as that makes text harder to read for me. I also ensured the colour scheme used on the site worked well for my colourblind user, seeking their input multiple times. They provided valuable insight for the priority colours feature.


### Functionality

I made sure the site was functional for my end users by seeking their input on things multiple times in development. The best example of this was the decision to use a bunch of premade categories, and their suggestions here were very valuable. If I did not seek their input, I would have separated Game Design from Writing, which I now see is better to group them under the same category, as writing is part of game design.


### End-User Implications

I addressed this implication by ensuring my end users could explain things they didn't understand or like through multiple iterations. This led to a more refined design than I started with.

### Privacy

I addressed the privacy implication by preventing users from accessing pages and api endpoints for projects they are not involved with, and by ensuring passwords are hashed and salted in the database to protect them.


### Legal Implications

I did not manage to find space to put a legal page, and I am not a lawyer so I do not trust I could do an adequate job here, though it should still comply with NZ copyright laws.


---

## Overall Review

The part of this project that went the best was the database design. While it was somewhat complex, the initial design I came up with proved to be adequate and future proof to user suggestions. I never had to change the schema of the database itself to comply with suggestions from my users, though the purpose of certain things was slightly changed over time. The categories table became kind of immutable per project, with categories not being creatable or editable except for the default categories created with a project.

Some parts did not go as well. The initial design is the best example of this, being impacted by me being ill with influenza for two weeks. This delayed documentation for that sprint until towards the end of the project. While it did not go as well as I hoped, I still got some valuable input from my end users while I was away which helped shape the final design. We also missed a lot of time to work on the minimal viable product due to strikes or other events that meant we lost DTD periods. This was not as impactful as missing most of the first sprint, but did slow down the second sprint considerably.

Testing changed some aspects of the design, such as the change to categories. Testing was valuable for ensuring my design was easy to use for my colourblind user, and ensured the site worked on most computer aspect ratios and resolutions.

If I could do something differnt, it would be that I would learn HTMX before coming into this, as I ended up needing a few dynamic elements where HTMX would have helped but I had to implement with raw JavaScript as there was not enough time to pick it up by then. An example of this is the description box which has to update the database when focus is lost, or the assign member button that has to autocomplete from users in the project.
