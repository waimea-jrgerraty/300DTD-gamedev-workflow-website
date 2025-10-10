# Project Requirements

## Identified Problem or Need

There is not a particular online tool that facilitates a task tracking workflow tailored for game development. Existing solutions are clumsy to use between multiple teams of specialised roles.

## End-User Requirements

The end users for this website are game studios and their employees. Specifically, this is made with the studio founded by a few people I know online in mind. These users are unhappy with their current solution which is Trello, as it is difficult effectively distribute tasks to different teams. The people who know how to 3D model do not want to be seeing each and every task related to programming. This has resulted in them having several very long task groups for different areas of work, which leads to a cluttered and unproductive workspace.
My specific end users have some other requirements. One of them suffers from colour blindness, so their input in design will be crucial for my solution to succeed. They also have a large google docs file for their game's story, which needs be seamlessly integrated into this solution.

## Proposed Solution

I intend to create a web application that allows users to create projects and invite other users to these projects. A project contains many tasks, which are organised into task groups and categories. Categories refer to areas of development, so someone specialising in one area does not have to see every task in an area they are not needed for. Creating a project will initialise it with some basic categories, such as Animation, Modelling, Programming, Writing. Within a category tasks will be in task groups


---

# Relevant Implications

## Accessibility

Accessibility implications involve ensuring my website is available to and usable for all end-users, regardless of their abilities.

### Relevance to the System

All users of this website need to be able to be able to use it with minimal difficulty; if parts of the site are not accessible for a user, (such as if they struggle with low-contrast text or colour blindness) they will seek other solutions. As this system targets a desktop application, this does not apply to mobile accessibility.

### Impact / Considerations

To ensure my website meets the accessibility requirements, I must ensure the website functions correctly on various desktop and laptop resolutions. Since the site is not targetting mobile support, that will be a lower priority. It would still be helpful to have a working (but potentially reduced) mobile interface, for cases where developers are messaged while away from their main device. As many of my users may have vision impairments, including myself, I must ensure the site remains easy to use under these conditions. To do this, I will ensure the following:
- The background and text should not have excessive contrast for a dark theme; for those with astigmatism such as myself, midnight themes cause halation around the white text making it harder to read. The background on my site will be a dark grey to minimise the effects of halation.
- Use a font with industry-respected readability for visually-impaired users.
- A suitable colour scheme should be chosen that works well for different types of colour blindness, such as using blue and red instead of green and red.
- Ensuring all UI components are appropriately sized and easy to navigate on different resolutions.



## Functionality 

The Functionality implication relates to *how well* my website works for its end users, in terms of meeting its intended purpose.

### Relevance to the System

The website must be functional for my end users, regardless of their knowledge of each area of game-development. As it is a wide field that brings in programmers, artists, writers, and management, the site must meet each of their requirements. Each of these user groups need the UI to meet their needs for managing tasks between them.

### Impact / Considerations

Ensuring the functionality of my website will involve frequent testing from my end-users while refining the final product, to ensure each of their usage requirements are met. As I am a programmer, I do not know what features will be needed for writers or artists, so their input will be necessary. The site also needs to be bug free and not feel clunky to use for it to work well for the end users.


## End-User Implications

End-User Implications are connected to the specific needs of my end-users.

### Relevance to the System

My end users have various degrees of ability in different aspects of game development, so I will need to consider how I can fulfil their specific needs while not confusing them with solutions for other users specific needs. As my target user-base is developers, the types of devices they will be using are desktops and laptops. 

### Impact / Considerations

To address end-user implications for my site, I will need to know a-lot about my end users, in terms of age, gender, and interest in order to design a suitable interface. My site will need to use language and content appropriate for the knowledge of my end users, including the tasks they generate. I can achieve this by separating tasks into categories, so people knowledgeable in one field don't have to see confusing terminology from users knowledgeable in another field. I will also need to ensure the site works on a range of desktop and laptop resolutions, and make regular use of user feedback in the design and implementation process. 



## Privacy

The Privacy implications of my website relate to protecting the privacy of my end users and their data.

### Relevance to the System

As this website deals with user accounts, I must ensure their sensitive account details like their password are properly encrypted to protect their credentials in the case of a data-breach. Since the projects generated by the users are not intended to be public, I need to ensure their projects are only accessible to invited users. Ideally, I would also encrypt the project data to protect from data-breaches, but I think that is outside the scope of this project.

### Impact / Considerations

This website will collect and use as little data from the user as is absolutely necessary, and will only store that data if it is required. This means user accounts will only contain a username, password, optional "role" and optional image. (role is a pre-made list of roles related to game development). Checks will need to be in place to ensure the user can only see data when necessary, such as restricting access to pages related to projects if you are not a member of that project. I will also need to abide by all privacy laws, such as the NZ Privacy Act 1993.



## Legal Implications

Legal implications mean ensuring my website conforms to all relevant NZ laws.

### Relevance to the System

My website may host private, potentially copyrighted data from other companies, so I will need to ensure that data is protected, and will need to include a Terms of Conditions / Privacy Policy to state that users maintain full ownership of their data and copyrights, and that users are responsible for ensuring they have legal rights to upload content. 

### Impact / Considerations

I will need to include a footer to indicate I have copyright over the website, but client data and content remain the property of their respective owners. I will also need a Terms of Conditions and Privacy Policy (accessible from the footer, and with a required checkbox for sign up).


---

# User Experience (UX) Principles

## Aesthetics and Minimalist Design

Aesthetics and Minimalist Design means keeping the UI as simple as possible, focussing on the current user action.

### Relevance to the System

This principle is important to my website, as it needs to be as simple as possible to use without a substantial learning curve. As such, keeping the design minimal will improve the user experience and make it easier to figure out how to use it for first time users.

### Impact / Considerations

To keep the design minimal, I will do things like not showing every little detail about a task on a project until you click on that task. This will reduce the visual clutter in the task list, and make it easier to find the tasks you are looking for. I will make sure my website is aesthetically appealing to my end users by getting frequent input from them in the design and implementation process.


## Help Users Recognize, Diagnose, and Recover from Errors

This principle means when something goes wrong on my website, such as a form being invalid, the website should clearly tell the user what happened, why it happened, and how to fix it.

### Relevance to the System

This principle is important for streamlining the experience on my website. When something the user tries does not work, telling them how to work around it will make onboarding quicker and help the user get started using my website sooner.

### Impact / Considerations

This site will make use of Flask's flash feature, as well as custom http responses for parts of the javascript API, which will need to display error messages to the user. These messages will need to be descriptive and offer a solution for best user experience. The remember me button on the login page should also remind users not to use that on public devices.


## User Control and Freedom

This principle means users should always feel in control of what happens on my website, such as the ability to cancel out of forms or undo actions if they make a mistake or change their mind.

### Relevance to the System

My website will have several modal forms, so ensuring the user has control over these and the freedom to cancel out of them if they want is important for my sites usability.

### Impact / Considerations

The website should not lock you into any form, be it the login/sign up pages or modal forms for managing your projects. There should be a simple and easy to understand way cancel at any point, such as by using the navbar on the login/sign up pages, or pressing the cancel/close buttons on modal forms. Even including a link to the sign up page from the login page and vice versa is something to consider for best practice. The remember me system will be optional through a checkbox on the login page.

