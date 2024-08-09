# OutlookCtl

This script provides useful interactions with Outlook.

## Commands

### Create timeblock

Command `create_timeblock` will create an appointment without invitees in Outlook Calendar.

Example: `outlookctl create_timeblock -s '2024-04-18 16:00' -t 'Test'`

Configuration:

- `default_timeblock_duration` is the timeblock (appointment) duration in minutes
