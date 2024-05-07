import win32com.client

from datetime import datetime, timedelta

from buvis.adapters import AdapterResponse, console

class OutlookLocalAdapter:

    def __init__(self):
        try:
            self.app = win32com.client.Dispatch("Outlook.Application")
            self.api = self.app.GetNamespace("MAPI")
            self.calendar = self.api.GetDefaultFolder(9)
        except Exception as e:
            console.panic(f"Outook connection failed:\n{e}")

    def create_timeblock(self, input):
        try:
            appointment = self.app.CreateItem(1) # 1 represents AppointmentItem
            if input.get("start") and isinstance(input["start"], datetime):
                start = input["start"]
            else:
                start = datetime.now().replace(minute=0, second=0)
            appointment.Start = start
            appointment.Subject = input["subject"]
            appointment.Body = input["body"]
            appointment.Duration = input["duration"]
            appointment.Location = input["location"]
            appointment.Categories = input["categories"]
            appointment.Save()
        except Exception as e:
            return AdapterResponse(8, f"Appointment creation failed:\n{e}")

        return AdapterResponse(0, "Appointment created")

    def get_all_appointments(self):
        appointments = self.calendar.Items
        appointments.IncludeRecurrences = True
        appointments.Sort('[Start]')
        return appointments

    def get_day_appointments(self, appointments, date):
        restrict_from = date.strftime("%Y-%d-%m")
        restrict_to = date + timedelta(days=1)
        restrict_to = restrict_to.strftime("%Y-%d-%m")
        restrict_query = f"[Start] >= '{restrict_from}' AND [End] <= '{restrict_to}'"
        appointments = appointments.Restrict(restrict_query)
        restricted_appointments = []

        for appointment in appointments:
            if appointment.Start.year == date.year and \
               appointment.Start.month == date.month and \
               appointment.Start.day == date.day:
               restricted_appointments.append(appointment)
        return restricted_appointments

    def get_conflicting_appointment(self, desired_start, desired_duration, debug = False):
        appointments = self.get_day_appointments(self.get_all_appointments(), desired_start)
        desired_start_time = desired_start.replace(second=0)
        desired_end_time = desired_start_time + timedelta(minutes=desired_duration)

        for appointment in appointments:
            appointment_start_time = appointment.Start.replace(tzinfo=None)
            appointment_end_time = appointment.End.replace(tzinfo=None)

            if debug:
                console.print(f"Checking if desired block ({desired_start_time} - {desired_end_time}) "
                              f"collides with appointment {appointment.Subject} ({appointment_start_time} - {appointment_end_time})")

            if appointment_start_time >= desired_end_time: # appointnments are sorted by Start, so it is safe to end early
                break

            if _is_colliding(appointment_start_time,
                             appointment_end_time,
                             desired_start_time,
                             desired_end_time):
                return AdapterResponse(0, appointment)
        return AdapterResponse(8, "No conflict found")

def _is_colliding(this_start, this_end, other_start, other_end):
    return this_start <= other_start < this_end or \
    this_start < other_end <= this_end
