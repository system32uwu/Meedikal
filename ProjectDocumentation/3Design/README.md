# NOTES

- Some entities are repeated in order to improve readability
- The atribute _active_ of the **User entity**, indicates if the user is an effective user of the system. In case they change their medical society, instead of wiping them from the database their information and records will be kept, but the user won't be able to access the system to schedule new appointments, this is in order to preserve their data and be able to diagnose their relatives in case of some genetical pathology, or have their medical history available in case they decide to come back, or need to transfer it to their new medical society, for example. Another case for this attribute is when a user comes to afiliate, even if their family members are **_not afiliated_**, it's a good idea to register them in order to keep track of genetical issues or whatever illness or disease a family member had or has that could be determinative to diagnose the user.
  This atribute can have the following values:
  - ACTIVE (effective user)
  - INACTIVE (moved to another society, unsuscribed)
  - NOT_AFFILIATED (might be a relative of a user for example)
- **_relation relationship_** keeps track of the relatives, friends contacts of a person, this is aimed to be used with patients but could also be useful with other kinds of users

- The attribute *content* of the **Form entity**, contains the serialized JSON of the form designed in React.

- The attribute _sessionTime_ of the **Treatment entity**, indicates a _default standard time_ for each session to last for.

- The attribute _indications_ of the **Treatment entity**, contains a JSON with each indication that needs to be followed in the treatment, also containing a _default standard schedule_ to follow.

- The attribute *schedule* of the **_follows relationship_** contains a JSON with the days of the week and the time each session is done, which may or may not be the same as in the _indications_ attribute of the **Treatment entity**.

- The attribute *notes* of the **_follows relationship_** contains a JSON with a follow-up from a session, information contained:

  - date

  - time

  - weekDay

  - media files (nomeclature: followUp-{treatmentID}-{followUpID}-{indexValue}) indexValue increases with each file upload in that followUp, starting at 1.

  - notes

  - sessionTime (how much time the session lasted, in seconds, which may or may not be the same value as its default indicated in the **Treatment entity**).

  **_date_ and _time_ fields should match the _schedule_ attribute, but of course there can be exceptions where the day and/or time of a specific session is changed.**

All the media files, besides of their names, will be saved inside of a folder with a descriptive and identifying path.

For media taken during an appointment while filling a form:

- meedikal/meedikal-FTP/appointment/{(patientSurname|patientID)}{appointmentID}/image1.jpg

For media taken in order to provide graphical indications for a treatment:

- meedikal/meedikal-FTP/treatment/{treatmentID}/indication1.jpg

For media taken during a followUp of a treatment:

- meedikal/meedikal-FTP/followUp/{(patientSurname|patientID)}{treatmentID}/{followUpID}/followUp-3-6-1.jpg
