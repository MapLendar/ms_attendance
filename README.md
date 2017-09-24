# ms_attendance

Attendance events microservice for the calendar-map application

## Structure

The data model for this microservice is very straightforward

#### Attendance model 
| Field    | Type     | Description                                                          |
| ---------| ---------| ---------------------------------------------------------------------|
| user_id  | BigInt   | User ID provided by the users (authentication) microservice          |
| event_id | BigInt   | Event ID provided by the events microservice                         |
| status   | SmallInt | Attendance status (0: not specified, 1: not attending, 2: attending) |

## Endpoints

You can find all the routes this microservice uses in [this file](./api_spec_swagger.yaml), paste it's contents [here](https://editor.swagger.io/) for a fully interactive api spec view.

