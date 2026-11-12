# Data model
`User` has a unique email and a password hash. `Application.owner_id` references its owner with cascading deletion. The API checks ownership on every application read, update and delete so identifiers cannot be used to access another account's records.
