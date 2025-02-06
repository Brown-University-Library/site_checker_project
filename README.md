
## Info

This is a [django](https://www.djangoproject.com) webapp that offers a publicly-viewable [webpage](https://library.brown.edu/sitechecker/) of the current status of the [Brown University Library's](https://library.brown.edu) checked-services, and an admin interface to add a service to be checked.

The admin-view allows you to set up:
- a url to be checked
- some expected-html
- a check-frequency
- email-addresses that should be notified
- optional additional email text

A separate cron-triggered script determines what sites need to be checked, and checks them.

A nice feature of the system...

If a failure is detected, the check frequency will reset to check again a couple minutes later (regardless of the normal user-specified check-frequency). And if a _second_ failure then occurs (right after the first), _then_ a failure-notification email goes out, and the checks continue for that site every couple of minutes until it's back up (only that single initial 'failure' email goes out).

An email doesn't go out on that first failure in case it's just some weird temporary blip. And once the site is back up, a 'back-up' email goes out, and the check-frequency returns to the normal user-specified frequency.

dummy test
---
