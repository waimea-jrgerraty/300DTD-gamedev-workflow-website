# Sprint 2 - A Minimum Viable Product (MVP)


## Sprint Goals

Develop a bare-bones, working web application that provides the key functionality of the system, then test and refine it so that it can serve as the basis for the final phase of development in Sprint 3.


---

## Implemented Database Schema

For the minimal viable product, I simplified the database by removing the categories and task_groups tables, as these are not needed for the MVP. The group member of a task points directly to a project for now.

![SCREENSHOT OF DB SCHEMA](screenshots/mvp_db_schema.png)


---

## Initial Implementation

The key functionality of the web app was implemented:
- An account system was created, prompting users to sign in or create an account before they can use the system. The home page when you are not signed in is a generic hero page, and when you are signed in it switches to list invitations and invites. You can also view other users' profiles by clicking on their icon, or edit your own profile by pressing your icon at the right of the nav bar, and selecting Profile from the drop down.
- The projects page that takes the place of the home page, although it only shows the project's name and icon right now. For the final refinement this will need to show the owner of the project and the number of members.
- The invitation system, which shows above projects on the projects page. Invitations can be declined (hidden) and hidden invites can be shown. Same notes for projects apply here, but additionally the show hidden button should only show when there are hidden invites.
- The project page, which strips out the categories and groups for now, listing tasks in one box. The styling needs to be fixed for final refinement, and categories and groups need implementing.
- The task page, which allows you to edit the description, which syncs to the database when the textbox loses focus. The assign to task system and mark as completed button was also implemented for the MVP.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

